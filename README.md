# ERP Django — UTEC Celaya

ERP académico con Django 4.2 LTS, DRF, PostgreSQL y facturas PDF con WeasyPrint 60.2.
Se despliega en Render.com como **Web Service con Docker**. WeasyPrint necesita
Pango y Cairo, que solo trae la imagen Docker; con el buildpack de Python falla.

## Ejecutar en local (Docker)

```bash
cp .env.example .env          # ajusta SECRET_KEY
docker compose up --build     # http://localhost:8000
```

El entrypoint aplica migraciones, recolecta estáticos, crea el superusuario
de prácticas `admin` / `12345` (solo si no existe) y arranca Gunicorn en `$PORT`.

Tests (WeasyPrint solo funciona dentro del contenedor):

```bash
docker compose run --rm --entrypoint "" -e DJANGO_SETTINGS_MODULE=core.settings \
  -v "$PWD/tests:/app/tests" web python manage.py test tests
```

## Desplegar en Render

1. Crea una base **PostgreSQL** (plan free) en la misma región que el servicio web.
2. Crea un **Web Service** desde este repositorio con **Language: Docker**
   (Dockerfile en la raíz, sin Build ni Start Command).
3. Health Check Path: `/`.
4. Variables de entorno:

| Variable | Valor | ¿Secreta? |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | `core.settings_prod` | No |
| `SECRET_KEY` | cadena larga y aleatoria | **Sí** |
| `DATABASE_URL` | Internal Database URL de la base de Render | **Sí** |
| `ALLOWED_HOSTS` | `.onrender.com` | No |
| `DEBUG` | `False` | No |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME` | solo si usas S3 para media (W11) | **Sí** |

Render define `PORT` y `RENDER_EXTERNAL_HOSTNAME`; no las agregues a mano.

## Verificar tras el deploy

| Petición | Esperado |
|---|---|
| `GET /` | 200 |
| `GET /ventas/1/pdf/` sin sesión | 302 a `/accounts/login/` |
| `GET /ventas/1/pdf/` con sesión | 200, `application/pdf` |
| `GET /ventas/999999/pdf/` con sesión | 404 |

En el plan free el servicio se suspende tras ~15 min sin tráfico; la primera
petición puede tardar cerca de un minuto. Eso no es un fallo.
