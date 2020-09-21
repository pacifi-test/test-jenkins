from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.almacen.constants import ALMACEN
from apps.producto.models.precio_venta import PrecioVenta
from apps.producto.models.producto import Producto
from apps.vendedor.models.pedido import Pedido
from apps.vendedor.models.pedido_detalle import PedidoDetalle
from backend_apps.utils.decorators import permission_resource_required
import simplejson as json


class ProductoView(View):
    u"""Buscar Producto para auto complete"""

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        codigo = self.request.GET.get("producto_codigo")
        ruta = self.request.GET.get("ruta")

        if codigo:
            try:
                producto = Producto.objects.get(codigo=codigo)
            except:
                data = json.dumps({"message": "El producto no existe"})
                return HttpResponse(data, status=400, content_type="application/json")
            try:
                precio = PrecioVenta.objects.get(producto_general=producto.producto_general, ruta=ruta)
            except:
                data = json.dumps({"message": "El producto no tiene precio asignado en esta ruta"})
                return HttpResponse(data, status=400, content_type="application/json")

            reserva = PedidoDetalle.objects.filter(pedido__estado=True, producto=producto).aggregate(Sum('cantidad'))
            print(reserva)

            data = {
                "codigo": producto.codigo,
                "marca": producto.marca.nombre,
                "color": producto.color,
                "cantidad": producto.equipo_set.filter(estado=ALMACEN).count(),
                "precio": precio.precio,
                "reserva": reserva['cantidad__sum'] if reserva['cantidad__sum'] else 0,

            }
            dump = json.dumps(data)

            return HttpResponse(dump, status=200, content_type="application/json")

        productos = Producto.objects.all()
        data = []
        for producto in productos:
            data.append(
                {
                    'codigo': producto.codigo,

                    'color': producto.color,
                    'cantidad': producto.equipo_set.filter(estado=ALMACEN).count()
                }
                # producto.codigo
            )

        dump = json.dumps(data)
        print(dump)
        return HttpResponse(dump, status=200, content_type="application/json")
