from uuid import uuid4

from django.db import models


class SistemaOperativo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(u"Nombre", max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.nombre
