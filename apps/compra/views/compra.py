from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.base import View

from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty

from ..forms.compra import CompraForm, CompraUpdateForm

from ..models.compra import Compra
from ..models.compra_detalle import CompraDetalle
from ...sunat.models.periodo import Periodo


class CompraCreateView(CreateView):
    u"""Compra Formulario"""
    model = Compra
    form_class = CompraForm
    template_name = "compra/compra/form.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompraCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CompraCreateView, self).get_context_data(**kwargs)
        periodo = Periodo.objects.get(estado=True)
        context['opts'] = self.model._meta
        context['cmi'] = 'menu'
        context['title'] = "Crear Compra"
        context['periodo'] = periodo
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.periodo = Periodo.objects.get(estado=True)
        if self.object.tipo_comprobante.codigo == 99:
            self.object.contable = False
        else:
            self.object.contable = True
        msg = "Proceso de Compra Iniciado"
        messages.success(self.request, msg)
        return super(CompraCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('compra:compra_detail', kwargs={'pk': self.object.id})


class CompraPendienteListView(ListView):
    model = Compra
    template_name = "compra/compra/slopes.html"
    paginate_by = 10

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompraPendienteListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'nro_correlativo')
        self.f = empty(self.request, 'f', 'nro_comprobante')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}, procesado=False).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(CompraPendienteListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'compra'
        context['title'] = ('Seleccione %s para Cambiar') % ('compra')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class CompraListView(ListView):
    model = Compra
    template_name = "compra/compra/list.html"
    paginate_by = 10

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompraListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'nro_correlativo')
        self.f = empty(self.request, 'f', 'nro_comprobante')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}, procesado=True).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(CompraListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'compra'
        context['title'] = ('Seleccione %s para Cambiar') % ('compra')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class CompraDetailView(DetailView):
    model = Compra
    template_name = "compra/compra/detail.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompraDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CompraDetailView, self).get_context_data(**kwargs)
        procesador = False
        total_compra = self.object.total
        total_detalle = CompraDetalle.objects.filter(compra__id=self.object.id).aggregate(Sum('total'))
        if total_compra == total_detalle['total__sum']:  # valida que las cantidades sean iguales y se pueda procesar
            procesador = True

        context['procesador'] = procesador
        context['opts'] = self.model._meta
        context['cmi'] = 'compra detalle'
        context['title'] = "Agregar Compra Detalle"
        return context


class CompraUpdateView(UpdateView):
    model = Compra
    form_class = CompraUpdateForm
    template_name = "compra/compra/form_update.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompraUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CompraUpdateView, self).get_form_kwargs()
        kwargs['url'] = reverse("compra:compra_update", kwargs={'pk': self.object.id})
        kwargs['compra'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CompraUpdateView, self).get_context_data(**kwargs)

        context['periodo'] = Periodo.objects.get(estado=True)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        msg = "Compra Actualizada"
        if self.object.tipo_comprobante.codigo == 99:
            self.object.contable = False
        else:
            self.object.contable = True
        messages.success(self.request, msg)
        return super(CompraUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('compra:compra_detail', kwargs={'pk': self.object.id})


class CompraProcesarView(View):
    model = Compra

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        if not pk:
            return HttpResponseRedirect(self.get_success_url())
        try:
            self.object = self.model.objects.get(pk=pk)
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.get_success_url())

        msg = ('The %(name)s "%(obj)s" is already %(action)s.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': "Compra Procesada"
        }

        self.object.procesado = True
        compra = Compra.objects.latest('nro_correlativo')

        if compra.nro_correlativo is None:
            self.object.nro_correlativo = str(1)

        else:
            self.object.nro_correlativo = str(int(compra.nro_correlativo) + 1)

        self.object.save()
        messages.success(self.request, msg)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        compra_pk = self.kwargs['pk']
        return reverse('compra:compra_detail', kwargs={'pk': compra_pk})
