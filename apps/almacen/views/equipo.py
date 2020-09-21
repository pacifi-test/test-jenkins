from django.contrib import messages
from django.db import transaction, IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import BaseDeleteView

from apps.almacen.models.equipo import Equipo
from apps.compra.models.compra_detalle import CompraDetalle
from backend_apps.backend_auth.constants import SUPERADMIN
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects
from ..constants import ALMACEN

from ..forms.equipo import EquipoUpdateModelForm
from ...producto.models.producto import Producto
import simplejson as json
from django.db import IntegrityError


class EquipoMenuListView(ListView):
    model = Equipo
    template_name = "almacen/equipo/list_menu.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(EquipoMenuListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None

        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'imei')
        self.f = empty(self.request, 'f', 'producto__id')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(EquipoMenuListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = "equipos"
        return context


class EquipoDetailView(DetailView):
    u"""
    Vista para realizar manenimiento de equipo
    """
    model = Equipo
    template_name = "almacen/equipo/detail.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(EquipoDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipoDetailView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = "Equipo"
        return context


class EquipoUpdateView(UpdateView):
    u"""Actualizar equipo"""
    model = Equipo
    form_class = EquipoUpdateModelForm
    template_name = "almacen/equipo/update.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        # buscando si es superadmin
        flag = False

        for g in user.groups.all():

            if g.name == SUPERADMIN:
                flag = True
        if user.is_staff:
            flag = True

        if not flag:
            messages.error(self.request, "Ud. No es administrador")
            return HttpResponseRedirect(reverse("almacen:equipo_list_menu"))
        return super(EquipoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipoUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = "Actualiza Equipo"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        msg = ('La %(name)s "%(obj)s" fue modificado satisfactoriamente.') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }

        messages.success(self.request, msg)
        return super(EquipoUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("almacen:equipo_detail", kwargs={'pk': self.get_object().id})


class EquipoDeleteView(BaseDeleteView):
    u"""Eliminar Equipo"""
    model = Equipo
    success_url = reverse_lazy("almacen:equipo_list_menu")

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        # buscando si es superadmin
        flag = False

        for g in user.groups.all():

            if g.name == SUPERADMIN or user.is_staff == True:
                flag = True
        if user.is_staff:
            flag = True

        if not flag:
            messages.error(self.request, "Ud. No es administrador")
            return HttpResponseRedirect(reverse("almacen:equipo_list_menu"))

        pk = self.kwargs['pk']
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.success_url)
        return super(EquipoDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()

            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request, 'No se Puede eliminar %(name)s' % {
                    "name": self.model._meta.verbose_name
                            + ' "' + (d) + '"'
                })
                raise Exception(msg)

            d.delete()
            msg = 'The %(name)s "%(obj)s" was deleted successfully.' % {
                'name': self.model._meta.verbose_name,
                'obj': d
            }
            if not d.id:
                messages.success(self.request, msg)

        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class EquipoJson(View):
    u"""
    Retorna equipo por imei usado para determinar si el equipo existe en la base de datos
    si manda estado verifica si esta en el estado.
    """

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(EquipoJson, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        imei = self.request.GET.get('imei')
        estado = self.request.GET.get('estado')
        equipo = Equipo.objects.get(imei=imei)
        if estado:
            equipo = Equipo.objects.get(imei=imei, estado=ALMACEN)
        data = {
            'imei': equipo.imei,
            'model': equipo.producto.codigo,
            'marca': equipo.producto.marca.nombre,
            'color': equipo.producto.color,
        }
        dump = json.dumps(data)

        return HttpResponse(dump, content_type="application/json")


class EquiposAddServicioView(View):
    u"""Ingreso directo"""

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(EquiposAddServicioView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        producto = Producto.objects.get(id=data['producto_id'])
        try:
            compra_detalle_id = data['compra_detalle_id']
        except:
            compra_detalle_id = False
        cantidad = 0
        for e in data['equipos']:
            equipo = Equipo()
            equipo.user = self.request.user
            equipo.estado = ALMACEN
            if compra_detalle_id:
                equipo.compra_detalle_id = compra_detalle_id
            equipo.imei = e['imei']
            equipo.producto = producto
            equipo.contable = data['contable']
            equipo.save()
            cantidad = cantidad + 1

        messages.success(self.request, "%s Equipos agregados satisfactoriamente" % cantidad)

        return HttpResponse({"ss": "222", })
