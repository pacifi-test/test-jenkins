from uuid import uuid4

from django.db import models

from apps.persona.models.cliente import Cliente
from apps.producto.constants import RUTA_CHOICES
from backend_apps.backend_auth.models import User

from datetime import datetime


class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    codigo = models.CharField(u"Código", max_length=50)
    ruta = models.CharField(u"ruta", choices=RUTA_CHOICES, max_length=20)
    total = models.DecimalField(u"Total", max_digits=5, decimal_places=2)
    estado = models.BooleanField(u"Estado", default=True)
    cliente = models.ForeignKey(Cliente, verbose_name=u"Cliente")
    distribuidor = models.ForeignKey(User, related_name=u"distribuidor")

    created_at = models.DateTimeField(u"Created at", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated at", auto_now=True)

    class Meta:
        verbose_name = u"Pedido"
        verbose_name_plural = u"Pedidos"
        ordering = ['created_at']


    def __str__(self):
        return self.codigo

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        date = datetime.today().strftime("%Y%m%d")
        count = len(Pedido.objects.all()) + 1
        self.codigo = "%s-%s" % (date, str(count))
        super(Pedido, self).save(force_insert, force_update, using, update_fields)
