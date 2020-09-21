from uuid import uuid4

from django.db import models


class Departamento(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    nombre = models.CharField(u"Nombre", max_length=150)
    codigo = models.CharField(u"Código", max_length=2)

    class Meta:
        verbose_name = u"Departamento"
        verbose_name_plural = u"Departamentos"
        ordering = ('codigo',)

    def __str__(self):
        return "%s" % (self.nombre)
