from uuid import uuid4
from django.db import models

from apps.producto.models.producto import Producto
from apps.sunat.models.igv import Igv
from backend_apps.backend_auth.models import User
from .compra import Compra
from ...producto.models.producto_general import ProductoGeneral


class CompraDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    compra = models.ForeignKey(Compra, verbose_name=u"Compra")

    producto_general = models.ForeignKey(ProductoGeneral, verbose_name=u"Producto General", blank=True, null=True)
    cantidad = models.IntegerField(u"canidad")
    # monto del igv en procentaje actual esto va escondido
    igv = models.DecimalField(u"IGV", max_digits=5, decimal_places=2)
    valor_unitario = models.DecimalField(u"Valor Unitario", max_digits=5, decimal_places=2)

    precio_unitario = models.DecimalField(u"Precio Unitario", max_digits=5, decimal_places=2)

    igv_total = models.DecimalField(u"IGV", max_digits=5, decimal_places=2)
    precio_total = models.DecimalField(u"P. Total", max_digits=9, decimal_places=2)
    total = models.DecimalField(u"Total", max_digits=6, decimal_places=2)

    created_at = models.DateTimeField(u"Created at", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated at", auto_now=True)
    user = models.ForeignKey(User, verbose_name=u"User")

    class Meta:
        verbose_name = u"Compra Detalle"
        verbose_name_plural = u"Compra Detalles"
        ordering = ("created_at",)

    def __str__(self):
        return "%s %s" % (self.producto_general, self.total)
