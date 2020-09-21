from uuid import uuid4

from django.db import models


class CodigoUnidadMedida(models.Model):
    u"""
    Código Unidad Medida.

    Tabla 6
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    codigo = models.CharField(u"Código", max_length=10)
    descripcion = models.CharField(u"Descripción", max_length=250)

    class Meta:
        verbose_name = "Codigo UnidadMedida Tabla Tabla 6"
        verbose_name_plural = "Codigos UnidadMedida Tabla 6"
        ordering = ["codigo"]

    def __str__(self):
        return "%s %s" % (self.codigo, self.descripcion)
