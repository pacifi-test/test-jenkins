from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import BaseUpdateView

from apps.almacen.models.salida import Salida
from apps.almacen.models.salida_detalle import SalidaDetalle
from apps.vendedor.forms.salida import SalidaModelForm
from backend_apps.utils.decorators import permission_resource_required


class SalidaListView(ListView):
    model = Salida
    template_name = "vendedor/salida/list.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(SalidaListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = self.model.objects.filter(vendedor=user).order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SalidaListView, self).get_context_data(**kwargs)

        context['opts'] = self.model._meta
        context['title'] = "Salida Detalle"
        return context


class SalidaDetailView(DetailView):
    model = Salida
    template_name = "vendedor/salida/detail.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(SalidaDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SalidaDetailView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = "Salida Detalle"
        return context


class SalidaUpdateView(BaseUpdateView):
    model = Salida
    form_class = SalidaModelForm

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(SalidaUpdateView, self).dispatch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        d = self.get_object()
        d.estado = True
        print("update")
        d.save()
        msg = "La salida se acepto exitosamente"
        messages.success(self.request, msg)

        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_success_url(self):
        d = self.get_object()

        return reverse("vendedor:salida_detail", kwargs={"pk": d.id})
