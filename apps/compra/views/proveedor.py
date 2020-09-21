from dal import autocomplete
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.persona.models.proveedor import Proveedor
from backend_apps.utils.decorators import permission_resource_required


class ProveedorTemplateView(TemplateView):
    template_name = "compra/proveedor/view.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProveedorTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProveedorTemplateView, self).get_context_data(**kwargs)
        num_doc = self.request.GET.get("nro_doc")
        try:

            proveedor = Proveedor.objects.get(numero_documento=num_doc)
        except:
            proveedor = None

        context['proveedor'] = proveedor
        return context


class ProveedorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Proveedor.objects.none()

        qs = Proveedor.objects.all()

        if self.q:
            qs = qs.filter(razon_social__istartswith=self.q)

        return qs
