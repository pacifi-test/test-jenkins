from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import BaseDeleteView

from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects
from ..models.precio_venta import PrecioVenta

from ..models.producto import Producto
from ..forms.producto import ProductoForm, ProductoSimpleForm
from ..models.producto_general import ProductoGeneral
from ...compra.models.compra_detalle import CompraDetalle


class ProductoListView(ListView):
    model = Producto
    template_name = "producto/producto/list.html"
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None

        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'codigo')
        self.f = empty(self.request, 'f', 'descripcion')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(ProductoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'producto'
        context['title'] = ('Seleccione %s para Cambiar') % ('producto')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "producto/producto/form.html"
    success_url = reverse_lazy('producto:producto_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductoCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'Producto'
        context['title'] = "Crear Producto"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        producto_general = self.object.producto_general
        self.object.marca = producto_general.marca
        self.object.codigo_general = producto_general.codigo
        self.object.descripcion = producto_general.descripcion
        if producto_general.imagen:
            self.object.imagen = producto_general.imagen

        msg = ('La %(name)s "%(obj)s" fue agregada satisfactoriamente.') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }

        messages.success(self.request, msg)
        return super(ProductoCreateView, self).form_valid(form)


class ProductoSimpleCreateView(CreateView):
    model = Producto
    form_class = ProductoSimpleForm
    template_name = "producto/producto/form_simple.html"
    success_url = reverse_lazy('producto:producto_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoSimpleCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ProductoSimpleCreateView, self).get_form_kwargs()
        producto_general_id = self.kwargs['producto_general_pk']
        kwargs['url'] = reverse('producto:producto_simple_add', kwargs={'producto_general_pk': producto_general_id})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProductoSimpleCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'Producto'
        context['title'] = "Crear Producto"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        producto_general = ProductoGeneral.objects.get(id=self.kwargs['producto_general_pk'])
        self.object.producto_general = producto_general
        self.object.marca = producto_general.marca
        self.object.codigo_general = producto_general.codigo
        self.object.codigo = "%s-%s" % (producto_general.codigo, self.object.color)
        self.object.descripcion = producto_general.descripcion
        if producto_general.imagen:
            self.object.imagen = producto_general.imagen

        msg = ('La %(name)s "%(obj)s" fue agregada satisfactoriamente.') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }

        messages.success(self.request, msg)
        return super(ProductoSimpleCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('producto:producto_general_update', kwargs={'pk': self.kwargs['producto_general_pk']})


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "producto/producto/form.html"
    success_url = reverse_lazy('producto:producto_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductoUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'Producto'
        context['title'] = 'cambiar %s' % 'Producto'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = 'The %(name)s "%(obj)s" fue cambiado satisfactoriamente.' % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }

        messages.success(self.request, msg)

        return super(ProductoUpdateView, self).form_valid(form)


class ProductoSimpleUpdateView(UpdateView):
    model = Producto
    form_class = ProductoSimpleForm
    template_name = "producto/producto/form_simple.html"
    success_url = reverse_lazy('producto:producto_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoSimpleUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ProductoSimpleUpdateView, self).get_form_kwargs()
        producto_general_id = self.kwargs['producto_general_pk']
        kwargs['url'] = reverse('producto:producto_simple_update',
                                kwargs={'pk': self.kwargs['pk'],
                                        'producto_general_pk': producto_general_id})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProductoSimpleUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'Producto'
        context['title'] = 'cambiar %s' % 'Producto'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = 'The %(name)s "%(obj)s" fue cambiado satisfactoriamente.' % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }

        messages.success(self.request, msg)

        return super(ProductoSimpleUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('producto:producto_general_update', kwargs={'pk': self.kwargs['producto_general_pk']})


class ProductoDeleteView(BaseDeleteView):
    model = Producto
    success_url = reverse_lazy('producto:producto_list')

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
        return super(ProductoDeleteView, self).dispatch(request, *args, **kwargs)

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


class ProductoSimpleDeleteView(BaseDeleteView):
    model = Producto

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
        return super(ProductoSimpleDeleteView, self).dispatch(request, *args, **kwargs)

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
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('producto:producto_general_update', kwargs={'pk': self.kwargs['producto_general_pk']})
