from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import BaseUpdateView

from apps.almacen.models.equipo import Equipo
from apps.compra.models.compra import Compra
from apps.compra.models.compra_detalle import CompraDetalle
from backend_apps.utils.decorators import permission_resource_required


class ComprobanteListView(ListView):
    u"""
    Lista de compras para almacen

    :url: /almacen/compra/listar
    :definicion: Lista las compras que aun no estan ingresadas a almacen
    """
    model = Compra
    template_name = "almacen/compra/list.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ComprobanteListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Compra.objects.filter(estado=False, procesado=True)
        for q in queryset:
            equipos = Equipo.objects.filter(compra_detalle__compra=q)
            cantidades = CompraDetalle.objects.filter(compra=q).aggregate(Sum('cantidad'))

            if cantidades['cantidad__sum'] == len(equipos):
                q.completado = True

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ComprobanteListView, self).get_context_data(**kwargs)
        # verificar si ya esta ingresado

        context['opts'] = self.model._meta
        context['cmi'] = 'compra'
        context['title'] = ('Seleccione %s para Cambiar') % ('compra')
        return context


class CompraDetailView(DetailView):
    model = Compra
    template_name = "almacen/compra/detail.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompraDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CompraDetailView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['cmi'] = 'compra detalle'
        context['title'] = "Agregar Compra Detalle"
        return context


class ComprobanteEstadoUpdateView(BaseUpdateView):
    """Acutaliza el estado de la compra para que ya este verificador completamente"""
    model = Compra
    fields = ['', ]
    success_url = reverse_lazy("almacen:compra_list")

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ComprobanteEstadoUpdateView, self).dispatch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Acutaliza el estado de la compra para que ya este verificador completamente"""
        # validamos que todos los detalles esten completados
        comprobate = self.get_object()
        flag = True
        comprobate_detalles = CompraDetalle.objects.filter(compra=comprobate)
        for com_det in comprobate_detalles:
            if len(com_det.equipo_set.all()) != com_det.cantidad:
                flag = False

        if not flag:
            messages.error(request, "Aun no se completan los equipos")
            return HttpResponseRedirect(reverse("almacen:compra_detail", kwargs={'pk': comprobate.id}))
        comprobate.estado = True
        comprobate.save()
        messages.success(request, "Comprobaten totalmente ingresado")

        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
