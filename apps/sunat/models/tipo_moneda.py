from uuid import uuid4

from django.db import models


class TipoMoneda(models.Model):
    u"""
    Tipo Moneda.

    Tabla 4
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    codigo = models.CharField(u"Código", max_length=10)
    descripcion = models.CharField(u"Descripción", max_length=250)

    class Meta:
        verbose_name = "Tipo Moneda Tabla 4"
        verbose_name_plural = "Tipos Moneda Tabla 4"
        ordering = ["codigo"]

    def __str__(self):
        return "%s %s" % (self.codigo, self.descripcion)
