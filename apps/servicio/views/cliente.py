from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.persona.models.cliente import Cliente
from backend_apps.utils.decorators import permission_resource_required

import simplejson as json


class ClienteView(View):
    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ClienteView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        clientes = Cliente.objects.all()
        list_data = []
        for c in clientes:
            list_data.append({
                "nombre": c.nombres,
                "campo_search": "%s %s %s" % (c.nombres, c.apellidos, c.nro_documento),
                "apellidos": c.apellidos,
                "tipo_documento": c.tipo_documento.descripcion,
                "nro_documento": c.nro_documento,
                "direccion": c.direccion,
                "distrito": c.lugar.nombre,
                "provicia": c.lugar.provincia.nombre,
                "departamento": c.lugar.provincia.departamento.nombre,
                "lugar": "%s - %s - %s" % (
                    c.lugar.provincia.departamento.nombre,
                    c.lugar.provincia.nombre,
                    c.lugar.nombre)
            })
        dump = json.dumps(list_data)
        return HttpResponse(dump, status=200, content_type="application/json")
