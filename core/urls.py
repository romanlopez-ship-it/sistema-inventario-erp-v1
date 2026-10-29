"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# core/urls.py
"""Enrutador principal del ERP Django — W01."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

# Importar vistas del núcleo
from . import views

""" Forzar la creación del superusuario en producción 
    sin intervención manual 
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()
try:
    # Intenta crear el superusuario usando el método oficial de Django
    User.objects.create_superuser('admin', 'admin@example.com', 'AdminUTEC2026*')
    print("¡Superusuario creado con éxito en producción!")
except IntegrityError:
    # Si el usuario ya existe, no hace nada y evita que el servidor falle
    pass
"""
# Importar y combinar todas las URLs de la API
from productos.api_urls   import urlpatterns as productos_api
from clientes.api_urls    import urlpatterns as clientes_api
from proveedores.api_urls import urlpatterns as proveedores_api
from ventas.api_urls      import urlpatterns as ventas_api

api_urlpatterns = (
    productos_api +
    clientes_api  +
    proveedores_api +
    ventas_api
)

urlpatterns = [
    path('admin/',       admin.site.urls),
    path('',             views.bienvenida,             name='inicio'),
    
    # Ruta discreta/oculta para verificación del servidor en Render
    path("_sys_status/", views.status_check, name="status_check"),

    # Allauth (login / logout / registro)
    path('accounts/',    include('allauth.urls')),     # ← agregar 
    # API REST
    path('api/',        include((api_urlpatterns, 'api'))), # ← agregar W10
    path('api/auth/token/', obtain_auth_token, name='api_token'), # ← agregar W10
    # Apps del ERP
    path('clientes/',    include('clientes.urls',       namespace='clientes')),
    path('proveedores/', include('proveedores.urls',    namespace='proveedores')),
    path('productos/',   include('productos.urls',      namespace='productos')),
    path('ventas/',      include('ventas.urls',         namespace='ventas')),
    path('reportes/',    include('reportes.urls',       namespace='reportes')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)