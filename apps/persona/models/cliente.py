from uuid import uuid4
from django.db import models

from apps.persona.models.distrito import Distrito
from apps.sunat.models.tipo_documento_identidad import TipoDocumentoIdentidad

from backend_apps.backend_auth.models import User


class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombres = models.CharField(u"Nombres", max_length=250)
    apellidos = models.CharField(u"Apellidos", max_length=250, blank=True, null=True)
    nro_telefono = models.CharField(u"Nro. Teléfono", max_length=20, blank=True, null=True)
    tipo_documento = models.ForeignKey(TipoDocumentoIdentidad, verbose_name=u"Tipo Documento")
    nro_documento = models.CharField(u"Nro. Documento", max_length=15, unique=True)
    correo_electronico = models.EmailField(u"Correo E.", max_length=150, blank=True, null=True)
    direccion = models.CharField(u"Dirección", max_length=250)
    lugar = models.ForeignKey(Distrito, verbose_name=u"Lugar", blank=True, null=True)

    es_juridico = models.BooleanField(u"Es Jurídico", default=False)

    created_at = models.DateTimeField(u"Created At", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated At", auto_now=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = u"Cliente"
        verbose_name_plural = u"Clientes"

    def __str__(self):
        return "%s %s" % (self.nombres, self.nro_documento)

    def nombre_completo(self):
        nombres = self.nombres
        apellidos = self.apellidos if self.apellidos else ""
        return "%s %s" % (nombres, apellidos)
