import simplejson as json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from backend_apps.backend_auth.models import User
from backend_apps.utils.decorators import permission_resource_required


class UserView(View):

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(UserView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        rol = self.request.GET.get("rol")
        if rol:
            users = users.filter(groups__name=rol)
        data = []
        for user in users:
            if user.person:
                data.append({
                    "username": user.username,
                    "nombres": user.person.first_name if user.person else user.username,
                    "apellidos": user.person.last_name if user.person else user.username,
                    "nro_documento": user.person.identity_num if user.person else "SN",
                })
        dump = json.dumps(data)
        return HttpResponse(dump, status=201, content_type="application/json")
