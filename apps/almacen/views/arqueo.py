from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.views.generic.base import View

from apps.almacen.constants import SALIDA
from apps.almacen.models.equipo import Equipo
from apps.almacen.models.salida import Salida
from apps.almacen.models.salida_detalle import SalidaDetalle
from backend_apps.backend_auth.constants import VENTA, DISTRIBUIDOR, ALMACEN
from backend_apps.backend_auth.models import User
from backend_apps.utils.decorators import permission_resource_required


class ArqueoListView(ListView):
    u"""User List para arqueo"""
    model = User
    template_name = "almacen/arqueo/user_list.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ArqueoListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        q = self.model.objects.filter(groups__name=DISTRIBUIDOR)

        return q

    def get_context_data(self, **kwargs):
        context = super(ArqueoListView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['cmi'] = 'Usuarios'
        context['title'] = 'Seleccione %s para agregar equipos' % 'Usuario'
        return context


class ArqueoSalidaListView(ListView):
    u"""Arque de de Equipos"""
    model = Salida
    template_name = "almacen/arqueo/salida_list.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ArqueoSalidaListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        print(self.kwargs['user_pk'])
        vendedor = User.objects.get(id=self.kwargs['user_pk'])
        print(vendedor)
        qs = self.model.objects.filter(arqueado=False, vendedor=vendedor)
        print(qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ArqueoSalidaListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = "Arqueo de Salida"
        return context


class ArqueoSalidaDetailView(DetailView):
    u"""Formulario para reingresar productos al almacen"""
    model = Salida
    pk_url_kwarg = 'salida_pk'
    template_name = "almacen/arqueo/salida_detail.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ArqueoSalidaDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArqueoSalidaDetailView, self).get_context_data(**kwargs)
        detalles = SalidaDetalle.objects.filter(salida=self.get_object()).order_by("equipo__estado")
        context['title'] = "%s" % self.get_object().codigo
        context['opts'] = self.model._meta
        context['detalles'] = detalles
        return context

    def post(self, request, *args, **kwargs):
        imei = self.request.POST.get('imei')
        salida_pk = self.kwargs['salida_pk']

        try:
            salida_detalle = SalidaDetalle.objects.get(salida__id=salida_pk, equipo__imei=imei)
            if salida_detalle.equipo.estado == ALMACEN:
                messages.info(request, "Equipo ya se encuentra en almacen")
                return HttpResponseRedirect(self.get_url_redirect(*args, **kwargs))

        except:
            messages.error(request, "Equipo no se encuentra en esta salida")
            return HttpResponseRedirect(self.get_url_redirect(*args, **kwargs))

        equipo = salida_detalle.equipo

        equipo.estado = ALMACEN
        equipo.save()
        messages.success(self.request, "Equipo Ingresado a almacen")

        return HttpResponseRedirect(self.get_url_redirect(*args, **kwargs))

    def get_url_redirect(self, *args, **kwargs):

        return reverse("almacen:arqueo_salida_detail", kwargs={'salida_pk': self.kwargs['salida_pk']})


class ArqueoSalidaEquipoUpdateView(View):

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ArqueoSalidaEquipoUpdateView, self).dispatch(request, *args, **kwargs)

    def update(self, *args, **kwargs):
        salida_detalle = SalidaDetalle.objects.get(id=self.kwargs['salida_detalle_pk'])
        equipo = salida_detalle.equipo

        equipo.estado = ALMACEN
        equipo.save()
        messages.success(self.request, "Equipo de en almacen")

        return HttpResponseRedirect(self.get_url_redirect(*args, **kwargs))

    def get(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def get_url_redirect(self, *args, **kwargs):
        salida_detalle_id = self.kwargs['salida_detalle_pk']
        salida = Salida.objects.get(salidadetalle__id=salida_detalle_id)

        return reverse("almacen:arqueo_salida_detail", kwargs={'salida_pk': salida.id})


class ArqueoSalidaCerrar(View):

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ArqueoSalidaCerrar, self).dispatch(request, *args, **kwargs)

    def update(self, *args, **kwargs):
        salida = Salida.objects.get(id=self.kwargs['salida_pk'])
        self.vendedor = salida.vendedor

        salida_detalles = SalidaDetalle.objects.filter(salida=salida, equipo__estado=SALIDA)
        if salida_detalles:
            messages.error(self.request, "Tiene Equipos sin areglar")
            return HttpResponseRedirect(reverse("almacen:arqueo_salida_detail", kwargs={"salida_pk": salida.id}))

        else:
            salida.arqueado = True
            messages.success(self.request, "Salida Cerrada")
            salida.save()

        return HttpResponseRedirect(self.get_url_redirect(*args, **kwargs))

    def get(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def get_url_redirect(self, *args, **kwargs):
        return reverse("almacen:arqueo_salida_list", kwargs={'user_pk': self.vendedor.id})
