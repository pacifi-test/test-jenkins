from uuid import uuid4

from django.db import models

from apps.persona.models.distrito import Distrito
from apps.sunat.models.tipo_documento_identidad import TipoDocumentoIdentidad
from backend_apps.backend_auth.models import User


class Proveedor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tipo_documento_identidad = models.ForeignKey(TipoDocumentoIdentidad, verbose_name=u"Tipo Documento Identidad")
    nro_documento = models.CharField(u"Número Documento", max_length=50, unique=True)
    razon_social = models.CharField(u"Razón Social", max_length=200)
    nro_telefono = models.CharField(u"Nro. Teléfono", max_length=20, blank=True, null=True)

    lugar = models.ForeignKey(Distrito, verbose_name=u"Lugar", blank=True, null=True)

    direccion = models.CharField(u"Dirección", max_length=250)

    created_at = models.DateTimeField(u"Created At", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated At", auto_now=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return "%s" % (self.razon_social)
