from django.conf.urls import url

from .views.cliente import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView
from .views.proveedor import ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView

from .views.csv import departamento_upload
from .views.ubigeo import distrito_select, provincia_select

urlpatterns = [

    # Menus

    url(u'^persona/listar$', ClienteListView.as_view(), name='cliente_list'),
    url(u'^proveedor/listar$', ProveedorListView.as_view(), name='proveedor_list'),

    # Utils
    url(u'^persona/crear$', ClienteCreateView.as_view(), name='cliente_add'),
    url(u'^persona/actualizar/(?P<pk>[^/]+)$', ClienteUpdateView.as_view(), name='cliente_update'),
    url(u'^persona/eliminar/(?P<pk>[^/]+)$', ClienteDeleteView.as_view(), name='cliente_delete'),
    url(u'^proveedor/crear$', ProveedorCreateView.as_view(), name='proveedor_add'),
    url(u'^proveedor/actualizar/(?P<pk>[^/]+)$', ProveedorUpdateView.as_view(), name='proveedor_update'),
    url(u'^proveedor/eliminar/(?P<pk>[^/]+)$', ProveedorDeleteView.as_view(), name='proveedor_delete'),

    # url(u'^ubigeo/departamento$', departamento_upload, name='depto_upload')

    # Apis Change
    url(u'^provincia/list_select/$', provincia_select, name='pronvincia_select'),
    url(u'^distrito/list_select/$', distrito_select, name='distrito_select'),

]
