from django.http import JsonResponse

from apps.persona.models.departamento import Departamento
from apps.persona.models.distrito import Distrito
from apps.persona.models.provincia import Provincia


def provincia_select(request):
    if request.method == 'GET':
        if request.is_ajax():
            departamento = Departamento.objects.get(id=request.GET.get('departamento'))
            pronvincias = Provincia.objects.filter(departamento=departamento)
            pronvincias = [{'id': x.id, 'nombre': x.nombre} for x in pronvincias]

            data = {
                "pronvincia_list": list(pronvincias)
            }

            return JsonResponse(data)
    return JsonResponse({"ss": "error"})


def distrito_select(request):
    if request.method == 'GET':
        if request.is_ajax():
            provincia = Provincia.objects.get(id=request.GET.get('provincia'))
            distritos = Distrito.objects.filter(provincia=provincia)
            pronvincias = [{'id': x.id, 'nombre': x.nombre} for x in distritos]

            data = {
                "pronvincia_list": list(pronvincias)
            }
            return JsonResponse(data)
