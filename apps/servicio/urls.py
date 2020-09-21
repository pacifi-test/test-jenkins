from django.conf.urls import url

from .views.cliente import ClienteView
from .views.user import UserView
from .views.producto import ProductoListGetView
from .views.tipo_comprobante import TipoComprobantesJson
from .views.venta import VentaJson

urlpatterns = [

    # Menus
    url(u'^cliente/list_get$', ClienteView.as_view(), name='cliente_list_get'),

    url(u'^tipo_comprobante/list_get$', TipoComprobantesJson.as_view(), name='tipo_comprobantes_list_get'),

    url(u'^user/list_get$', UserView.as_view(), name='distribuidor_list_get'),
    url(u'^producto/list_get$', ProductoListGetView.as_view(), name='producto_list_get'),
    url(u'^venta/get$', VentaJson.as_view(), name='venta_get'),

    # Vistas

]
