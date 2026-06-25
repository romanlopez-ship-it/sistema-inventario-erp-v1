# proveedores/views.py
"""Vistas de la app proveedores — W02 (placeholder)."""
"""from django.shortcuts import render

 Vista de índice de proveedores
    Función que renderiza la página de índice de proveedores con un contexto que incluye 
    el título, descripción y espiral.
    Args:
        request: Objeto HttpRequest que contiene información sobre la solicitud web.  
    Incluido en W02 como placeholder para la vista de índice de proveedores.
    Returns:    
        HttpResponse que contiene la página renderizada de índice de proveedores.      
def index(request):
    
    context = {
        'titulo': 'Proveedores',
        'descripcion': 'Red de proveedores de mercancía.',
        'espiral': 'Espiral 2 · W04',
    }
    return render(request, 'proveedores/index.html', context)
"""

# proveedores/views.py
"""Vistas de la app proveedores — W07 y W08

Lectura: ListView y DetailView.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from .forms import ProveedorForm

from .models import Proveedor


class ProveedorListView(ListView):
    """Lista paginada de proveedores activos."""

    model               = Proveedor
    template_name       = 'proveedores/lista.html'
    context_object_name = 'proveedores'
    paginate_by         = 20

    def get_queryset(self):
        return Proveedor.objects.filter(activo=True).order_by('nombre')


class ProveedorDetailView(DetailView):
    """Detalle de un proveedor con sus productos asociados."""

    model               = Proveedor
    template_name       = 'proveedores/detalle.html'
    context_object_name = 'proveedor'
    pk_url_kwarg        = 'proveedor_id'

    """
    Agrega los productos del proveedor al contexto de la vista de detalle.
    Se filtran los productos activos y se ordenan por nombre.
    
    Returns:
        dict: Contexto de la vista de detalle con los productos del proveedor.
  """
    def get_context_data(self, **kwargs):
        """Agrega los productos del proveedor al contexto."""
        ctx = super().get_context_data(**kwargs) # Llama al método get_context_data 
                                                 # de la clase base para obtener el contexto inicial.
        # Agrega los productos del proveedor al contexto.
        ctx['productos'] = (
            self.object.productos # Accede a los productos relacionados con el proveedor actual.
            .select_related('categoria') # Optimiza la consulta para obtener la categoría 
                                         # de cada producto en la misma consulta.
            .filter(activo=True)         # Filtra los productos activos.
            .order_by('nombre')          # Ordena los productos por nombre.
        )
        return ctx # Devuelve el contexto actualizado con los productos del proveedor.
    

class ProveedorCreateView(LoginRequiredMixin, CreateView):
    """Formulario para crear un proveedor."""

    model         = Proveedor
    form_class    = ProveedorForm
    template_name = 'proveedores/crear.html'
    success_url   = reverse_lazy('proveedores:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Proveedor "{self.object.nombre}" creado exitosamente.'
        )
        return response


class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    """Formulario para editar un proveedor."""

    model         = Proveedor
    form_class    = ProveedorForm
    template_name = 'proveedores/editar.html'
    pk_url_kwarg  = 'proveedor_id'
    success_url   = reverse_lazy('proveedores:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Proveedor "{self.object.nombre}" actualizado.'
        )
        return response


class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
    """Confirmación y borrado de un proveedor."""

    model         = Proveedor
    template_name = 'proveedores/eliminar.html'
    pk_url_kwarg  = 'proveedor_id'
    success_url   = reverse_lazy('proveedores:lista')

    def form_valid(self, form):
        nombre   = self.object.nombre
        response = super().form_valid(form)
        messages.success(self.request, f'Proveedor "{nombre}" eliminado.')
        return response