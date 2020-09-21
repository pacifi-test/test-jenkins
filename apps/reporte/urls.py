from django.conf.urls import url

from .views.equipo import EquipoListView

urlpatterns = [
    # Menu
    url(u'^equipo/listar$', EquipoListView.as_view(), name='equipo_list'),
    url(u'^salida/listar$', EquipoListView.as_view(), name='equipo_list'),

    url(u'^salida/detail/(?P<pk>[^/]+)$', EquipoListView.as_view(), name='equipo_list'),

]
