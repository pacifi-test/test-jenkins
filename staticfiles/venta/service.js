(function () {
    "use strict";
    angular.module("myApp")
        .factory("VentaService", ["$resource", VentaService]);

    function VentaService($resource) {
        var url = "/venta";
        var params = {'id': '@id'};
        var methods = {"update": {method: 'PUT'}};
        return {

            VentaCrear: $resource(url + "/venta/crear/:id/", params, methods),
            TipoComprobanteGet: $resource(url + "/equipo/get/:id/", params, methods),

        };
    }
}());