from uuid import uuid4

from django.db import models


class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    nombre = models.CharField(u"Nombre", max_length=50)
    descripcion = models.TextField(u"Descripción", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
