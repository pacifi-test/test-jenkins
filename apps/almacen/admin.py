from django.contrib import admin
from .models.almacen import Almacen
from .models.equipo import Equipo
from .models.salida import Salida
from .models.salida_detalle import SalidaDetalle


@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    pass


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("id", "compra_detalle", "producto", "imei", "user", "estado", "contable", "created_at")


@admin.register(Salida)
class SalidaAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "estado", "codigo", "arqueado", "vendedor")


@admin.register(SalidaDetalle)
class SalidaDetalleAdmin(admin.ModelAdmin):
    list_display = ("id", "salida", "equipo",)
