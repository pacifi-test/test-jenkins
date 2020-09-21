from uuid import uuid4

from django.db import models
from django.utils.text import slugify

from .marca import Marca
from .producto_general import ProductoGeneral
from ...almacen.constants import ALMACEN


class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    producto_general = models.ForeignKey(ProductoGeneral, blank=True, null=True, verbose_name=u"Producto General")
    codigo_general = models.CharField(u"Código General", max_length=100)
    codigo = models.CharField(u"Código interno", max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=150)
    color = models.CharField(verbose_name=u"Color", max_length=150)
    marca = models.ForeignKey(Marca, verbose_name=u"Marca")
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to="producto", blank=True, null=True)

    created_at = models.DateTimeField(u"Created At", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated At", auto_now=True)

    class Meta:
        verbose_name = u"Producto"
        verbose_name_plural = u"Productos"
        ordering = ("codigo",)

    def __str__(self):
        return "%s" % self.codigo

    def almacenados_codigo(self):
        return len(self.equipo_set.filter(estado=ALMACEN))

    def almacenados_codigo_general(self):
        return len(self.equipo_set.filter(estado=ALMACEN))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.codigo)
        self.codigo = self.codigo.upper()
        self.color = self.color.upper()
        super(Producto, self).save(*args, **kwargs)
