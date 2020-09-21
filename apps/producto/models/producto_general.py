from uuid import uuid4

from django.db import models
from django.utils.text import slugify

from apps.producto.models.marca import Marca


class ProductoGeneral(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    codigo = models.CharField(u"Código", max_length=50, blank=True, null=True, unique=True)
    slug = models.SlugField(unique=True, max_length=70)
    marca = models.ForeignKey(Marca, verbose_name=u"Marca")
    descripcion = models.TextField(u"Descripción", blank=True, null=True)
    imagen = models.ImageField(upload_to="producto_general", blank=True, null=True)

    created_at = models.DateTimeField(u"Created At", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated At", auto_now=True)

    class Meta:
        verbose_name = u"Producto General"
        verbose_name_plural = u"Productos Generales"

    def __str__(self):
        return self.codigo

    def save(self, *args, **kwargs):
        self.codigo = self.codigo.upper()
        self.slug = slugify(self.codigo)
        super(ProductoGeneral, self).save(*args, **kwargs)
