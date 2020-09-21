from django.conf.urls import url

from .views.pedido import PedidoCrearTemplateView, PedidoDetailView, PedidoListView, PedidoStateUpdate
from .views.producto import ProductoView
from .views.salida import SalidaListView, SalidaDetailView, SalidaUpdateView

urlpatterns = [
    # Menu
    url(r"^salida/listar$", SalidaListView.as_view(), name='salida_list'),
    url(r"^pedido/crear$", PedidoCrearTemplateView.as_view(), name='pedido_add'),
    url(r"^pedido/listar$", PedidoListView.as_view(), name='pedido_list'),
    # utils
    url(r"^salida/detallar/(?P<pk>[^/]+)$", SalidaDetailView.as_view(), name='salida_detail'),
    url(r"^salida/aceptar/(?P<pk>[^/]+)$", SalidaUpdateView.as_view(), name='salidaaceptar_update'),

    url(r"^pedido/crear$", SalidaListView.as_view(), name='salida_list'),
    url(r"^pedido/detallar/(?P<pk>[^/]+)$", PedidoDetailView.as_view(), name='pedido_detail'),
    url(r"^pedido/update/(?P<pk>[^/]+)$", PedidoStateUpdate.as_view(), name='pedido_update'),

    # apis
    url(r"^producto/listar$", ProductoView.as_view(), name='producto_list'),

]
