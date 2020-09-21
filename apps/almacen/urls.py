from django.conf.urls import url

from .views.arqueo import ArqueoSalidaListView, ArqueoListView, ArqueoSalidaDetailView, ArqueoSalidaEquipoUpdateView, \
    ArqueoSalidaCerrar
from .views.compra import ComprobanteListView, CompraDetailView, ComprobanteEstadoUpdateView
from .views.compra_detalle import CompraDetalleDetailView, CompraDetalleServiceView
from .views.equipo import EquiposAddServicioView, EquipoJson, EquipoMenuListView, \
    EquipoUpdateView, EquipoDetailView, EquipoDeleteView
from .views.usuario import UserDetailView
from .views.salida import SalidaCreateTemplateView, SalidaDetailView
from .views.producto import ProductoListView, ProductoDetailView, ProductoDetailCountAlmacenServiceView

urlpatterns = [

    # Menu
    url(r"^compra/listar$", ComprobanteListView.as_view(), name='compra_list'),
    url(r"^arqueo/listar$", ArqueoListView.as_view(), name='arqueo_list'),
    url(r"^salida/crear$", SalidaCreateTemplateView.as_view(), name='salida_add'),
    url(r"^producto/listar$", ProductoListView.as_view(), name='producto_list'),
    url(r"^equipo/listar$", EquipoMenuListView.as_view(), name='equipo_list_menu'),

    # Utils

    url(r"^usuario/detallar/(?P<pk>[^/]+)$", UserDetailView.as_view(), name='user_detail'),
    url(r"^salida/detallar/(?P<pk>[^/]+)$", SalidaDetailView.as_view(), name='salida_detail'),
    url(r"^producto/detallar/(?P<pk>[^/]+)$", ProductoDetailView.as_view(), name='producto_detail'),

    # administracion de equipo
    url(r"^equipo/detail/(?P<pk>[^/]+)$", EquipoDetailView.as_view(), name='equipo_detail'),
    url(r"^equipo/eliminar/(?P<pk>[^/]+)$", EquipoDeleteView.as_view(), name='equipo_delete'),
    url(r"^equipo/actualizar/(?P<pk>[^/]+)$", EquipoUpdateView.as_view(), name='equipo_update'),

    # compra
    url(r"^compra_detalle/detallar/(?P<pk>[^/]+)/(?P<producto_pk>[^/]+)$", CompraDetalleDetailView.as_view(),
        name='compra_detalle_detail'),
    url(r"^compra/detallar/(?P<pk>[^/]+)$", CompraDetailView.as_view(), name='compra_detail'),
    url(r"^compra/update_status/(?P<pk>[^/]+)$", ComprobanteEstadoUpdateView.as_view(), name='compra_updatestatus'),
    url(r"^compra_detalle/detailjson/$", CompraDetalleServiceView.as_view(), name='comra_detalle_detail_json'),

    # Arqueo
    url(r"^arqueo_salida/listar/(?P<user_pk>[^/]+)$", ArqueoSalidaListView.as_view(), name='arqueo_salida_list'),
    url(r"^arqueo_salida/detallar/(?P<salida_pk>[^/]+)$", ArqueoSalidaDetailView.as_view(),
        name='arqueo_salida_detail'),
    url(r"^arqueo_salida/cerrar/(?P<salida_pk>[^/]+)$", ArqueoSalidaCerrar.as_view(), name='arqueo_salida_close'),
    url(r"^arqueo_salida/equipo/(?P<salida_detalle_pk>[^/]+)$", ArqueoSalidaEquipoUpdateView.as_view(),
        name='arqueo_equipo_update'),

    # Service
    url(r"^equipo/add_service$", EquiposAddServicioView.as_view(), name='equipo_addservice'),
    url(r"^equipo/detail_json$", EquipoJson.as_view(), name='equipo_detail_json'),
    url(r"^producto/almacen_contar/(?P<pk>[^/]+)$", ProductoDetailCountAlmacenServiceView.as_view(),
        name='producto_detailservice'),

]
