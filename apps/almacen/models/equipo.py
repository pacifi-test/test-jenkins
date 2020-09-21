from uuid import uuid4

from django.db import models

from apps.compra.models.compra_detalle import CompraDetalle
from apps.producto.models.producto import Producto
from backend_apps.backend_auth.models import User

from ..constants import ESTADO_EQUIPO_CHOICES, ALMACEN


class Equipo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    compra_detalle = models.ForeignKey(CompraDetalle, verbose_name=u"Compra Detalle", blank=True, null=True)
    imei = models.CharField(u"Imei", max_length=150, unique=True)
    producto = models.ForeignKey(Producto, verbose_name="Producto")
    estado = models.CharField(u"Estado", choices=ESTADO_EQUIPO_CHOICES, default=ALMACEN, max_length=15)
    contable = models.BooleanField(u"Contable", default=True)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(u"Created At", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated At", auto_now=True)

    class Meta:
        verbose_name = u"Equipo"
        verbose_name_plural = u"Equipos"

    def __str__(self):
        return "%s %s" % (self.producto, self.imei)
