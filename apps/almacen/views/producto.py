from http.client import HTTPResponse

from django.db import models
from django.db.models import Count, Q
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from apps.almacen.constants import ALMACEN, VENDIDO, SALIDA
from apps.almacen.models.equipo import Equipo
from apps.producto.models.producto import Producto
from backend_apps.utils.decorators import permission_resource_required
import simplejson as json


class ProductoListView(ListView):
    model = Producto
    template_name = "almacen/producto/list.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        agrupar = self.request.GET.get("agrupar")
        query = self.model.objects.all()
        if agrupar:
            q = """
            select 'af415e59-2185-4e5b-85a6-b23544355bdf' as id,
       producto_producto.codigo_general,
       count(almacen_equipo.id)               as cantidad_almacen,
       pm.nombre                              as marca_nombre
from producto_producto,
     almacen_equipo,
     producto_marca pm
where almacen_equipo.producto_id = producto_producto.id
  and almacen_equipo.estado = 'ALMACEN'
  and pm.id = producto_producto.marca_id
group by producto_producto.codigo_general, pm.nombre
            """
            query = Producto.objects.raw(q)
        else:
            query = self.model.objects.all()
        return query

    def get_context_data(self, **kwargs):
        context = super(ProductoListView, self).get_context_data(**kwargs)
        context['title'] = "productos"
        context['opts'] = self.model._meta
        return context


class ProductoDetailView(DetailView):
    u"""
    Vista para agregar productos directamente
    """
    model = Producto
    template_name = "almacen/producto/detail.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductoDetailView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta

        context['title'] = "Producto"
        return context


class ProductoDetailCountAlmacenServiceView(View):

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoDetailCountAlmacenServiceView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        producto = Producto.objects.get(id=self.kwargs["pk"])
        almacen = Equipo.objects.filter(producto=producto, estado=ALMACEN)
        vendidos = Equipo.objects.filter(producto=producto, estado=VENDIDO)
        salida = Equipo.objects.filter(producto=producto, estado=SALIDA)

        data = {
            'almacen': len(almacen),
            'vendidos': len(vendidos),
            'salida': len(salida),

        }
        dump = json.dumps(data)

        return HttpResponse(dump, content_type="application/json")
