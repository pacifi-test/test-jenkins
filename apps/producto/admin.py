from django.contrib import admin

from .models.categoria import Categoria
from .models.galeria import Galeria
from .models.marca import Marca
from .models.producto import Producto
from .models.producto_general import ProductoGeneral
from .models.sistema_operativo import SistemaOperativo
from .models.precio_venta import PrecioVenta


@admin.register(Categoria)
class CategriaAdmin(admin.ModelAdmin):
    pass


@admin.register(Galeria)
class GaleriaAdmin(admin.ModelAdmin):
    pass


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    pass


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', "producto_general", 'marca', "codigo", "created_at",)


@admin.register(ProductoGeneral)
class ProductoGeneralAdmin(admin.ModelAdmin):
    list_display = ('id', "codigo", 'marca', "created_at",)


@admin.register(SistemaOperativo)
class SistemaOperativoAdmin(admin.ModelAdmin):
    pass


@admin.register(PrecioVenta)
class PrecioVentaAdmin(admin.ModelAdmin):
    list_display = ("id", "producto_general", "precio", "ruta",)
