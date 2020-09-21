from uuid import uuid4
from django.db import models


class Igv(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    estado = models.BooleanField(default=True)
    monto = models.IntegerField(u"Monto")
    periodo = models.CharField(u"Periodo", max_length=4)

    class Meta:
        verbose_name = "Igv"
        verbose_name_plural = "Igvs"

    def __str__(self):
        return self.periodo
