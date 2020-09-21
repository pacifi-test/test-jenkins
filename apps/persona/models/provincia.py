from uuid import uuid4

from django.db import models
from .departamento import Departamento


class Provincia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    departamento = models.ForeignKey(Departamento, verbose_name=u"Departamento")
    nombre = models.CharField(u"Nombre", max_length=150)
    codigo = models.CharField(u"Código", max_length=2)

    class Meta:
        verbose_name = u"Provincia"
        verbose_name_plural = u"Provincias"
        ordering = ('codigo',)

    def __str__(self):
        return "%s" % (self.nombre)
