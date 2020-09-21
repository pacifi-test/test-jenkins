from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views.generic import DetailView, CreateView, TemplateView, ListView, DeleteView

from apps.sunat.models.igv import Igv
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.security import get_dep_objects
from ..models.compra import Compra
from ..models.compra_detalle import CompraDetalle
from ..forms.compra_detalle import CompraDetalleForm
from ...sunat.models.periodo import Periodo


class CompraDetalleCreateView(CreateView):
    model = CompraDetalle
    form_class = CompraDetalleForm
    template_name = "compra/detalle/form.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompraDetalleCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CompraDetalleCreateView, self).get_form_kwargs()
        compra_id = self.kwargs['compra_pk']
        kwargs['url'] = reverse('compra:compradetalle_add', kwargs={'compra_pk': compra_id})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CompraDetalleCreateView, self).get_context_data(**kwargs)
        context['periodo'] = Periodo.objects.get(estado=True)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        igv_periodo = Igv.objects.get(estado=True)
        compra = Compra.objects.get(id=self.kwargs['compra_pk'])

        self.object.compra = compra
        self.object.igv = igv_periodo.monto
        self.object.total = self.object.igv_total + self.object.precio_total

        self.object.user = self.request.user
        return super(CompraDetalleCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('compra:compra_detail', kwargs={'pk': self.object.compra.id})


class CompraDetalleListView(ListView):
    model = CompraDetalle
    template_name = "compra/detalle/list.html"

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CompraDetalleListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return CompraDetalle.objects.filter(compra__id=self.kwargs['compra_pk'])

    def get_context_data(self, **kwargs):
        context = super(CompraDetalleListView, self).get_context_data(**kwargs)
        compra_pk = self.kwargs['compra_pk']
        compra = Compra.objects.get(id=compra_pk)

        total = CompraDetalle.objects.filter(compra__id=compra_pk).aggregate(Sum('total'))

        context['compra_pk'] = compra_pk
        context['compra'] = compra
        context['total'] = total
        return context


class CompraDetalleDeleteView(DeleteView):
    model = CompraDetalle

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        self.compra_pk = self.kwargs['compra_pk']
        if not pk:
            return HttpResponseRedirect(self.get_success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.get_success_url())

        return super(CompraDetalleDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()

            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request, ('No se puede eliminars') % {
                    "name": self.model._meta.verbose_name
                            + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)

            d.delete()
            msg = ('El %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': force_text(self.model._meta.verbose_name),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)

        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        compra_pk = self.kwargs['compra_pk']
        return reverse('compra:compra_detail', kwargs={'pk': compra_pk})
