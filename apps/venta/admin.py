from django.contrib import admin

from apps.venta.models.venta import Venta
from apps.venta.models.venta_detalle import VentaDetalle


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        "id", "nro_correlativo", "total", "base_imponible", "tipo_comprobante", "igv", "created_at")


@admin.register(VentaDetalle)
class VentaDetalleAdmin(admin.ModelAdmin):
    list_display = ("id", "cantidad", "precio_unitario", "precio_total", "base_imponible", "igv")
