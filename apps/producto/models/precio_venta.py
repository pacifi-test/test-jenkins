from uuid import uuid4

from django.db import models

from apps.producto.models.producto import Producto
from backend_apps.backend_auth.models import User
from .producto_general import ProductoGeneral
from ..constants import RUTA_CHOICES


class PrecioVenta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    producto_general = models.ForeignKey(ProductoGeneral, verbose_name=u"Producto General", blank=True, null=True)
    ruta = models.CharField(u"Precio Ruta", max_length=15, choices=RUTA_CHOICES)

    estado = models.BooleanField(u"Estado", default=True)
    precio = models.DecimalField(u"Precio Local", max_digits=5, decimal_places=2)

    created_at = models.DateTimeField(u"Created At", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated at", auto_now=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = u"Precio de Venta"
        verbose_name_plural = u"Precios de Venta"
