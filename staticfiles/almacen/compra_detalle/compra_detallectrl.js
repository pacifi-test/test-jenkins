(function () {
    angular.module("myApp").controller('compraDetalleCtrl', compraDetalleCtrl);

    compraDetalleCtrl.$inject = ["AlmacenService", "$q", "$location", "toastr", "Servicio"];

    function compraDetalleCtrl(AlmacenService, $q, $location, toastr, Servicio) {

        var self = this;
        self.contable = true;
        self.focusAdd = false;
        self.equipos = [];
        self.animationsEnabled = true;

        init();

        function init() {
            self.producto_id = angular.element(document.querySelector('#producto_id')).val();
            self.producto_general_codigo = angular.element(document.querySelector('#producto_general_codigo_id')).val();
            self.compra_detalle_id = angular.element(document.querySelector('#compra_detalle_id')).val();

            var promises = [loadCompraDetail()];
            return $q.all(promises).then(function () {
            });
        }


        function loadCompraDetail() {
            AlmacenService.CompraDetalleJsonDetail.get({"compra_detalle_id": self.compra_detalle_id}, function (r) {
                self.compra_detalle_detalles = r;
                self.cantidad = self.compra_detalle_detalles.cantidad;
                self.registrados = self.compra_detalle_detalles.registrados;
                self.contable = self.compra_detalle_detalles.contable;
            });
        }

        self.addEquipo = function () {
            self.equipo = {
                'imei': self.imei,

            };
            if ((self.equipos.length + self.registrados) < self.cantidad) {
                if (buscarRepetido(self.equipos, self.equipo)) {
                    self.focusAdd = true;
                    self.imei = '';
                    toastr.error("Equipo Repetido");
                } else {
                    AlmacenService.EquipoGet.get({'imei': self.imei}, function (r) {

                        toastr.error("Imei repetido en base de datos");
                        self.focusAdd = true;
                        self.imei = '';
                    }, function (r) {
                        self.equipos.unshift(self.equipo);
                        self.focusAdd = true;
                        self.imei = '';
                        toastr.success(self.equipo.imei, 'Equipo Agregado');
                        self.focusAdd = true;
                        self.imei = '';
                    });

                }
            } else {
                toastr.info("Equipos Completos", "Productos completados");
            }
        };

        self.removeEquipo = function (item) {
            var index = self.equipos.indexOf(item);
            self.equipos.splice(index, 1);

        };

        self.enviarEquipos = function () {
            AlmacenService.Equipo.save({
                'contable': self.contable,
                'equipos': self.equipos,
                'producto_id': self.producto_id,
                'compra_detalle_id': self.compra_detalle_id
            }, function (r) {
                console.log(r);
                toastr.success("Ingreso Satisfactorio");
                loadCompraDetail();
                self.focusAdd = true;
                self.imei = '';
                self.equipos = [];
            }, function (err) {
                self.imei = '';
                self.focusAdd = true;
                toastr.error("No se puede Registrar Verifique Imei");
            });
        };


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

        self.showDialog = function (flag) {
            jQuery("#confirmation-dialog .modal").modal(flag ? 'show' : 'hide');
        };
    }
}());