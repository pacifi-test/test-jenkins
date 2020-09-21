from django.conf.urls import url

from .views.venta import VentaForm, VentaDetailView, VentaListView, VentaElectronicaView, VentaXml
from .views.equipo import EquipoGetJson

urlpatterns = [
    # Menus
    url(u'^venta/crear$', VentaForm.as_view(), name='venta_form'),

    # Vistas
    url(u'^venta/listar$', VentaListView.as_view(), name='venta_list'),
    url(r"^venta/detallar/(?P<pk>[^/]+)$", VentaDetailView.as_view(), name='venta_detail'),
    url(r"^venta/electronica/(?P<pk>[^/]+)$", VentaElectronicaView.as_view(), name='venta_electronica'),
    url(r"^venta/xml/(?P<pk>[^/]+)$", VentaXml.as_view(), name='venta_xml'),
    url(r"^venta/cdr/(?P<pk>[^/]+)$", VentaElectronicaView.as_view(), name='venta_electronica'),
    # Json
    url(u'^equipo/get$', EquipoGetJson.as_view(), name='equipo_get'),

]
