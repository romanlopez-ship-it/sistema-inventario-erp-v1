"""Vistas de la app ventas — W07 / W08 / W12.

Lectura: VentaListView y VentaDetailView (W07).
Escritura: crear_venta y VentaDeleteView (W08).
Exportación PDF: venta_pdf con WeasyPrint (W12).
"""

from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from configuracion.models import ConfiguracionERP
from .forms import DetalleVentaForm, VentaForm
from .models import DetalleVenta, Venta


class VentaListView(ListView):
    """Lista paginada de ventas en orden cronológico inverso."""

    model = Venta
    template_name = "ventas/lista.html"
    context_object_name = "ventas"
    paginate_by = 20

    def get_queryset(self):
        """Pre-carga cliente para evitar N+1 en la tabla de ventas."""
        return Venta.objects.select_related("cliente").order_by("-fecha")


class VentaDetailView(DetailView):
    """Detalle de una venta con todas sus líneas de producto."""

    model = Venta
    template_name = "ventas/detalle.html"
    context_object_name = "venta"
    pk_url_kwarg = "venta_id"

    def get_queryset(self):
        """Pre-carga cliente y prefetch líneas de detalle."""
        return Venta.objects.select_related("cliente").prefetch_related(
            "detalles__producto"
        )


def crear_venta(request):
    """Crea un encabezado de venta con una línea de detalle.

    GET → muestra los dos formularios vacíos.
    POST → valida ambos, guarda si correctos, muestra errores si no.
    Protección: redirige a login si no autenticado.
    """
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    venta_form = VentaForm(request.POST or None)
    detalle_form = DetalleVentaForm(request.POST or None)

    if request.method == "POST":
        if venta_form.is_valid() and detalle_form.is_valid():
            venta = venta_form.save()
            detalle = detalle_form.save(commit=False)
            detalle.venta = venta
            # precio_unitario se auto-captura en save() si es None
            detalle.save()
            messages.success(
                request,
                f"Venta #{venta.pk} registrada. Total: ${venta.total:.2f}",
            )
            return redirect("ventas:detalle", venta_id=venta.pk)

    return render(
        request,
        "ventas/crear.html",
        {
            "venta_form": venta_form,
            "detalle_form": detalle_form,
        },
    )


class VentaDeleteView(LoginRequiredMixin, DeleteView):
    """Confirmación y borrado de una venta (y sus detalles en cascada)."""

    model = Venta
    template_name = "ventas/eliminar.html"
    pk_url_kwarg = "venta_id"
    success_url = reverse_lazy("ventas:lista")

    def form_valid(self, form):
        pk = self.object.pk
        response = super().form_valid(form)
        messages.success(self.request, f"Venta #{pk} eliminada.")
        return response


# ── W12: GENERACIÓN DE FACTURA PDF CON WEASYPRINT ────────────────────────────


@login_required
def venta_pdf(request, venta_id: int) -> HttpResponse:
    """Genera y descarga la factura de una venta en formato PDF.

    Motor: WeasyPrint (requiere entorno Linux o contenedor Docker).

    Args:
        request: HttpRequest de Django.
        venta_id: ID de la venta a generar.

    Returns:
        HttpResponse con Content-Type application/pdf y descarga directa.
    """
    import weasyprint  # Importación local para entorno Docker/Linux

    venta = get_object_or_404(
        Venta.objects.select_related("cliente").prefetch_related(
            "detalles__producto__categoria"
        ),
        pk=venta_id,
    )
    config = ConfiguracionERP.get_instance()
    context = {
        "venta": venta,
        "config": config,
        "hoy": date.today(),
    }

    html_string = render_to_string(
        "ventas/factura_pdf.html", context, request=request
    )

    # base_url permite que WeasyPrint encuentre imágenes y archivos estáticos
    pdf_bytes = weasyprint.HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="factura_{venta.pk:05d}.pdf"'
    )
    return response