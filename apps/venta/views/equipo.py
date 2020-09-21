import simplejson as json
from decimal import Decimal

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.almacen.constants import ALMACEN
from apps.almacen.models.equipo import Equipo
from apps.almacen.models.salida import Salida
from apps.producto.models.precio_venta import PrecioVenta
from backend_apps.utils.decorators import permission_resource_required


class EquipoGetJson(View):
    u"""Equipos Get
    retorna equipos cargados en almacen a un usuario"""

    # modificar este metodo para realizar la venta directa del almacen

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(EquipoGetJson, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        ruta = self.request.GET.get("ruta")
        estado = self.request.GET.get("estado")
        imei = self.request.GET.get("imei")


        if imei:

            try:
                equipo = Equipo.objects.get(imei=imei, estado=estado)
                try:
                    precio_venta = PrecioVenta.objects.get(producto_general__producto__equipo=equipo, ruta=ruta)
                except Exception as e:
                    data = {
                        "message": e
                    }
                    dump = json.dumps(data)
                    return HttpResponse(dump, status=400, content_type="application/json")

                data = {
                    'imei': equipo.imei,

                    'precio_venta': Decimal(precio_venta.precio),
                    'model': equipo.producto.codigo,

                }
                dump = json.dumps(data)
                return HttpResponse(dump, status=200, content_type="application/json")
            except Exception as e:
                data = {
                    "message": e
                }
                dump = json.dumps(data)
                return HttpResponse(dump, status=400, content_type="application/json")

