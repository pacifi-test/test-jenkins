(function () {
    "use strict";
    angular.module("myApp")
        .factory("VendedorService", ["$resource", VendedorService]);

    function VendedorService($resource) {
        var url = "/vendedor";

        var params = {'id': '@id'};
        var methods = {"update": {method: 'PUT'}};
        return {
            Producto: $resource(url + "/producto/listar/:id/", params, methods),
            PedidoCrear: $resource(url + "/pedido/crear/:id/", params, methods),
        };
    }
}());