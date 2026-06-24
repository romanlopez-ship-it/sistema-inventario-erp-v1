# ventas/urls.py
"""URLs de la app productos — W02."""
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