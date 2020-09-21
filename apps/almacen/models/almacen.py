from uuid import uuid4

from django.db import models

from apps.almacen.models.equipo import Equipo
from backend_apps.backend_auth.models import User


class Almacen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    equipo = models.ForeignKey(Equipo)

    usuario = models.ForeignKey(User)

    created_at = models.DateTimeField(u"Created At", auto_now_add=True)
    updated_at = models.DateTimeField(u"Updated At", auto_now=True)

    def __str__(self):
        return self.equipo
