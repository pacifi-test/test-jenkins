from uuid import uuid4

from django.db import models


class TipoComprobantePago(models.Model):
    u"""
    Tipo Comprobante Pago.

    Tabla 10
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    codigo = models.CharField(u"Código", max_length=10)
    descripcion = models.CharField(u"Descripción", max_length=250)

    class Meta:
        verbose_name = "Tipo Comprobante Pago Tabla 10"
        verbose_name_plural = "Tipo Comprobante Pagos Tabla 10"
        ordering = ["codigo"]

    def __str__(self):
        return "%s %s" % (self.codigo, self.descripcion)
