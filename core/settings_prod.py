# core/settings_prod.py
"""Configuración de producción — Render.com (borrador W02).

Hereda settings.py y sobreescribe valores críticos para producción.
W03 completará: DATABASE_URL con PostgreSQL, variables de Render.

Uso:
    DJANGO_SETTINGS_MODULE=core.settings_prod gunicorn core.wsgi
"""
from .settings import *   # hereda toda la configuración base
import os
import dj_database_url 

# Seguridad básica
DEBUG      = False
SECRET_KEY = os.environ['SECRET_KEY']   # obligatorio; sin default en prod

# ── HOSTS PERMITIDOS ────────────────────────────────────────────────────────
# Render inyecta RENDER_EXTERNAL_HOSTNAME automáticamente
_render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
_extra_hosts  = os.environ.get('ALLOWED_HOSTS', '').split(',')

ALLOWED_HOSTS = ['localhost', '127.0.0.1'] + (
    [_render_host] if _render_host else []
) + [h for h in _extra_hosts if h]

# ── BASE DE DATOS: PostgreSQL via DATABASE_URL ─────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,          # conexiones persistentes 10 min
        conn_health_checks=True,   # verifica conexión antes de usarla
        ssl_require=True,          # Render requiere SSL en PostgreSQL
    )
}

# HTTPS y cookies seguras
SECURE_SSL_REDIRECT            = True
SECURE_HSTS_SECONDS            = 31536000    # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD            = True
SESSION_COOKIE_SECURE          = True
CSRF_COOKIE_SECURE             = True
X_FRAME_OPTIONS                = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF    = True
SECURE_REFERRER_POLICY         = 'same-origin'

# ── ARCHIVOS ESTÁTICOS ─────────────────────────────────────────────────────
# WhiteNoise ya configurado en settings.py; solo confirmar almacenamiento
WHITENOISE_MANIFEST_STRICT = False
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging mínimo en producción
# ── LOGGING: solo WARNING y superiores en producción ──────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '[%(levelname)s] %(name)s: %(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django.security': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# W03 agregará:
# import dj_database_url
# DATABASES = {'default': dj_database_url.config(conn_max_age=600)}