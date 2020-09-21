(function () {
    angular.module("myApp").controller('ventaCtrl', ventaCtrl);
    ventaCtrl.$inject = ["$http", "VentaService", "$q", "toastr", "$window"];

    function ventaCtrl($http, VentaService, $q, toastr, $window) {
        var self = this;
        self.equipos = [];
        self.precio_total = 0;
        self.focusAdd = false;

        init();

        function init() {
            var promises = [loadComprobantes()];
            return $q.all(promises).then(function () {
            });
        }

        function loadComprobantes() {
            VentaService.TipoComprobante.query(function (r) {
                self.tipo_comprobantes = r;
                console.log(r);
            });
        }

        self.buscarCliente = function (codigo) {
            VentaService.Cliente.get({'codigo': codigo}, function (r) {
                self.cliente = r;
            });
        };

        self.realizarVenta = function () {
            VentaService.Preventa.save({
                "cliente": self.cliente,
                "equipos": self.equipos,
                'tipo_comprobante': self.tipo_comprobante,

            }, function (r) {
                toastr.success("Venta Realizada");
                console.log(r.id);
                $window.location.href = "/venta/preventa/detallar/" + r.id;

            }, function (err) {
                console.log(err);
                // $window.location.href = "/venta/preventa/detail/91992929291010";
            });
        };

        self.buscarEquipo = function (imei) {
            VentaService.Equipo.get({'codigo': imei}, function (r) {
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
                toastr.error("Equipo no disponible");
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
            console.log("calculando");
            self.precio_total = 0;
            equipos.forEach(function (item, index) {
                self.precio_total = self.precio_total + item.precio_venta;
            });
        }

        function buscarRepetido(equipos, equipo) {
            console.log("busncando repetido");
            repetido = false;
            equipos.forEach(function (item, idenx) {
                if (item.imei === equipo.imei) {
                    repetido = true;
                }
                return repetido;
            });
            return repetido;

        }

    }
}());