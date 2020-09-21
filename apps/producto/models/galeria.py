from uuid import uuid4

from django.db import models
from .producto import Producto


class Galeria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    producto = models.ForeignKey(Producto, verbose_name=u"Producto")
    imagen = models.ImageField(upload_to="galería")

    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerias"

    def __str__(self):
        return self.producto.codigo
