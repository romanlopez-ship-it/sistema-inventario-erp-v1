"""Módulo auxiliar de diagnóstico del servidor y stack técnico."""

import os
import platform
import sys
import django
from django.conf import settings


def obtener_contexto_diagnostico() -> dict:
    """Ejecuta las pruebas de diagnóstico y retorna el contexto estructurado."""
    # 1. Entorno de Ejecución
    py_version = sys.version
    os_platform = platform.platform()

    # 2. Base de datos
    db_status = {"ok": False, "vendor": "", "version": "", "error": ""}
    try:
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            row = cursor.fetchone()
            db_status["ok"] = True
            db_status["vendor"] = connection.vendor
            db_status["version"] = row[0] if row else "Conectado"
    except Exception as e:
        db_status["error"] = str(e)

    # 3. Redis / Caché
    redis_status = {
        "ok": False,
        "backend": settings.CACHES["default"]["BACKEND"],
        "error": "",
    }
    try:
        from django.core.cache import cache

        cache.set("stack_info_test", "PONG", timeout=10)
        if cache.get("stack_info_test") == "PONG":
            redis_status["ok"] = True
    except Exception as e:
        redis_status["error"] = str(e)

    # 4. WeasyPrint
    weasy_status = {
        "ok": False,
        "version": "No disponible",
        "pdf_bytes": 0,
        "error": "",
    }
    try:
        import weasyprint

        weasy_status["version"] = weasyprint.__version__
        pdf_bin = weasyprint.HTML(
            string="<h1>Test Render WeasyPrint</h1><p>ERP Django UTEC</p>"
        ).write_pdf()
        if pdf_bin and pdf_bin.startswith(b"%PDF"):
            weasy_status["ok"] = True
            weasy_status["pdf_bytes"] = len(pdf_bin)
    except Exception as e:
        weasy_status["error"] = str(e)

    # 5. Paquetes Clave del ERP
    pkgs = {}
    for pkg_name, module_name in [
        ("Django REST Framework", "rest_framework"),
        ("Pillow (Imágenes)", "PIL"),
        ("openpyxl (Excel)", "openpyxl"),
        ("Celery", "celery"),
        ("django-storages", "storages"),
        ("Anymail (SendGrid)", "anymail"),
    ]:
        try:
            mod = __import__(module_name)
            pkgs[pkg_name] = getattr(mod, "__version__", "Instalado")
        except ImportError:
            pkgs[pkg_name] = "❌ No instalado"

    # 6. Variables de Entorno
    env_vars = {
        "DJANGO_SETTINGS_MODULE": os.environ.get(
            "DJANGO_SETTINGS_MODULE", "No definida"
        ),
        "DEBUG": str(settings.DEBUG),
        "ALLOWED_HOSTS": str(settings.ALLOWED_HOSTS),
        "RENDER_EXTERNAL_HOSTNAME": os.environ.get(
            "RENDER_EXTERNAL_HOSTNAME", "N/A (Local)"
        ),
        "DATABASE_URL": (
            "Configurada (Oculta)"
            if os.environ.get("DATABASE_URL")
            else "No definida"
        ),
        "REDIS_URL": (
            "Configurada (Oculta)"
            if os.environ.get("REDIS_URL")
            else "No definida"
        ),
    }

    return {
        "py_version": py_version,
        "os_platform": os_platform,
        "django_version": django.get_version(),
        "db_status": db_status,
        "redis_status": redis_status,
        "weasy_status": weasy_status,
        "pkgs": pkgs,
        "env_vars": env_vars,
    }