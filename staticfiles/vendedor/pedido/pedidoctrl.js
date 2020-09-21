(function () {
    'use strict';
    angular.module("myApp")
        .controller("pedidoCtrl", pedidoCtrl);
    pedidoCtrl.$inject = ["VendedorService", "toastr", "$q", "Servicio", "$window"];

    function pedidoCtrl(VendedorService, toastr, $q, Servicio, $window) {
        var self = this;
        self.productos_seleccionados = [];
        self.producto = undefined;
        self.ruta = undefined;
        self.total = 0;
        init();

        function init() {
            var promises = [loadProductos(), loadCliente()];
            return $q.all(promises).then(function () {
            });
        }


        self.addProducto = function () {


            self.productos_seleccionados.unshift(
                {
                    "producto": self.producto,
                    "cantidad": self.cantidad,
                    "precio_total": self.cantidad * self.producto.precio,
                }
            );
            self.producto = undefined;
            self.cantidad = '';
            self.producto_codigo = '';
            calcularPrecio(self.productos_seleccionados);
        };

        self.selectCliente = function (item) {
            self.cliente = item;

        };

        self.removeProducto = function (item) {
            var index = self.productos_seleccionados.indexOf(item);
            self.productos_seleccionados.splice(index, 1);
            calcularPrecio(self.productos_seleccionados);
        };


        self.buscarProducto = function (item) {

            VendedorService.Producto.get({"producto_codigo": self.producto_codigo, "ruta": self.ruta},
                function (r) {
                    self.producto = r;
                    toastr.success(self.producto, "Producto encontrado");
                }, function (error) {
                    toastr.error(error.data.message, "Error");
                });
        };

        self.realizarPedido = function () {
            VendedorService.PedidoCrear.save({
                "cliente": self.cliente,
                "productos": self.productos_seleccionados,
                "ruta": self.ruta,
            }, function (r) {
                toastr.success("mensaje", "Producto Guardadao");
                $window.location.href = "/vendedor/pedido/detallar/" + r.id;
            }, function (error) {
                toastr.error(error.data.message, "Error al realizar el pedido");
            });
        };

        function loadProductos() {
            VendedorService.Producto.query(function (r) {
                self.productos = r;

            });
        }

        function loadCliente() {
            Servicio.ClienteListGet.query(function (r) {
                self.clientes = r;
            });
        }

        function calcularPrecio(productos) {
            self.total = 0;
            productos.forEach(function (producto) {
                self.total = self.total + producto.precio_total;
                console.log("calcular precio");
                console.log(self.total);
            });
        }
    }
}());