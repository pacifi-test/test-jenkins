from uuid import uuid4

from django.db import models

from apps.almacen.models.equipo import Equipo
from apps.venta.models.venta import Venta


class VentaDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    venta = models.ForeignKey(Venta, verbose_name=u"Venta")
    equipo = models.ForeignKey(Equipo, verbose_name=u"Equipo")

    cantidad = models.IntegerField(u"Cantidad")
    precio_unitario = models.DecimalField(u"Precio Unitario", max_digits=5, decimal_places=2)
    valor_unitario = models.DecimalField(u"Valor Unitario", max_digits=5, decimal_places=2)

    precio_total = models.DecimalField(u"Precio Total", max_digits=5, decimal_places=2)
    base_imponible = models.DecimalField(u"Base Imponible", max_digits=5, decimal_places=2)
    igv = models.DecimalField(u"IGV", max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = u"Venta Detalle"
        verbose_name_plural = u"Venta Detalles"

    def __str__(self):
        return "%s %s" % (self.venta.nro_correlativo, self.equipo.imei)
