from uuid import uuid4

from django.db import models


class Periodo(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    nombre = models.CharField(u"Nombre", max_length=40)
    estado = models.BooleanField(u"Estado")
    igv = models.DecimalField(u"IGV", max_digits=5, decimal_places=2)
    anio = models.CharField(u"Año", max_length=4)

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

    def __str__(self):
        return self.nombre
