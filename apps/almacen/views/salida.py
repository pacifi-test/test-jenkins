from django.contrib import messages
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView

from backend_apps.backend_auth.constants import DISTRIBUIDOR, ALMACEN, UUIDEncoder
from backend_apps.backend_auth.models import User
from backend_apps.utils.decorators import permission_resource_required
from ..constants import SALIDA
from ..models.equipo import Equipo
from ..models.salida import Salida
from ..models.salida_detalle import SalidaDetalle
from ...producto.constants import RUTA_CHOICES

import simplejson as json


class SalidaListView(ListView):
    model = Salida

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(SalidaListView, self).dispatch(request, *args, **kwargs)


class SalidaCreateTemplateView(TemplateView):
    model = Salida
    template_name = "almacen/salida/form.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(SalidaCreateTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SalidaCreateTemplateView, self).get_context_data(**kwargs)
        distribuidores = User.objects.filter(groups__name=DISTRIBUIDOR)
        rutas = RUTA_CHOICES
        print(distribuidores)
        context['title'] = 'Salida de Productos'
        context['opts'] = self.model._meta
        context['distribuidores'] = distribuidores
        context['rutas'] = rutas

        return context

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                user = self.request.user
                username = data['distribuidor']
                ruta = data['ruta']
                distribuidor = User.objects.get(username=username)
                salida = Salida()
                salida.vendedor = distribuidor
                salida.ruta = ruta
                salida.user = user
                salida.save()

                # cargando detalles
                for e in data['equipos']:
                    sd = SalidaDetalle()
                    sd.salida = salida
                    equipo = Equipo.objects.get(imei=e['imei'])
                    sd.equipo = equipo
                    sd.save()
                    equipo.estado = SALIDA
                    equipo.save()

                salida_data = {
                    'id': salida.id,
                }
                dump = json.dumps(salida_data, cls=UUIDEncoder)

                return HttpResponse(dump, content_type="application/json", status=201)

        except IntegrityError as e:
            print("error", e)


class SalidaDetailView(DetailView):
    u"""Metodo para imprimir la salida"""
    model = Salida
    template_name = "almacen/salida/detail.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(SalidaDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SalidaDetailView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = "salida"
        return context
