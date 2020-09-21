from uuid import uuid4

from django.db import models

from .provincia import Provincia


class Distrito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    provincia = models.ForeignKey(Provincia, verbose_name=u"Provincia")
    nombre = models.CharField(u"Nombre", max_length=150)
    codigo = models.CharField(u"Código", max_length=2)

    class Meta:
        verbose_name = u"Distrito"
        verbose_name_plural = u"Distritos"
        ordering = ('codigo',)

    def __str__(self):
        return "%s" % (self.nombre)

    def ubigeo(self):
        return "%s%s%s"%(self.provincia.departamento.codigo,self.provincia.codigo,self.codigo)
