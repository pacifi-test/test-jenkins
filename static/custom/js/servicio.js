(function () {
    "use strict";
    angular.module("myApp")
        .factory("Servicio", ["$resource", Servicio]);

    function Servicio($resource) {
        var url = "/servicio";

        var params = {'id': '@id'};
        var methods = {"update": {method: 'PUT'}};
        return {
            ClienteListGet: $resource(url + "/cliente/list_get/:id/", params, methods),
            TipoComprobanteListGet: $resource(url + "/tipo_comprobante/list_get/:id/", params, methods),
            UserListGet: $resource(url + "/user/list_get/:id/", params, methods),
            VentaGet: $resource(url + "/venta/get/:id/", params, methods),
            ProductoListGet: $resource(url + "/producto/list_get/:id/", params, methods),

        };
    }
}());