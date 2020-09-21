from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from apps.almacen.models.salida import Salida
from backend_apps.backend_auth.models import User
from backend_apps.utils.decorators import permission_resource_required

from backend_apps.backend_auth.constants import VENTA




class UserDetailView(DetailView):
    model = User
    template_name = "almacen/user/detail.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        salidas = Salida.objects.filter(vendedor=self.object)
        context['salidas'] = salidas
        return context
