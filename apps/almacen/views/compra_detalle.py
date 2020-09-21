import simplejson as json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView

from apps.almacen.models.equipo import Equipo
from apps.compra.models.compra_detalle import CompraDetalle
from apps.producto.models.producto import Producto
from backend_apps.utils.decorators import permission_resource_required


class CompraDetalleDetailView(DetailView):
    template_name = "almacen/compra_detalle/detail.html"
    model = CompraDetalle

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(CompraDetalleDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CompraDetalleDetailView, self).get_context_data(**kwargs)
        producto = Producto.objects.get(id=self.kwargs['producto_pk'])

        context['producto'] = producto
        context['opts'] = self.model._meta
        context['title'] = "Producto"
        return context


class CompraDetalleServiceView(DetailView):
    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(CompraDetalleServiceView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        compra_detalle_id = self.request.GET.get("compra_detalle_id")
        compra_detalle = CompraDetalle.objects.get(id=compra_detalle_id)
        equipos = Equipo.objects.filter(compra_detalle=compra_detalle)
        equipos_dic = []
        for equipo in equipos:
            equipos_dic.append({
                "producto_codigo": equipo.producto.codigo,
                "imei": equipo.imei
            })
        registrados = len(equipos)

        data = {
            "registrados": registrados,
            "equipos": equipos_dic,
            "cantidad": compra_detalle.cantidad,
            "contable": compra_detalle.compra.contable

        }

        dump = json.dumps(data)
        print(dump)

        return HttpResponse(dump, status=200, content_type="application/json")
