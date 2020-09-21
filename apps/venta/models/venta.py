from uuid import uuid4

from django.db import models

from apps.persona.models.cliente import Cliente
from apps.sunat.models.periodo import Periodo
from apps.sunat.models.serie import Serie
from apps.sunat.models.tipo_comprobante_pago import TipoComprobantePago
from backend_apps.backend_auth.models import User


class Venta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    periodo = models.ForeignKey(Periodo, verbose_name=u"Periodo")
    serie = models.ForeignKey(Serie, verbose_name=u"Serie")
    nro_correlativo = models.IntegerField(blank=True, null=True)
    distribuidor = models.ForeignKey(User, related_name="distruibuidor", verbose_name=u"Distribuidor", blank=True,
                                     null=True)
    contado = models.BooleanField(u"Libre", default=True)
    tipo_comprobante = models.ForeignKey(TipoComprobantePago, verbose_name=u"Tipo Comprobante")
    cliente = models.ForeignKey(Cliente, verbose_name=u"Cliente")

    estado = models.BooleanField(u"Estado", default=False)  # si ya se realizo la venta
    arqueado = models.BooleanField(u"Arquedo", default=False)

    igv = models.DecimalField(u"IGV", max_digits=9, decimal_places=2)
    base_imponible = models.DecimalField(u"Base Imponible", max_digits=9, decimal_places=2)
    total = models.DecimalField(u"Total", max_digits=9, decimal_places=2)

    user = models.ForeignKey(User, verbose_name=u"user")
    created_at = models.DateTimeField(u"Created At", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated At", auto_now=True)

    electronico = models.BooleanField(u"Facturado Electronicamente", default=False)

    monto_texto = models.CharField(u"Monto Texto", max_length=200, blank=True, null=True)

    qr = models.CharField(u"qr", max_length=150, blank=True, null=True)
    xml_ruta = models.CharField(u"xml ruta", max_length=150, blank=True, null=True)
    cdr_ruta = models.CharField(u"cdr ruta", max_length=150, blank=True, null=True)
    hash = models.CharField(u"Hash", max_length=150, blank=True, null=True)
    hash_cdr = models.CharField(u"Hash", max_length=150, blank=True, null=True)
    nota_motivo = models.CharField(u"Nota Motivo", max_length=150, blank=True, null=True)
    nota_codigo = models.CharField(u"Nota Codigo", max_length=50, blank=True,
                                   null=True)  # codigo por el que se esta creando la nota
    fecha_envio_sunat = models.CharField(u"Nota Codigo", max_length=50, blank=True,
                                         null=True)  # codigo por el que se esta creando la nota
    codigo_sunat = models.CharField(u"codigo sunat", max_length=20, blank=True, null=True)
    mensaje_sunat = models.CharField(u"codigo sunat", max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = u"Venta"
        verbose_name_plural = u"Ventas"

    def __str__(self):
        return "%s" % (self.nro_correlativo)

    def fecha_local(self):
        from django.utils import timezone
        return timezone.localtime(self.created_at)

    def serie_numero(self):
        return "%s-%s" % (self.serie.serie, self.nro_correlativo)
