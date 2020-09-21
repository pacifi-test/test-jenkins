from django.views.generic import ListView

from apps.almacen.models.salida import Salida


class SalidaListView(ListView):
    model = Salida
    template_name = "reporte/salida/list.html"
