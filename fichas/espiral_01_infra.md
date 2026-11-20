# Ficha de Sistematización — Espiral 1
## ERP Django · Espiral E1: Infraestructura y Configuración Base
## UTEC Celaya · Técnico en Programación (SEP 3061300006-23)

| Campo | Contenido |
|---|---|
| **Número de espiral** | 1 |
| **Nombre del ciclo** | Infraestructura y Configuración Base |
| **Semanas** | W01 – W03 |
| **Fecha de inicio** | ___/___/_____ |
| **Fecha de cierre** | ___/___/_____ |
| **Responsable** | [Nombre del estudiante] |
| **Asesor** | MC. Román Fernando López González |

---

## 1. Objetivo del ciclo

Establecer el entorno de desarrollo portable en USB y desplegar el
proyecto Django base en Render.com, de modo que cualquier avance
posterior tenga una URL pública verificable desde el inicio del proyecto.

---

## 2. Tareas realizadas

| # | Tarea | Estado | Artefacto en el repositorio | Tiempo invertido |
|---|---|---|---|---|
| 1 | Configurar Python 3.11 embeddable en USB | ✅ | `env_erp/` (Python 3.11.9) | h:mm |
| 2 | Instalar pip y virtualenv | ✅ | `env_erp/` | h:mm |
| 3 | Configurar Git Portable | ✅ | repositorio `main` | h:mm |
| 4 | Crear scripts iniciar/finalizar sesión | ✅ | `E:\iniciar_sesion.bat`, `E:\finalizar_sesion.bat` (USB) | h:mm |
| 5 | Crear proyecto Django con 5 apps | ✅ | `clientes/ proveedores/ productos/ ventas/ reportes/` | h:mm |
| 6 | Sistema de templates Fable 5 AzulERP | ✅ | `templates/base.html`, `templates/bienvenida.html` | h:mm |
| 7 | Configurar WhiteNoise y estáticos | ✅ | `core/settings.py` (STATIC_ROOT, WhiteNoise) | h:mm |
| 8 | Completar settings_prod.py con PostgreSQL | ✅ | `core/settings_prod.py` (`dj_database_url`) | h:mm |
| 9 | Crear Procfile, Dockerfile, docker-compose.yml | ✅ | `Procfile`, `Dockerfile`, `docker-compose.yml` | h:mm |
| 10 | Crear render.yaml | ✅ | `render.yaml` | h:mm |
| 11 | Desplegar en Render.com → URL pública | ✅ | servicio `erp-django-utec-web` | h:mm |
| 12 | Ejecutar Sprint 0 Review y Retrospectiva | ✅ | `sprint1_planning.md` | h:mm |

---

## 3. Evidencias generadas

- [x] Repositorio GitHub: `https://github.com/romanlopez-ship-it/sistema-inventario-erp-v1`
- [x] URL pública Render: `https://erp-django-utec-web.onrender.com`
- [ ] Captura de pantalla: `evidencias/espiral_01/render_url.png`
- [ ] Captura de pantalla: `evidencias/espiral_01/manage_check.png`
- [x] Pruebas de la espiral: `tests/test_w01_entorno.py`, `tests/test_w02_mvt.py`,
      `tests/test_w03_deploy.py` → OK
- [ ] Commit de cierre:
```
El historial de Git de este repositorio inicia en W11 (sincronización
del 2026-10-30); los commits de W01–W03 no están disponibles.
```

---

## 4. Criterios de aceptación verificados

| Criterio | ¿Cumplido? | Evidencia |
|---|---|---|
| `manage.py check --deploy` sin warnings críticos | ✅ | Lo ejecuta `docker-entrypoint.sh` en cada despliegue (Logs de Render) |
| URL pública `https://…onrender.com/` → HTTP 200 | ✅ | `healthCheckPath: /` en `render.yaml` |
| Repositorio con ≥ 6 commits en rama `main` | ✅ | `git log --oneline` |
| Pruebas W01 + W02 + W03 pasando | ✅ | `python manage.py test tests.test_w01_entorno tests.test_w02_mvt tests.test_w03_deploy` |
| Ficha Schmelkes E1 completa | ✅ | Este documento |

---

## 5. Problemas encontrados y soluciones

| Problema | Causa | Solución aplicada |
|---|---|---|
| `/clientes/` respondía 404 (enlace del menú del admin roto) | Desde W07 la lista de clientes vive en `/clientes/lista/` y no quedó ruta raíz | Ruta `''` → `ClienteListView` (`clientes:inicio`), igual que las demás apps |
| Pruebas de W02 buscaban `<app>:inicio` y `<app>/index.html` | W07 reemplazó las vistas `index` por CBV con `lista.html` | Pruebas de W02 actualizadas a `<app>:lista` / `<app>/lista.html` |
| `docker-entrypoint.sh` fallaba en Render | Finales de línea CRLF de Windows | `.gitattributes` con `*.sh text eol=lf` |

---

## 6. Lecciones aprendidas

1.
2.
3.

---

## 7. Tiempo total invertido

| Categoría | Horas |
|---|---|
| Diseño | |
| Implementación | |
| Pruebas | |
| Documentación | |
| **Total Espiral 1** | |
