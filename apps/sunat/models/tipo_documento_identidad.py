from uuid import uuid4
from django.db import models


class TipoDocumentoIdentidad(models.Model):
    u"""
    Tipo Documento Identidad.

    Modelo Tabla 2
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    codigo = models.CharField(u"Código", max_length=10)
    descripcion = models.CharField(u"Descripción", max_length=250)

    class Meta:
        verbose_name = "Tipo Documento Identidad Tabla 2"
        verbose_name_plural = "Tipo Documentos Identidads Tabla 2"
        ordering = ["codigo"]

    def __str__(self):
        return "%s %s" % (self.codigo, self.descripcion)
