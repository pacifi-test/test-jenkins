from django.forms import ModelForm

from apps.almacen.models.salida import Salida


class SalidaModelForm(ModelForm):
    class Meta:
        model = Salida
        exclude = ("created_at", "updated_at", "vendedor", "user", "estado", "ruta", "arqueado",)
