from uuid import uuid4

from django.db import models

from apps.producto.constants import RUTA_CHOICES
from backend_apps.backend_auth.models import User
from datetime import datetime

class Salida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    codigo = models.CharField(u"Código", max_length=50)
    # Usuario al que se le hace la salida
    vendedor = models.ForeignKey(User, verbose_name=u"Vendedor")
    estado = models.BooleanField(u"Estado", default=False)  # estado de aceptación del usuario
    ruta = models.CharField(u"Ruta", max_length=15, choices=RUTA_CHOICES)
    arqueado = models.BooleanField(u"Arqueado?", default=False)
    # usuario que hace el registro
    user = models.ForeignKey(User, verbose_name=u"User", related_name=u"user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"Salida"
        verbose_name_plural = u"Salidas"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        date = datetime.today().strftime("%Y%m%d")
        count = len(Salida.objects.all()) + 1
        self.codigo = "%s-%s" % (date, str(count))
        super(Salida, self).save(force_insert, force_update, using, update_fields)
