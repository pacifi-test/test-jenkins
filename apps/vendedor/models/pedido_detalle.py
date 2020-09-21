from uuid import uuid4

from django.db import models

from .pedido import Pedido
from ...producto.models.producto import Producto


class PedidoDetalle(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    pedido = models.ForeignKey(Pedido, verbose_name=u"Pedido")
    producto = models.ForeignKey(Producto)
    precio_unitario = models.DecimalField(u"Precio Unitario", max_digits=5, decimal_places=2)
    cantidad = models.IntegerField(u"Cantidad", blank=True, null=True)
    total = models.DecimalField(u"Total", max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = u"Pedido Detalle"
        verbose_name_plural = u"Pedido Detalles"

    def __str__(self):
        return "%s %s" % (self.pedido.codigo, self.producto.codigo)
