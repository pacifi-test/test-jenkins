from http.client import HTTPResponse

from django.contrib import messages
from django.db import transaction, IntegrityError
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import BaseUpdateView

from apps.persona.models.cliente import Cliente
from apps.producto.models.precio_venta import PrecioVenta
from apps.producto.models.producto import Producto
from apps.vendedor.models.pedido import Pedido
from apps.vendedor.models.pedido_detalle import PedidoDetalle
from backend_apps.backend_auth.constants import UUIDEncoder
from backend_apps.utils.decorators import permission_resource_required

import simplejson as json

from backend_apps.utils.forms import empty


class PedidoCrearTemplateView(TemplateView):
    template_name = "vendedor/pedido/form.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(PedidoCrearTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PedidoCrearTemplateView, self).get_context_data(**kwargs)
        context['opts'] = Pedido._meta
        context['title'] = "Crear pedido"
        return context

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            json_data = json.loads(request.body)  # request.raw_post_data w/ Django < 1.4
            try:
                with transaction.atomic():
                    cliente = json_data['cliente']
                    productos = json_data['productos']
                    ruta = json_data['ruta']
                    cliente = Cliente.objects.get(nro_documento=cliente['nro_documento'])
                    pedido = Pedido()
                    pedido.cliente = cliente
                    pedido.ruta = ruta
                    pedido.distribuidor = self.request.user
                    pedido.total = 0
                    pedido.save()

                    # cargando productos
                    total = 0
                    for p in productos:
                        producto = Producto.objects.get(codigo=p['producto']['codigo'])
                        pedido_detalle = PedidoDetalle()
                        precio = PrecioVenta.objects.get(ruta=pedido.ruta, producto_general__producto=producto)

                        pedido_detalle.pedido = pedido

                        pedido_detalle.producto = producto
                        pedido_detalle.precio_unitario = precio.precio
                        pedido_detalle.cantidad = int(p['cantidad'])
                        pedido_detalle.total = float(pedido_detalle.cantidad) * float(precio.precio)
                        total = float(total) + float(pedido_detalle.total)
                        pedido_detalle.save()
                    pedido.total = total
                    pedido.save()
            except Exception as e:
                data = {"message": "Error %s" % e}
                dump = json.dumps(data)
                return HttpResponse(dump, status=400, content_type="application/json")
        data = {
            "id": pedido.id
        }
        messages.success(request, "Pedido Ingresado Satisfactoriamente")
        dump = json.dumps(data, cls=UUIDEncoder)
        return HttpResponse(dump, status=200, content_type="application/json")


class PedidoDetailView(DetailView):
    model = Pedido
    template_name = "vendedor/pedido/detail.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(PedidoDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PedidoDetailView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = "Detalles de Pedido"

        return context


class PedidoListView(ListView):
    model = Pedido
    template_name = "vendedor/pedido/list.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(PedidoListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'codigo')
        self.f = empty(self.request, 'f', 'ruta')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}, distribuidor=self.request.user) \
            .order_by('-estado')

    def get_context_data(self, **kwargs):
        context = super(PedidoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'marca'
        context['title'] = ('Seleccione %s para Cambiar') % ('marca')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class PedidoStateUpdate(BaseUpdateView):
    model = Pedido
    success_url = reverse_lazy('vendedor:pedido_list')

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(PedidoStateUpdate, self).dispatch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            d.estado = False
            d.save()
            msg = 'El %(name)s "%(obj)s" fue dado de baja satisfactoriamente.' % {
                'name': self.model._meta.verbose_name,
                'obj': d
            }
            messages.success(self.request, msg)
        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
