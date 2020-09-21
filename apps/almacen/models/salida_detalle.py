from uuid import uuid4

from django.db import models

from .salida import Salida
from .equipo import Equipo


class SalidaDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    regresado = models.BooleanField(default=False)
    salida = models.ForeignKey(Salida, verbose_name=u"Salida")
    equipo = models.ForeignKey(Equipo, verbose_name=u"Equipo")

    class Meta:
        verbose_name = u"Salida Detalle"
        verbose_name_plural = u"Salida Detalle"
        ordering = ('equipo__producto',)
