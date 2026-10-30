"""Suite de pruebas W12 — Factura PDF con WeasyPrint.

Requiere Linux/Docker (WeasyPrint necesita Pango y Cairo).

Ejecutar con:
    docker compose run --rm --entrypoint "" web python manage.py test tests.test_w12_pdf -v 2
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from clientes.models import Cliente
from configuracion.models import ConfiguracionERP
from productos.models import Categoria, Producto
from ventas.models import DetalleVenta, Venta


class VentaPdfTest(TestCase):
    """Comportamiento de /ventas/<id>/pdf/."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", password="testpass123")
        cliente = Cliente.objects.create(nombre="Cliente PDF", correo="pdf@example.com")
        categoria = Categoria.objects.create(nombre="General")
        producto = Producto.objects.create(
            nombre="SSD 1TB", precio=Decimal("1500.00"), stock=10, categoria=categoria
        )
        self.venta = Venta.objects.create(cliente=cliente)
        DetalleVenta.objects.create(venta=self.venta, producto=producto, cantidad=2)
        self.url = reverse("ventas:pdf", kwargs={"venta_id": self.venta.pk})

    def test_sin_login_redirige_a_login(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 302)
        self.assertIn("login", r["Location"])

    def test_venta_inexistente_404(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("ventas:pdf", kwargs={"venta_id": 999999}))
        self.assertEqual(r.status_code, 404)

    def test_pdf_valido(self):
        self.client.force_login(self.user)
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "application/pdf")
        self.assertTrue(r.content.startswith(b"%PDF"))

    def test_logo_inexistente_no_rompe_pdf(self):
        """Disco efímero de Render: el archivo del logo puede no existir."""
        config = ConfiguracionERP.get_instance()
        config.logo.name = "configuracion/no-existe.png"
        config.save(update_fields=["logo"])
        self.client.force_login(self.user)
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.content.startswith(b"%PDF"))


class TotalesFacturaTest(TestCase):
    """El TOTAL de la factura debe incluir el IVA."""

    def test_calculo_iva_y_total(self):
        from ventas.views import calcular_totales
        t = calcular_totales(Decimal("3000"), Decimal("16.00"))
        self.assertEqual(t["subtotal"], Decimal("3000.00"))
        self.assertEqual(t["iva"], Decimal("480.00"))
        self.assertEqual(t["total_con_iva"], Decimal("3480.00"))

    def test_redondeo_a_centavos(self):
        from ventas.views import calcular_totales
        t = calcular_totales(Decimal("10.05"), Decimal("16.00"))
        self.assertEqual(t["iva"], Decimal("1.61"))           # 1.608 -> 1.61
        self.assertEqual(t["total_con_iva"], Decimal("11.66"))

    def test_plantilla_muestra_total_con_iva(self):
        from django.template.loader import render_to_string
        from ventas.views import calcular_totales
        cliente = Cliente.objects.create(nombre="C", correo="c@example.com")
        venta = Venta.objects.create(cliente=cliente)
        config = ConfiguracionERP.get_instance()
        html = render_to_string("ventas/factura_pdf.html", {
            "venta": venta, "config": config,
            **calcular_totales(Decimal("3000"), config.iva_porcentaje),
        })
        self.assertIn("$480.00", html)
        self.assertIn("$3480.00", html)
