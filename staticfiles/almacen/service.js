(function () {
    "use strict";
    angular.module("myApp")
        .factory("AlmacenService", ["$resource", AlmacenService]);

    function AlmacenService($resource) {
        var url = "/almacen/";
        var params = {'id': '@id'};
        var methods = {"update": {method: 'PUT'}};
        return {
            Producto: $resource(url + "producto/almacen_contar/:id/", params, methods),
            Equipo: $resource(url + "equipo/add_service/:id/", params, methods),
            EquipoGet: $resource(url + "equipo/detail_json/:id/", params, methods),
            SalidaPost: $resource(url + "salida/crear/:id/", params, methods),
            CompraDetalleJsonDetail: $resource(url + "compra_detalle/detailjson/:id/", params, methods),

        };
    }
}());