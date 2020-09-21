from django.conf.urls import url

from .models.marca import Marca
from .views.marca import MarcaListView, MarcaCreateView, MarcaDeleteView, MarcaUpdateView, MarcaAutocomplete
from .views.precio_venta import PrecioVentaCreateView, PrecioVentaUpdateView, PrecioListView
from .views.producto import ProductoCreateView, ProductoDeleteView, ProductoListView, ProductoUpdateView, \
    ProductoSimpleCreateView, ProductoSimpleDeleteView, ProductoSimpleUpdateView
from .views.producto_general import ProductoGeneralCreateView, ProductoGeneralUpdateView, ProductoGeneralDeleteView, \
    ProductoGeneralListView

urlpatterns = [
    # Menu
    url(u'^marca/listar$', MarcaListView.as_view(), name='marca_list'),
    url(u'^producto/listar$', ProductoListView.as_view(), name='producto_list'),
    url(u'^producto_general/listar$', ProductoGeneralListView.as_view(), name='producto_general_list'),

    # Utils
    url(u'^marca/crear$', MarcaCreateView.as_view(), name='marca_add'),
    url(u'^marca/actualizar/(?P<pk>[^/]+)$', MarcaUpdateView.as_view(), name='marca_update'),
    url(u'^marca/eliminar/(?P<pk>[^/]+)$', MarcaDeleteView.as_view(), name='marca_delete'),
    url(u'^producto/crear$', ProductoCreateView.as_view(), name='producto_add'),
    url(u'^producto/crear_simple/(?P<producto_general_pk>[^/]+)$', ProductoSimpleCreateView.as_view(),
        name='producto_simple_add'),
    url(u'^producto/actualizar/(?P<pk>[^/]+)$', ProductoUpdateView.as_view(), name='producto_update'),
    url(u'^producto/actualizar_simple/(?P<pk>[^/]+)/(?P<producto_general_pk>[^/]+)$',
        ProductoSimpleUpdateView.as_view(),
        name='producto_simple_update'),
    url(u'^producto/eliminar/(?P<pk>[^/]+)$', ProductoDeleteView.as_view(), name='producto_delete'),
    url(u'^producto/eliminar_simple/(?P<pk>[^/]+)/(?P<producto_general_pk>[^/]+)$', ProductoSimpleDeleteView.as_view(),
        name='producto_simple_delete'),
    url(u'^producto_general/crear$', ProductoGeneralCreateView.as_view(), name='producto_general_add'),
    url(u'^producto_general/actualizar/(?P<pk>[^/]+)$', ProductoGeneralUpdateView.as_view(),
        name='producto_general_update'),
    url(u'^producto_general/eliminar/(?P<pk>[^/]+)$', ProductoGeneralDeleteView.as_view(),
        name='producto_general_delete'),

    url('precio/listar/(?P<producto_general_pk>[^/]+)', PrecioListView.as_view(), name='precio_list'),
    url('precio/agregar/(?P<producto_general_pk>[^/]+)', PrecioVentaCreateView.as_view(), name='precioventa_add'),
    url('precio/actualizar/(?P<pk>[^/]+)', PrecioVentaUpdateView.as_view(), name='precio_update'),

    # Autocompletes
    url('marca/autocomplete/', MarcaAutocomplete.as_view(model=Marca, create_field='nombre'),
        name='marca_autocomplete'),
]
