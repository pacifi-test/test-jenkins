"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog

from backend_apps.access.views import dashboard

from django.conf.urls.static import static
from qr_code import urls as qr_code_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript_catalog'),
    url(r'^qr_code/', include(qr_code_urls, namespace="qr_code")),

    # Backend

    url(r'^backend/', include('backend_apps.backend_auth.urls', namespace='backend')),
    url(r'^access/', include('backend_apps.access.urls', namespace='access')),

    url(r'^$', dashboard, name='dashboard'),

    # My Apps
    url(r'^almacen/', include('apps.almacen.urls', namespace='almacen')),
    url(r'^compra/', include('apps.compra.urls', namespace='compra')),
    url(r'^persona/', include('apps.persona.urls', namespace='persona')),
    url(r'^producto/', include('apps.producto.urls', namespace='producto')),
    url(r'^sunat/', include('apps.sunat.urls', namespace='sunat')),
    url(r'^servicio/', include('apps.servicio.urls', namespace='servicio')),
    url(r'^vendedor/', include('apps.vendedor.urls', namespace='vendedor')),
    url(r'^venta/', include('apps.venta.urls', namespace='venta')),
    url(r'^reporte/', include('apps.reporte.urls', namespace='reporte')),

]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
