from dal import autocomplete
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

from ..models.marca import Marca

from ..forms.marca import MarcaForm


class MarcaListView(ListView):
    model = Marca
    paginate_by = settings.PER_PAGE
    template_name = "producto/marca/list.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MarcaListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'id')
        self.f = empty(self.request, 'f', 'nombre')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(MarcaListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'marca'
        context['title'] = ('Seleccione %s para Cambiar') % ('marca')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = "producto/marca/form.html"
    success_url = reverse_lazy('producto:marca_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MarcaCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MarcaCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'marca'
        context['title'] = "Crear Marca"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        msg = ('La %(name)s "%(obj)s" fue agregada satisfactoriamente.') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }

        messages.success(self.request, msg)
        return super(MarcaCreateView, self).form_valid(form)


class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = "producto/marca/form.html"
    success_url = reverse_lazy('producto:marca_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MarcaUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MarcaUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'marca'
        context['title'] = 'cambiar %s' % 'Marca'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = 'The %(name)s "%(obj)s" fue cambiado satisfactoriamente.' % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)

        return super(MarcaUpdateView, self).form_valid(form)


class MarcaDeleteView(BaseDeleteView):
    model = Marca
    success_url = reverse_lazy('producto:marca_list')

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
        return super(MarcaDeleteView, self).dispatch(request, *args, **kwargs)

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


class MarcaAutocomplete(autocomplete.Select2QuerySetView):
    def get_create_option(self, context, q):
        """Form the correct create_option to append to results."""
        create_option = []
        display_create_option = False
        if self.create_field and q:
            page_obj = context.get('page_obj', None)
            if page_obj is None or page_obj.number == 1:
                display_create_option = True

            # Don't offer to create a new option if a
            # case-insensitive) identical one already exists
            existing_options = (self.get_result_label(result).lower()
                                for result in context['object_list'])
            if q.lower() in existing_options:
                display_create_option = False

        if display_create_option and self.has_add_permission(self.request):
            create_option = [{
                'id': q,
                'text': ('Crear "%(new_value)s"') % {'new_value': q},
                'create_id': True,
            }]
        return create_option

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Marca.objects.none()

        qs = Marca.objects.all()

        if self.q:
            qs = qs.filter(nombre__istartswith=self.q)

        return qs
