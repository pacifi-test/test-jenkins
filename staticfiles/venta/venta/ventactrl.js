(function () {
    angular.module("myApp").controller('ventaCtrl', ventaCtrl);
    ventaCtrl.$inject = ["$http", "VentaService", "$q", "toastr", "$window", "Servicio"];

    function ventaCtrl($http, VentaService, $q, toastr, $window, Servicio) {
        var self = this;
        self.equipos = [];
        self.precio_total = 0;
        self.focusAdd = false;
        self.ruta = undefined;

        init();

        function init() {
            var promises = [loadDistrobuidores(), loadClientes()];
            return $q.all(promises).then(function () {
            });
        }


        self.selectCliente = function (item) {
            self.cliente = item;

        };
        self.selectDistribuidor = function (item) {
            self.distribuidor = item
        };

        self.realizarVenta = function () {
            VentaService.VentaCrear.save({
                "cliente": self.cliente,
                "equipos": self.equipos,
                'tipo_comprobante': self.tipo_comprobante,
                'ruta': self.ruta,
                'distribuidor': self.distribuidor

            }, function (r) {
                toastr.success("Venta Realizada");

                $window.location.href = "/venta/venta/detallar/" + r.id;

            }, function (err) {
                console.log(err);
                toastr.error(err.data.message, "Error al realizar Venta");
                // $window.location.href = "/venta/preventa/detail/91992929291010";
            });
        };

        self.buscarEquipo = function (imei) {
            VentaService.TipoComprobanteGet.get({
                    'imei': imei,
                    'estado': 'ALMACEN',
                    'ruta': self.ruta
                },
                function (r) {
                    self.equipo = r;
                    if (buscarRepetido(self.equipos, self.equipo)) {
                        self.focusAdd = true;
                        self.imei = '';
                        toastr.error("Equipo Repetido");
                    } else {
                        self.equipos.push(self.equipo);
                        self.focusAdd = true;
                        self.imei = '';
                        toastr.success(self.equipo.imei, 'Equipo Agregado');
                    }
                    calcularPrecio(self.equipos);
                }, function (r) {
                    toastr.error(r.data.message, "Equipo no disponible");
                    self.focusAdd = true;
                    self.imei = '';
                });
        };

        self.removeEquipo = function (item) {
            var index = self.equipos.indexOf(item);
            self.equipos.splice(index, 1);
            calcularPrecio(self.equipos);
        };

        function calcularPrecio(equipos) {

            self.precio_total = 0;
            equipos.forEach(function (item, index) {
                self.precio_total = self.precio_total + item.precio_venta;
            });
        }

        function buscarRepetido(equipos, equipo) {

            repetido = false;
            equipos.forEach(function (item, idenx) {
                if (item.imei === equipo.imei) {
                    repetido = true;
                }
                return repetido;
            });
            return repetido;

        }


        self.tipo_comprobantes = [
            {
                "codigo": "01",
                "descripcion": "Factura"
            },
            {
                "codigo": "03",
                "descripcion": "Boleta de Venta"
            },
            {
                "codigo": "99",
                "descripcion": "Recibo Simple"
            },
        ];


        function loadClientes() {
            Servicio.ClienteListGet.query(function (r) {
                self.clientes = r;

            });
        }

        function loadDistrobuidores() {
            Servicio.UserListGet.query({"rol": "DISTRIBUIDOR"}, function (r) {
                self.distruibuidores = r;

            });
        }
    }
}());