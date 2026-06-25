# productos/urls.py
"""
    URLs de la app productos — W02.
from django.urls import path
from . import views

app_name = 'productos'
    # Espiral 2 W05: 
urlpatterns = [
    path('', views.index, name='inicio'),
    # Espiral 2 W05:
    # path('lista/',          views.ProductoListView.as_view(),   name='lista'),
    # path('nuevo/',          views.ProductoCreateView.as_view(), name='crear'),
    # path('<int:pk>/',       views.ProductoDetailView.as_view(), name='detalle'),
    # path('<int:pk>/editar/',views.ProductoUpdateView.as_view(), name='editar'),
]
"""
# productos/urls.py
"""URLs de la app productos — W07 (Lista + Detalle)."""
from django.urls import path
from . import views

app_name = 'productos'
# Uso de Class-Based Views (CBV) para la lectura de datos (W07). 
# Las vistas de escritura (W08) se implementarán más adelante.
urlpatterns = [
    # Lectura (W07)
    path('',                    views.ProductoListView.as_view(),       name='lista'),
    path('<int:producto_id>/',  views.ProductoDetailView.as_view(),     name='detalle'),
    # Escritura (W08) — comentadas hasta implementarlas
    path('nuevo/',                    views.ProductoCreateView.as_view(), name='crear'),
    path('<int:producto_id>/editar/',  views.ProductoUpdateView.as_view(), name='editar'),
    path('<int:producto_id>/eliminar/',views.ProductoDeleteView.as_view(), name='eliminar'),
]