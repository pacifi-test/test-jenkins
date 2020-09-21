from django.contrib import admin

from .models.cliente import Cliente
from .models.empresa import Empresa

from .models.proveedor import Proveedor

from .models.departamento import Departamento
from .models.provincia import Provincia
from .models.distrito import Distrito


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    pass


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    pass


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre')


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'departamento', 'codigo', 'nombre',)


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'provincia', 'codigo', 'nombre')


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    pass
