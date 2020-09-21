from django.contrib import admin

from apps.compra.models.compra_detalle import CompraDetalle
from .models.compra import Compra


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'nro_correlativo', 'proveedor', 'nro_comprobante', 'procesado', 'estado', 'fecha_emision']


@admin.register(CompraDetalle)
class CompraDetalleAdmin(admin.ModelAdmin):
    list_display = ("id", "igv", "valor_unitario", "precio_unitario", "igv_total", "precio_total", "total")
