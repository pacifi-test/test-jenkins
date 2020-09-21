from uuid import uuid4

from django.db import models


class CodigoAduana(models.Model):
    u"""
    Codigo Aduana.

    Tabla 11
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    codigo = models.CharField(u"Código", max_length=10)
    descripcion = models.CharField(u"Descripción", max_length=250)

    class Meta:
        verbose_name = u"Código Aduana Tabla 11"
        verbose_name_plural = "Codigos de Aduana Tabla 11"
        ordering = ["codigo"]

    def __str__(self):
        return "%s %s" % (self.codigo, self.descripcion)
