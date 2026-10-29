"""Módulo auxiliar de diagnóstico del servidor y stack técnico."""

import os
import platform
import sys
import django
from django.conf import settings
from django.http import HttpResponse
from django.template import Context, Template


def obtener_reporte_stack_html():
    """Ejecuta las pruebas del sistema y devuelve el HTML formateado."""
    # 1. Entorno
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

    # 5. Librerías clave
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

    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Diagnóstico de Servidor & Stack</title>
    </head>
    <body>
        <h1>🛠️ Diagnóstico de Servidor & Stack</h1>
        
        <h2>1. Entorno</h2>
        <ul>
            <li>Python: {{ py_version }}</li>
            <li>S.O.: {{ os_platform }}</li>
            <li>Django: {{ django_version }}</li>
        </ul>

        <h2>2. Base de Datos (PostgreSQL)</h2>
        <p>Estado: {% if db_status.ok %}✅ CONECTADO ({{ db_status.vendor }}){% else %}❌ ERROR DE CONEXIÓN{% endif %}</p>
        <p>Versión: {{ db_status.version }}</p>
        {% if db_status.error %}<p>Error: {{ db_status.error }}</p>{% endif %}

        <h2>3. Motor de PDF (WeasyPrint)</h2>
        <p>Estado: {% if weasy_status.ok %}✅ FUNCIONAL (v{{ weasy_status.version }}){% else %}❌ FALLÓ{% endif %}</p>
        {% if weasy_status.ok %}
        <p>PDF de prueba generado correctamente ({{ weasy_status.pdf_bytes }} bytes).</p>
        {% endif %}
        {% if weasy_status.error %}<p>Error: {{ weasy_status.error }}</p>{% endif %}

        <h2>4. Caché / Redis</h2>
        <p>Estado: {% if redis_status.ok %}✅ CONECTADO{% else %}❌ ERROR{% endif %}</p>
        <p>Backend: {{ redis_status.backend }}</p>
        {% if redis_status.error %}<p>Error: {{ redis_status.error }}</p>{% endif %}

        <h2>5. Paquetes</h2>
        <ul>
            {% for name, ver in pkgs.items %}
            <li><strong>{{ name }}:</strong> {{ ver }}</li>
            {% endfor %}
        </ul>

        <h2>6. Variables de Entorno</h2>
        <ul>
            {% for key, val in env_vars.items %}
            <li><strong>{{ key }}:</strong> {{ val }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """

    t = Template(html_template)
    c = Context(
        {
            "py_version": py_version,
            "os_platform": os_platform,
            "django_version": django.get_version(),
            "db_status": db_status,
            "redis_status": redis_status,
            "weasy_status": weasy_status,
            "pkgs": pkgs,
            "env_vars": env_vars,
        }
    )
    return HttpResponse(t.render(c))