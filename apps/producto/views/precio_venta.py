from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView

from backend_apps.utils.decorators import permission_resource_required

from ..forms.precio_venta import PrecioVentaForm
from ..models.precio_venta import PrecioVenta
from ..models.producto import Producto
from ..models.producto_general import ProductoGeneral
from ...compra.models.compra_detalle import CompraDetalle


class PrecioListView(DetailView):
    model = ProductoGeneral
    template_name = "producto/producto_general/detail.html"
    pk_url_kwarg = "producto_general_pk"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrecioListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrecioListView, self).get_context_data(**kwargs)

        compras_detalles = CompraDetalle.objects.filter(producto_general=self.object).order_by('-created_at')

        precios = PrecioVenta.objects.filter(producto_general=self.object)

        completo = True if len(precios) == 3 else False

        context['compras_detalles'] = compras_detalles
        context['opts'] = self.model._meta
        context['cmi'] = 'productos'
        context['completo'] = completo

        context['precios'] = precios
        context['title'] = ('Seleccione %s para Cambiar') % ('producto')
        return context


class PrecioVentaCreateView(CreateView):
    model = PrecioVenta
    template_name = "producto/precio/form.html"
    form_class = PrecioVentaForm

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrecioVentaCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PrecioVentaCreateView, self).get_form_kwargs()
        producto_general_id = self.kwargs['producto_general_pk']
        kwargs['url'] = reverse('producto:precioventa_add', kwargs={'producto_general_pk': producto_general_id})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        producto_general_id = self.kwargs['producto_general_pk']
        self.object.producto_general_id = producto_general_id
        self.object.user = self.request.user
        msg = ('La %(name)s "%(obj)s" fue modificado satisfactoriamente.') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)
        return super(PrecioVentaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("producto:precio_list", kwargs={'producto_general_pk': self.object.producto_general_id})


class PrecioVentaUpdateView(UpdateView):
    model = PrecioVenta
    template_name = "producto/precio/form.html"
    form_class = PrecioVentaForm

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrecioVentaUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PrecioVentaUpdateView, self).get_form_kwargs()
        precio_id = self.kwargs['pk']
        kwargs['url'] = reverse('producto:precio_update', kwargs={'pk': precio_id})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        msg = ('La %(name)s "%(obj)s" fue modificado satisfactoriamente.') % {
            'name': self.model._meta.verbose_name,
            'obj': self.object
        }
        messages.success(self.request, msg)
        return super(PrecioVentaUpdateView, self).form_valid(form)

    def get_success_url(self):
        print("self.object.producto_general.id")
        print(self.object.producto_general)
        return reverse("producto:precio_list", kwargs={'producto_general_pk': self.object.producto_general.id})
