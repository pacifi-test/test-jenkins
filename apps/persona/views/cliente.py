from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import BaseDeleteView

from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects

from ..models.cliente import Cliente

from ..forms.cliente import ClienteForm


class ClienteListView(ListView):
    model = Cliente
    paginate_by = settings.PER_PAGE
    template_name = "persona/cliente/list.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ClienteListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'nombres')
        self.f = empty(self.request, 'f', 'apellidos')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(ClienteListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'cliente'
        context['title'] = ('Seleccione %s para Cambiar') % ('cliente')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "persona/cliente/form.html"
    success_url = reverse_lazy('persona:cliente_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ClienteCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'cliente'
        context['title'] = "Crear cliente"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        msg = ('La %(name)s "%(obj)s" fue agregada satisfactoriamente.') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }

        messages.success(self.request, msg)
        return super(ClienteCreateView, self).form_valid(form)


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "persona/cliente/form.html"
    success_url = reverse_lazy('persona:cliente_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ClienteUpdateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ClienteUpdateView, self).get_initial()
        initial = initial.copy()
        d = self.object
        if d.lugar:
            initial['provincia'] = d.lugar.provincia
            initial['departamento'] = d.lugar.provincia.departamento

        return initial

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'cliente'
        context['title'] = 'cambiar %s' % 'cliente'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = 'The %(name)s "%(obj)s" fue cambiado satisfactoriamente.' % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)

        return super(ClienteUpdateView, self).form_valid(form)


class ClienteDeleteView(BaseDeleteView):
    model = Cliente
    success_url = reverse_lazy('persona:cliente_list')

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
        return super(ClienteDeleteView, self).dispatch(request, *args, **kwargs)

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
