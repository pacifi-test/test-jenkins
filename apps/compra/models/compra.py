from uuid import uuid4

from django.db import models

from apps.persona.models.proveedor import Proveedor
from apps.sunat.models.codigo_aduana import CodigoAduana
from apps.sunat.models.periodo import Periodo
from apps.sunat.models.tipo_comprobante_pago import TipoComprobantePago
from apps.sunat.models.tipo_moneda import TipoMoneda
from backend_apps.backend_auth.models import User


class Compra(models.Model):
    u"""
    Comprobante.

    Tabla 8.1 Registro de Compras.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    codigo_aduana = models.ForeignKey(CodigoAduana, verbose_name=u"Código Aduana", blank=True, null=True)
    tipo_comprobante = models.ForeignKey(TipoComprobantePago, verbose_name=u"Tipo Comprobante")
    tipo_moneda = models.ForeignKey(TipoMoneda, verbose_name=u"Tipo Moneda")
    proveedor = models.ForeignKey(Proveedor, verbose_name=u"Proveedor")
    # Verifica que el proceso de compra este cerrado por completo
    procesado = models.BooleanField(u"Procesado", default=False)
    # Verifica que ya este en agregado al almacen
    estado = models.BooleanField(u"Estado", default=False)
    contable = models.BooleanField(u"Contable", default=True)
    fecha_emision = models.DateField(u"Fecha de emisión")
    fecha_vencimiento = models.DateField(u"Fecha Vencimiento")
    periodo = models.ForeignKey(Periodo, verbose_name=u"Periodo")

    base_imponible = models.DecimalField(u"Base Imponible", max_digits=9, decimal_places=2, blank=True, null=True)
    igv = models.DecimalField(u"IGV", max_digits=9, decimal_places=2)
    total = models.DecimalField(u"Total", max_digits=9, decimal_places=2)
    serie_comprobante = models.CharField(u"Serie", max_length=30)
    nro_comprobante = models.CharField(u"Número Comprobante", max_length=30)
    nro_correlativo = models.CharField(u"Número Correlativo", max_length=20, blank=True, null=True)  # Número correlativo

    created_at = models.DateTimeField(u"Created At", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated At", auto_now=True)
    user = models.ForeignKey(User, verbose_name=u"User")

    class Meta:
        verbose_name = u"Compra"
        verbose_name_plural = u"Compras"
        ordering = ("-nro_correlativo",)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Compra, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return "%s %s" % (self.nro_correlativo, self.proveedor.razon_social)
