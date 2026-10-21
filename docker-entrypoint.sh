#!/bin/sh
# docker-entrypoint.sh
# Punto de entrada unificado para el contenedor ERP Django.
# Se ejecuta en LOCAL (docker-compose) y en PRODUCCIÓN (Render).
# ─────────────────────────────────────────────────────────────────
set -e   # detener si cualquier comando falla

echo "==> [entrypoint] Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

echo "==> [entrypoint] Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "==> [entrypoint] Verificando la configuración de Django..."
python manage.py check --deploy 2>/dev/null || python manage.py check

echo "==> [entrypoint] Verificando y creando superusuario..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@email.com', '12345')"

echo "==> [entrypoint] Iniciando Gunicorn..."
exec gunicorn core.wsgi \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120 \
    --log-file - \
    --access-logfile -
Dar permisos de ejecución:
:: En Windows (Git Bash o WSL):
chmod +x docker-entrypoint.sh

:: Verificar el atributo en git para que se preserve en Linux:
git add docker-entrypoint.sh
git update-index --chmod=+x docker-entrypoint.sh


