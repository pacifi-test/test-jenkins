from django.conf.urls import url

from .views.compra import (CompraCreateView, CompraDetailView, CompraPendienteListView, CompraProcesarView,
                           CompraUpdateView, CompraListView)
from .views.compra_detalle import CompraDetalleCreateView, CompraDetalleListView, CompraDetalleDeleteView
from .views.producto_general import ProductoGeneralAutocomplete
from .views.proveedor import ProveedorTemplateView, ProveedorAutocomplete

urlpatterns = [
    # Cargar Menu
    url('compra/crear$', CompraCreateView.as_view(), name='compra_add'),
    url('compra/pendientes$', CompraPendienteListView.as_view(), name='compra_slopes'),
    url('compra/listar$', CompraListView.as_view(), name='compra_list'),

    # No Menu
    url('compra/procesar/(?P<pk>[^/]+)', CompraProcesarView.as_view(), name='compra_process'),
    url('compra/actualizar/(?P<pk>[^/]+)', CompraUpdateView.as_view(), name='compra_update'),
    url('compra/detallar/(?P<pk>[^/]+)$', CompraDetailView.as_view(), name='compra_detail'),

    url('compra_detalle/crear/(?P<compra_pk>[^/]+)$', CompraDetalleCreateView.as_view(), name='compradetalle_add'),
    url('compra_detalle/listar/(?P<compra_pk>[^/]+)$', CompraDetalleListView.as_view(), name='compradetalle_list'),
    url('compra_detalle/eliminar/(?P<pk>[^/]+)/(?P<compra_pk>[^/]+)$', CompraDetalleDeleteView.as_view(),
        name='compradetalle_delete'),

    # Utils

    url('proveedor/view/$', ProveedorTemplateView.as_view(), name='proveedor_view'),
    # Autocompletes
    url('proveedor/autocomplete/', ProveedorAutocomplete.as_view(), name='proveedor_autocomplete'),
    url('producto/autocomplete/', ProductoGeneralAutocomplete.as_view(), name='producto_autocomplete')

]
