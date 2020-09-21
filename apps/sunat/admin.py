from django.contrib import admin

from .models.codigo_aduana import CodigoAduana
from .models.codigo_unidad_medida import CodigoUnidadMedida
from .models.igv import Igv
from .models.periodo import Periodo
from .models.serie import Serie
from .models.tipo_comprobante_pago import TipoComprobantePago
from .models.tipo_documento_identidad import TipoDocumentoIdentidad
from .models.tipo_moneda import TipoMoneda


@admin.register(CodigoAduana)
class CodigoAduanaAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "descripcion"]


@admin.register(CodigoUnidadMedida)
class CodigoUnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "descripcion"]


@admin.register(Igv)
class IgvAdmin(admin.ModelAdmin):
    pass


@admin.register(TipoComprobantePago)
class TipoComprobantePagoAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "descripcion"]


@admin.register(TipoDocumentoIdentidad)
class TipoDocumentoIdentidadAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "descripcion"]


@admin.register(TipoMoneda)
class TipoMonedaAdmin(admin.ModelAdmin):
    list_display = ["id", "codigo", "descripcion"]


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('id', 'serie', 'numero_maximo', 'estado', 'tipo_comprobante',)


@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    pass
