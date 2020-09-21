import simplejson as json
from django.conf import settings

from django.db.models import Sum
from django.forms import model_to_dict

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from qr_code.templatetags.qr_code import qr_url_from_text

from apps.almacen.models.equipo import Equipo
from apps.persona.models.empresa import Empresa
from apps.venta.models.venta import Venta
from apps.venta.models.venta_detalle import VentaDetalle
from backend_apps.utils.decorators import permission_resource_required


class VentaJson(View):

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(VentaJson, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        venta = Venta.objects.get(id=self.request.GET.get("venta_id"))
        items = []
        productos_generales = VentaDetalle.objects.values('equipo__producto__producto_general__codigo',
                                                          'precio_unitario').annotate(
            precio_total=Sum('precio_total'), base_imponible=Sum('base_imponible'), cantidad=Sum('cantidad'),
            igv=Sum('igv')).filter(
            venta=venta)
        for p in productos_generales:
            equipos = [(e.imei) for e in Equipo.objects.filter(ventadetalle__venta=venta,
                                                               producto__producto_general__codigo=p[
                                                                   'equipo__producto__producto_general__codigo'])]
            str1 = ', '.join(str(e) for e in equipos)
            desc = "%s %s" % (p['equipo__producto__producto_general__codigo'], str1)
            items.append(
                {
                    'codigo': p['equipo__producto__producto_general__codigo'],
                    'descripcion': desc,
                    'precio_unitario': "%.2f" % p['precio_unitario'],
                    'precio_total': "%.2f" % p['precio_total'],
                    'base_imponible': "%.2f" % p['base_imponible'],
                    'cantidad': p['cantidad'],
                    'igv': "%.2f" % p['igv'],

                }
            )

        empresa = Empresa.objects.get(estado=True)
        qr_img = qr_url_from_text(venta.qr, version=5, image_format="png", error_correction="L")

        domain = request.META['HTTP_HOST']
        if settings.DEBUG == True:
            http = "http://"
        else:
            http = "https://"
        data = {
            'empresa': empresa.nombre,
            'nro_ruc': empresa.nro_ruc,
            "qr_img": http + domain + qr_img,
            "serie_numero": venta.serie_numero(),
            "fecha": venta.fecha_local().strftime("%d-%m-%Y"),
            "cliente": {
                "nombre_completo": venta.cliente.nombre_completo(),
                "nro_documento": venta.cliente.nro_documento,
                "tipo_documento": venta.cliente.tipo_documento.descripcion,
                "direccion": venta.cliente.direccion,
            },
            'venta': model_to_dict(venta,
                                   fields=['nro_correlativo', 'igv', 'base_imponible', 'total', 'monto_texto', 'qr'])
            ,
            "items": items,

        }
        dump = json.dumps(data)
        return HttpResponse(dump, status=200, content_type="application/json")
