from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.views.generic.edit import BaseDeleteView

from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects

from ..models.proveedor import Proveedor

from ..forms.proveedor import ProveedorForm


class ProveedorListView(ListView):
    model = Proveedor
    paginate_by = settings.PER_PAGE
    template_name = "persona/proveedor/list.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProveedorListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'razon_social')
        self.f = empty(self.request, 'f', 'nro_documento')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(ProveedorListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'proveedor'
        context['title'] = ('Seleccione %s para Cambiar') % ('proveedor')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "persona/proveedor/form.html"
    success_url = reverse_lazy('persona:proveedor_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProveedorCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProveedorCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'proveedor'
        context['title'] = "Crear proveedor"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        msg = ('La %(name)s "%(obj)s" fue agregada satisfactoriamente.') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }

        messages.success(self.request, msg)
        return super(ProveedorCreateView, self).form_valid(form)


class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "persona/proveedor/form.html"
    success_url = reverse_lazy('persona:proveedor_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProveedorUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProveedorUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'proveedor'
        context['title'] = 'cambiar %s' % 'proveedor'
        return context

    def get_initial(self):
        initial = super(ProveedorUpdateView, self).get_initial()
        initial = initial.copy()
        d = self.object
        if d.lugar:
            initial['provincia'] = d.lugar.provincia
            initial['departamento'] = d.lugar.provincia.departamento

        return initial

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = 'The %(name)s "%(obj)s" fue cambiado satisfactoriamente.' % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)

        return super(ProveedorUpdateView, self).form_valid(form)


class ProveedorDeleteView(BaseDeleteView):
    model = Proveedor
    success_url = reverse_lazy('persona:proveedor_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.success_url)
        return super(ProveedorDeleteView, self).dispatch(request, *args, **kwargs)

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
