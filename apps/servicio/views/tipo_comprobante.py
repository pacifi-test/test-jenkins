from django.core import serializers
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.sunat.models.tipo_comprobante_pago import TipoComprobantePago
from backend_apps.utils.decorators import permission_resource_required


class TipoComprobantesJson(View):
    u"""Lista de comprobantes"""

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(TipoComprobantesJson, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        tipo_comprobantes = TipoComprobantePago.objects.all()
        dump = serializers.serialize('json', tipo_comprobantes)
        return HttpResponse(dump, content_type="application/json")
