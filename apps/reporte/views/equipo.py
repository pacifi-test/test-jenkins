from django.utils.decorators import method_decorator
from django.views.generic import ListView

from apps.almacen.constants import ESTADO_EQUIPO_CHOICES
from apps.almacen.models.equipo import Equipo
from backend_apps.utils.decorators import permission_resource_required
from backend_apps.utils.forms import empty


class EquipoListView(ListView):
    model = Equipo
    template_name = "reporte/equipo/list.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(EquipoListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'imei')
        self.f = empty(self.request, 'f', 'estado')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        estado = self.request.GET.get('estado')
        contable = self.request.GET.get('contable')
        query = self.model.objects.all()
        print(query)
        print(estado)
        print(contable)
        if estado != "all":
            query = query.filter(estado=estado)
        if contable != 'all':
            if contable == 'true':
                query = query.filter(contable=True)
            else:
                query = query.filter(contable=False)

        return query.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(EquipoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['estados'] = ESTADO_EQUIPO_CHOICES
        context['title'] = "reporte Equipo"
        return context
