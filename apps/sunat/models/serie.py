from uuid import uuid4

from django.db import models

from apps.sunat.models.tipo_comprobante_pago import TipoComprobantePago


class Serie(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    serie = models.CharField(u"Serie", max_length=20)
    numero_maximo = models.IntegerField(u"Número Máximo")
    estado = models.BooleanField(u"Estado", default=True)
    tipo_comprobante = models.ForeignKey(TipoComprobantePago, verbose_name=u"Tipo Comprobante")

    class Meta:
        verbose_name_plural = u"Series"
        verbose_name = u"Serie"

    def __str__(self):
        return "%s %s %s" % (self.tipo_comprobante.codigo, self.serie, self.numero_maximo)
