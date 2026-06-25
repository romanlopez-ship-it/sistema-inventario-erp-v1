# proveedores/urls.py
"""URLs de la app proveedores — W02.
from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.index, name='inicio'),
    # Espiral 2 W05:
    # path('lista/',          views.ProveedoresListView.as_view(),   name='lista'),
    # path('nuevo/',          views.ProveedoresCreateView.as_view(), name='crear'),
    # path('<int:pk>/',       views.ProveedoresDetailView.as_view(), name='detalle'),
    # path('<int:pk>/editar/',views.ProveedoresUpdateView.as_view(), name='editar'),
]

"""

# proveedores/urls.py
"""URLs de la app proveedores — W07."""
from django.urls import path
from . import views

app_name = 'proveedores'
# Uso de Class-Based Views (CBV) para la lectura de datos (W07). 
# Las vistas de escritura (W08) se implementarán más adelante.
urlpatterns = [
    path('',                            views.ProveedorListView.as_view(),    name='lista'),
    path('<int:proveedor_id>/',         views.ProveedorDetailView.as_view(),  name='detalle'),
    path('nuevo/',                      views.ProveedorCreateView.as_view(),  name='crear'),
    path('<int:proveedor_id>/editar/',   views.ProveedorUpdateView.as_view(),  name='editar'),
    path('<int:proveedor_id>/eliminar/', views.ProveedorDeleteView.as_view(), name='eliminar'),
]