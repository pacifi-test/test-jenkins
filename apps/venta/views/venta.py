import segno
import qrcode
import simplejson as json
import requests
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.base import View
from qr_code.templatetags.qr_code import qr_url_from_text

from apps.almacen.constants import VENDIDO
from apps.almacen.models.equipo import Equipo
from apps.persona.models.cliente import Cliente
from apps.persona.models.empresa import Empresa
from apps.producto.models.precio_venta import PrecioVenta
from apps.sunat.models.periodo import Periodo
from apps.sunat.models.serie import Serie
from apps.sunat.models.tipo_comprobante_pago import TipoComprobantePago
from apps.sunat.utils import numero_to_letras
from apps.venta.models.venta import Venta
from apps.venta.models.venta_detalle import VentaDetalle
from backend_apps.backend_auth.constants import UUIDEncoder
from backend_apps.backend_auth.models import User
from backend_apps.utils.decorators import permission_resource_required


class VentaForm(TemplateView):
    template_name = "venta/venta/form.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(VentaForm, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VentaForm, self).get_context_data(**kwargs)
        context['title'] = "Venta"
        context['opts'] = Venta._meta
        return context

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                venta = Venta()
                data = json.loads(request.body)

                tipo_comprobate = TipoComprobantePago.objects.get(codigo=data['tipo_comprobante'])
                serie = Serie.objects.get(estado=True, tipo_comprobante=tipo_comprobate)
                empresa = Empresa.objects.get(estado=True)
                user = self.request.user
                cliente = Cliente.objects.get(nro_documento=data['cliente']['nro_documento'])
                periodo = Periodo.objects.get(estado=True)
                venta.user = user
                venta.tipo_comprobante = tipo_comprobate
                venta.cliente = cliente
                venta.periodo = periodo
                # cargando serie  y número
                venta.serie = serie
                venta.nro_correlativo = serie.venta_set.all().count() + 1

                if tipo_comprobate.codigo == 99:
                    venta.contado = False

                if data['distribuidor']:
                    venta.distribuidor = User.objects.get(username=data['distribuidor']['username'])

                if serie.numero_maximo <= venta.nro_correlativo:
                    data = {
                        "message": "Numero de serie exedido"
                    }
                    dump = json.dumps(data)
                    return HttpResponse(dump, status=400, content_type="application/json")

                # datos electronicos

                venta.igv = 0
                venta.base_imponible = 0
                venta.total = 0
                venta.save()

                igv = 0
                base_imponible = 0
                total = 0
                # cargando detalles
                try:
                    for d in data['equipos']:

                        try:
                            ven_det = VentaDetalle()
                            equipo = Equipo.objects.get(imei=d['imei'])

                            precio_venta = PrecioVenta.objects.get(ruta=data['ruta'],
                                                                   producto_general__producto__equipo=equipo)
                            ven_det.equipo = equipo
                            ven_det.venta = venta
                            ven_det.cantidad = 1  # por este medio es 1
                            ven_det.precio_unitario = precio_venta.precio
                            ven_det.valor_unitario = float(precio_venta.precio) / float(
                                (1 + (float(periodo.igv) / 100)))

                            ven_det.precio_total = float(ven_det.cantidad) * float(precio_venta.precio)
                            ven_det.base_imponible = float(ven_det.precio_total) / (
                                    1 + (float(periodo.igv) / 100))
                            ven_det.igv = float(ven_det.precio_total) - float(ven_det.base_imponible)

                            ven_det.save()
                        except Exception as e:
                            print(e)

                        equipo.estado = VENDIDO
                        equipo.save()
                        # trabajando totales
                        base_imponible = float(base_imponible) + float(ven_det.base_imponible)
                        igv = float(igv) + float(ven_det.igv)
                        total = float(total) + float(ven_det.precio_total)


                except Exception as e:
                    data = {
                        "message": e
                    }
                    dump = json.dumps(data)
                    return HttpResponse(dump, status=400, content_type="application/json")
                venta.igv = igv
                venta.base_imponible = base_imponible
                venta.total = total
                venta.monto_texto = numero_to_letras(venta.total)
                venta.qr = "%s|%s|%s|%s|%.2f|%.2f|%s|%s|%s|" % (
                    empresa.nro_ruc,
                    venta.tipo_comprobante.codigo,
                    venta.serie.serie,
                    venta.nro_correlativo,
                    venta.igv,
                    venta.total,
                    venta.fecha_local().strftime("%Y-%m-%d"),
                    venta.cliente.tipo_documento.codigo,
                    venta.cliente.nro_documento,
                )
                venta.save()

                data = {
                    'id': venta.id,
                }

                dump = json.dumps(data, cls=UUIDEncoder)

                return HttpResponse(dump, content_type="application/json", status=201)
        except Exception as e:
            data = {"message": "Error %s" % e}
            dump = json.dumps(data)
            return HttpResponse(dump, status=400, content_type="application/json")


class VentaDetailView(DetailView):
    model = Venta
    template_name = "venta/venta/detail.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(VentaDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VentaDetailView, self).get_context_data(**kwargs)

        productos_generales = VentaDetalle.objects.values('equipo__producto__producto_general',
                                                          'equipo__producto__producto_general__codigo',
                                                          'precio_unitario').annotate(
            precio_total=Sum('precio_total'), base_imponible=Sum('base_imponible'), cantidad=Sum('cantidad')).filter(
            venta=self.get_object())

        for pr in productos_generales:
            equipos = Equipo.objects.filter(ventadetalle__venta=self.get_object(),
                                            producto__producto_general__id=pr['equipo__producto__producto_general'])

            pr['equipos'] = equipos

        qr_url = qr_url_from_text(self.object.qr, version=5, image_format="png", error_correction="L")

        context['opts'] = self.model._meta
        context['qr_url'] = qr_url

        context['productos_generales'] = productos_generales
        context['empresa'] = Empresa.objects.get(estado=True)

        context['title'] = "Venta"
        return context

    def get_template_names(self):
        if self.get_object().tipo_comprobante.codigo == "01":
            return ['venta/venta/factura.html']

        if self.get_object().tipo_comprobante.codigo == "03":
            return ['venta/venta/boleta.html']

        if self.get_object().tipo_comprobante.codigo == "99":
            return ['venta/venta/boleta.html']


class VentaListView(ListView):
    model = Venta
    template_name = "venta/venta/list.html"

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(VentaListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VentaListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['title'] = "Comprobante Electronico"
        return context


class VentaElectronicaView(View):

    @method_decorator(permission_resource_required())
    def dispatch(self, request, *args, **kwargs):
        return super(VentaElectronicaView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        venta = Venta.objects.get(id=self.kwargs['pk'])
        venta_detalles = VentaDetalle.objects.filter(venta=venta)
        empresa = Empresa.objects.get(estado=True)
        items = []
        num = 0
        for vd in venta_detalles:
            num = num + 1
            items.append(
                {
                    "item": num,
                    "codigo_interno": vd.equipo.producto.producto_general.codigo,
                    "descripcion": vd.equipo.producto.producto_general.descripcion,
                    "codigo_producto_sunat": None,
                    "unidad_de_medida": "NIU",
                    "cantidad": vd.cantidad,
                    "valor_unitario": vd.valor_unitario,
                    "codigo_tipo_precio": "01",
                    "precio_unitario": vd.precio_unitario,
                    "codigo_tipo_afectacion_igv": "10",
                    "total_base_igv": vd.base_imponible,
                    "porcentaje_igv": 18,
                    "total_igv": vd.igv,
                    "total_impuestos": vd.igv,
                    "total_valor_item": vd.base_imponible,
                    "total_item": vd.precio_total
                }
            )

        data = {
            "empresa_id": "1",
            "serie_documento": "%s" % venta.serie.serie,
            "numero_documento": "%s" % venta.nro_correlativo,
            "fecha_de_emision": venta.created_at.strftime("%Y-%m-%d"),
            "hora_de_emision": venta.fecha_local().strftime("%H:%M:%S"),
            "codigo_tipo_operacion": "0101",
            "codigo_tipo_documento": venta.tipo_comprobante.codigo,
            "codigo_tipo_moneda": "PEN",
            "fecha_de_vencimiento": venta.created_at.strftime("%Y-%m-%d"),
            "numero_orden_de_compra": "0045467898",
            # ESTO ES PARA NOTAS
            "codigo_tipo_documento_afecto": "01",
            "serie_documento_afecto": "F001",
            "numero_documento_afecto": "1",
            "nota_credito_tipo_codigo": "01",
            "nota_debito_tipo_codigo": "01",
            "nota_descripcion": "ANULACION DE LA OPERACION",
            # FIN NOTA
            "total_gratis": "0.00",
            "total_otros_cargos": "0.00",
            "datos_del_emisor": {
                "codigo_del_domicilio_fiscal": "0000"
            },
            "datos_del_cliente_o_receptor": {
                "codigo_tipo_documento_identidad": venta.cliente.tipo_documento.codigo,
                "numero_documento": venta.cliente.nro_documento,
                "apellidos_y_nombres_o_razon_social": venta.cliente.nombre_completo(),
                "codigo_pais": "PE",
                "ubigeo": venta.cliente.lugar.ubigeo(),
                "direccion": venta.cliente.direccion,
                "correo_electronico": None,
                "telefono": None
            },
            "totales": {
                "total_exportacion": 0.00,
                "total_operaciones_gravadas": venta.base_imponible,
                "total_operaciones_inafectas": 0.00,
                "total_operaciones_exoneradas": 0.00,
                "total_operaciones_gratuitas": 0.00,
                "total_igv": venta.igv,
                "total_impuestos": venta.igv,
                "total_valor": venta.base_imponible,
                "total_venta": venta.total
            },
            "items": items

        }
        headers = {'Content-type': 'application/json'}

        dump = json.dumps(data)

        try:
            print(dump)
            response = requests.post("http://facturador.imperiumse.com/api/document/", data=dump, headers=headers)
            # response = requests.post("http://factura-peru.com/api/document/", data=dump, headers=headers)

            if response.status_code == 404 or response.status_code == 500:
                messages.error(self.request, "No se puede completar la petición")

                return HttpResponseRedirect(reverse("venta:venta_list"))
        except:
            messages.error(self.request, "No se puede completar la petición")
            return HttpResponseRedirect(reverse("venta:venta_list"))
        data = json.loads(response.content)
        print(data)
        if data['data']['code']=='0':
            venta.electronico = True
            venta.save()
        else:
            messages.error(self.request, "No se puede completar la petición: %s %s" %(data['data']['code'],data['data']['description']) )
            return HttpResponseRedirect(reverse("venta:venta_list"))
        messages.success(self.request, "Recibo Electronico Satisfactoriamente")
        return HttpResponseRedirect(reverse("venta:venta_list"))


class VentaXml(View):

    def dispatch(self, request, *args, **kwargs):
        return super(VentaXml, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        venta = Venta.objects.get(id=self.kwargs['pk'])
        params = {
            "number": venta.nro_correlativo, "serie": venta.serie.serie, "company_number": '20605461043'}
        try:
            response = requests.get("http://facturador.imperiumse.com/api/document-xml/", params=params)
            print(response.content)
            if response.status_code == 500:
                messages.error(self.request, "error 500 api")
                return HttpResponseRedirect(reverse("venta:venta_list"))
        except Exception as e:

            messages.error(self.request, "error %s " % e)
            return HttpResponseRedirect(reverse("venta:venta_list"))
        messages.success(self.request, "respuesta satisfactoria")
        # response = requests.get("http://facturador.imperiumse.com/api/document-cdr/", data=dump, headers=headers)
        response = HttpResponse(response.content, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=' + "documeno.xml"
        return response
