# W17 — Listo para producción (SendGrid + django-anymail)

*Verificación: 2026-11-19*

W17 está lista para producción, con una condición: antes de subir tienes que verificar el remitente en SendGrid (paso 1). Lo hice todo sin Docker: en el laboratorio las tareas corren en modo EAGER y los correos se imprimen en la consola. No hice commit.

## Qué se verificó

| Verificación | Resultado |
|---|---|
| `manage.py check` | Sin problemas |
| Migración `0004_correo_enviado_pedido` | Aplicada |
| Prueba en el shell con backend de consola (Parte 5) | 1.ª llamada `ok`, 2.ª `skip`: no se envía dos veces. La alerta de stock también sale bien |
| `test_w17_correo` | 12/12 OK (las 9 de la guía + 3 que agregué para los errores que corregí) |
| Pruebas de W13 a W17 | 48/48 OK |
| Suite completa | 159 pruebas. Siguen las mismas 11 fallas de antes en W01/W02/W03/W08/W12; W17 no agrega ninguna |
| Tu API Key de SendGrid | Válida, con permiso de envío (Mail Send). La consulté en solo lectura y no envié ningún correo |

## Cambios en el proyecto

- **Archivos nuevos:** `templates/emails/` (4 plantillas), `tests/test_w17_correo.py` y la migración `0004`.
- **Archivos modificados:** `core/settings.py`, `core/settings_prod.py`, `ventas/models.py`, `ventas/tasks.py`, `render.yaml`, `requirements.txt` (sigue en UTF-8), `.env.example` y `sprint5_planning.md`.
- **Tu API Key** solo está en `.env`, que Git ignora, así que no se sube al repositorio.

## Errores corregidos en la guía (16)

Los más graves, que habrían roto producción:

1. **Faltaba verificar el remitente.** SendGrid rechaza el correo con error 403 si el remitente no está verificado. Agregué la sección 1.2-bis.
2. **`ip_pool_name` en la configuración** hace fallar el envío en una cuenta gratuita. Lo quité.
3. **La URL de Render estaba fija** en el código. Ahora se toma de `SITE_URL`, que en Render sale sola de `RENDER_EXTERNAL_URL`.
4. **El enlace del correo apuntaba a `/ventas/<pk>/`**, que es el detalle de una Venta, no de un Pedido. Ahora el botón lleva a la tienda.
5. **El subtotal perdía los centavos** (`{% widthratio %}` redondea a entero) y **el texto plano mostraba entidades HTML** (`O&#x27;Brien`). Corregí las dos cosas.

La tabla completa está en la sección **NOTAS** al final de [Guia_Lab_W17.md](guias/Guia_Lab_W17.md). También agregué una **PARTE 7** nueva, con el despliegue en Render y una tabla de solución de problemas.

## Pasos para subir a Render

1. En SendGrid ve a **Settings → Sender Authentication → Verify a Single Sender**, verifica tu correo y usa ese mismo correo como `DEFAULT_FROM_EMAIL`. No pude revisar si ya tienes uno, porque la clave no tiene permiso para listar remitentes.
2. Agrega las 3 variables nuevas en Render (Environment). Como el servicio ya existe, el Blueprint no las crea solo.
3. Haz `git add .`, revisa que **no** aparezca `.env`, haz el commit y `git push origin main`.
4. En los Logs confirma `Applying ventas.0004... OK`. Luego haz una compra con la tarjeta 4242 y revisa tu bandeja, incluida la carpeta de Spam.

## Variables de entorno del servicio web en Render

| Variable | Valor | ¿Nueva? |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | `core.settings_prod` | |
| `SECRET_KEY` | generada por Render | |
| `DEBUG` | `False` | |
| `ALLOWED_HOSTS` | `.onrender.com` | |
| `DATABASE_URL` | Internal URL de `erp-django-db` | |
| `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY` | `sk_test_…` / `pk_test_…` | |
| `STRIPE_WEBHOOK_SECRET` | el `whsec_` del endpoint creado en el Dashboard de Stripe | |
| `REDIS_URL` | Internal Key Value URL (`redis://red-…:6379`) | |
| `CELERY_EMBEDDED_WORKER` | `1` | |
| **`SENDGRID_API_KEY`** | tu clave `SG.…` (está en `.env`) | ✅ W17 |
| **`DEFAULT_FROM_EMAIL`** | `ERP Django <tu-correo-verificado@gmail.com>` | ✅ W17 |
| **`ADMIN_EMAIL`** | el correo que recibirá las alertas de stock y los errores 500 | ✅ W17 |

No agregues `EMAIL_BACKEND` ni `RENDER_EXTERNAL_URL`. La primera la decide `settings_prod.py` y la segunda la pone Render automáticamente.

**Sobre la clave:** como se compartió en un chat, conviene crear una nueva en SendGrid cuando termines de probar, borrar la anterior y actualizar `SENDGRID_API_KEY` en Render y en `.env`.
