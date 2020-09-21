import simplejson as json
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.producto.models.producto import Producto
from backend_apps.utils.decorators import permission_resource_required


class ProductoListGetView(View):
    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoListGetView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        producto_general_codigo = self.request.GET.get("producto_general_codigo")
        if producto_general_codigo:
            productos = Producto.objects.filter(producto_general__codigo=producto_general_codigo)
            data = []
            for p in productos:
                data.append({
                    "codigo": p.codigo,
                    "codigo_general": p.codigo_general,
                    "marca": p.producto_general.marca.nombre
                }
                )
            dump = json.dumps(data)
            return HttpResponse(dump, status=200, content_type="application/json")
        productos = Producto.objects.all()
        data = []
        for p in productos:
            data.append({
                "codigo": p.codigo,
                "codigo_general": p.codigo_general,
                "marca": p.producto_general.marca
            }
            )
        dump = json.dumps(data)
        return HttpResponse(dump, status=200, content_type="application/json")
