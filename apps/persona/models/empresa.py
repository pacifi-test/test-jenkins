from uuid import uuid4

from django.db import models


class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(u"Nombre Empresa", max_length=200)
    nro_telefono = models.CharField(u"Nro. Teléfono", max_length=20, blank=True, null=True)
    direccion = models.CharField(u"Dirección", max_length=200)
    nro_ruc = models.CharField(u"Número de Ruc", max_length=11)
    nombre_moneda = models.CharField(u"Nombre Moneda", max_length=150)
    simbolo_moneda = models.CharField(u"Simbolo Empresa", max_length=150)
    estado = models.BooleanField(u"Estado", default=True)

    def __str__(self):
        return self.nombre
