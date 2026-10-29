# ventas/urls.py
"""URLs de la app productos — W02.
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.index, name='inicio'),
    # Espiral 2 W05:
    # path('lista/',          views.VentasListView.as_view(),   name='lista'),
    # path('nuevo/',          views.VentasCreateView.as_view(), name='crear'),
    # path('<int:pk>/',       views.VentasDetailView.as_view(), name='detalle'),
    # path('<int:pk>/editar/',views.VentasUpdateView.as_view(), name='editar'),
]
"""
# ventas/urls.py
"""URLs de la app ventas — W07."""
from django.urls import path
from . import views

app_name = 'ventas'
# Uso de Class-Based Views (CBV) para la lectura de datos (W07). 
# Las vistas de escritura (W08) se implementarán más adelante.
urlpatterns = [
    path('',                        views.VentaListView.as_view(),      name='lista'),
    path('<int:venta_id>/',         views.VentaDetailView.as_view(),    name='detalle'),
    path('nueva/',                  views.crear_venta,                 name='crear'),
    path('<int:venta_id>/eliminar/',views.VentaDeleteView.as_view(),   name='eliminar'),

   # Ruta W12 para la descarga de PDF 
   path('<int:venta_id>/pdf/'      ,views.venta_pdf,                   name='pdf'), 
]