from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import BaseDeleteView

from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty
from backend_apps.utils.security import get_dep_objects
from ..constants import LOCAL, REGIONAL, NACIONAL
from ..forms.producto_general import ProductoGeneralForm
from ..models.precio_venta import PrecioVenta
from ..models.producto_general import ProductoGeneral


class ProductoGeneralListView(ListView):
    model = ProductoGeneral
    template_name = "producto/producto_general/list.html"
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoGeneralListView, self).dispatch(request, *args, **kwargs)

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
        context = super(ProductoGeneralListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'producto general'
        context['title'] = ('Seleccione %s para Cambiar') % ('producto General')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class ProductoGeneralCreateView(CreateView):
    model = ProductoGeneral
    form_class = ProductoGeneralForm
    template_name = "producto/producto_general/form.html"
    success_url = reverse_lazy('producto:producto_general_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoGeneralCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductoGeneralCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'Producto General'
        context['title'] = "Crear Producto General"
        return context

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            self.object = form.save(commit=True)
            msg = ('El %(name)s "%(obj)s" fue agregada satisfactoriamente.') % {
                'name': self.model._meta.verbose_name,
                'obj': self.object
            }

            # precio Local
            precio = PrecioVenta()
            precio.producto_general = self.object
            precio.estado = True
            precio.ruta = LOCAL
            precio.user = self.request.user
            precio.precio = form.cleaned_data['precio_local']
            precio.save()

            # precio Regional
            precio = PrecioVenta()
            precio.producto_general = self.object
            precio.estado = True
            precio.ruta = REGIONAL
            precio.user = self.request.user
            precio.precio = form.cleaned_data['precio_regional']
            precio.save()

            # precio Nacional
            precio = PrecioVenta()
            precio.producto_general = self.object
            precio.estado = True
            precio.ruta = NACIONAL
            precio.user = self.request.user
            precio.precio = form.cleaned_data['precio_nacional']
            precio.save()

            messages.success(self.request, msg)
            return super(ProductoGeneralCreateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.error(self.request, e)

            return super(ProductoGeneralCreateView, self).form_invalid(form)


class ProductoGeneralUpdateView(UpdateView):
    model = ProductoGeneral
    form_class = ProductoGeneralForm
    template_name = "producto/producto_general/form.html"
    success_url = reverse_lazy('producto:producto_general_list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoGeneralUpdateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProductoGeneralUpdateView, self).get_initial()
        initial = initial.copy()
        if self.get_object():
            try:
                precio_local = PrecioVenta.objects.get(producto_general=self.get_object(), ruta=LOCAL, estado=True)

                if precio_local:
                    initial['precio_local'] = precio_local.precio
                    initial['precio_local_id'] = precio_local.id

                precio_regional = PrecioVenta.objects.get(producto_general=self.get_object(), ruta=REGIONAL,
                                                          estado=True)

                if precio_regional:
                    initial['precio_regional'] = precio_regional.precio
                    initial['precio_regional_id'] = precio_regional.id

                precio_nacional = PrecioVenta.objects.get(producto_general=self.get_object(), ruta=NACIONAL,
                                                          estado=True)

                if precio_nacional:
                    initial['precio_nacional'] = precio_nacional.precio
                    initial['precio_nacional_id'] = precio_nacional.id
            except:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super(ProductoGeneralUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'Producto General'
        context['title'] = 'cambiar %s' % 'Producto General'
        return context

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            self.object = form.save(commit=False)
            msg = 'El %(name)s "%(obj)s" fue cambiado satisfactoriamente.' % {
                'name': self.model._meta.verbose_name,
                'obj': self.object
            }
            messages.success(self.request, msg)
            try:
                precio_local = PrecioVenta.objects.get(producto_general=self.get_object(), ruta=LOCAL, estado=True)

            except:
                precio_local = PrecioVenta()
                precio_local.producto_general = self.object
                precio_local.estado = True
                precio_local.ruta = LOCAL
                precio_local.user = self.request.user
                precio_local.precio = form.cleaned_data['precio_local']
                precio_local.save()

            precio_local.precio = form.cleaned_data['precio_local']
            precio_local.save()
            try:
                precio_regional = PrecioVenta.objects.get(producto_general=self.get_object(), ruta=REGIONAL,
                                                          estado=True)

            except:
                precio_regional = PrecioVenta()

                precio_regional.producto_general = self.object
                precio_regional.estado = True
                precio_regional.ruta = REGIONAL
                precio_regional.user = self.request.user
                precio_regional.precio = form.cleaned_data['precio_regional']
                precio_regional.save()

            precio_regional.precio = form.cleaned_data['precio_regional']
            precio_regional.save()

            try:
                precio_nacional = PrecioVenta.objects.get(producto_general=self.get_object(), ruta=NACIONAL,
                                                          estado=True)

            except:
                precio_nacional = PrecioVenta()
                precio_nacional.producto_general = self.object
                precio_nacional.estado = True
                precio_nacional.ruta = NACIONAL
                precio_nacional.user = self.request.user
                precio_nacional.precio = form.cleaned_data['precio_nacional']
                precio_nacional.save()

            precio_nacional.precio = form.cleaned_data['precio_nacional']
            precio_nacional.save()

            return super(ProductoGeneralUpdateView, self).form_valid(form)

        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            return super(ProductoGeneralUpdateView, self).form_invalid(form)


class ProductoGeneralDeleteView(BaseDeleteView):
    model = ProductoGeneral
    success_url = reverse_lazy('producto:producto_general_list')

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
        return super(ProductoGeneralDeleteView, self).dispatch(request, *args, **kwargs)

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
