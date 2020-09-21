from django.contrib import admin

from .models.pedido import Pedido
from .models.pedido_detalle import PedidoDetalle


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "total", "cliente", "distribuidor", "estado")


@admin.register(PedidoDetalle)
class PedidoDetalleAdmin(admin.ModelAdmin):
    pass
