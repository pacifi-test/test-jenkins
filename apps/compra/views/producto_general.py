from dal import autocomplete
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.persona.models.proveedor import Proveedor
from apps.producto.models.producto_general import ProductoGeneral
from backend_apps.utils.decorators import permission_resource_required


class ProductoGeneralAutocomplete(autocomplete.Select2QuerySetView):
    paginate_by = 5

    def get_queryset(self):

        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return ProductoGeneral.objects.none()

        qs = ProductoGeneral.objects.all()

        if self.q:
            qs = qs.filter(codigo=self.q)

        return qs
