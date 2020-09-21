(function () {
    angular.module("myApp").controller('equipoCtrl', equipoCtrl);

    equipoCtrl.$inject = ["AlmacenService", "$q", "$location", "toastr"];

    function equipoCtrl(AlmacenService, $q, $location, toastr) {

        var self = this;
        self.contable = true;
        self.focusAdd = false;
        self.equipos = [];
        self.animationsEnabled = true;

        init();

        function init() {
            self.producto_id = angular.element(document.querySelector('#producto_id')).val();
            var promises = [loadProducto()];
            return $q.all(promises).then(function () {
            });
        }

        function loadProducto() {
            AlmacenService.Producto.get({id: self.producto_id}, function (r) {
                self.producto = r;
                console.log(self.producto);
            });
        }

        self.addEquipo = function () {
            self.equipo = {
                'imei': self.imei,

            };
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
        };

        self.removeEquipo = function (item) {
            var index = self.equipos.indexOf(item);
            self.equipos.splice(index, 1);

        };

        self.enviarEquipos = function () {
            AlmacenService.Equipo.save({
                'contable': self.contable,
                'equipos': self.equipos,
                'producto_id': self.producto_id
            }, function (r) {
                console.log(r);
                toastr.success("Ingreso Satisfactorio");
                loadProducto();
                location.href = "/almacen/producto/listar";
                self.focusAdd = true;
                self.imei = '';
                self.equipos = [];
            }, function (err) {
                self.imei = '';
                self.focusAdd = true;
                toastr.error("No se puede Registrar Verifique Imei", err);
                console.log(err);
            });
        };


        self.multiConfirmationDialog = function () {

            self.confirmationDialogConfig = {
                title: "Seleccione la Operación a Realizar...",
                message: "Verifique bien su operación.",
                buttons: [{
                    label: "Contable",
                    class: "btn-primary",
                    action: 'functioncontable'
                }, {
                    label: "No Contable",
                    class: "btn-warning",
                    action: 'functionnocontable'
                }
                ]
            };
            self.showDialog(true);
        };

        self.functioncontable = function () {
            self.contable = true;
            self.enviarEquipos()
            self.showDialog();
        };
        self.functionnocontable = function () {
            self.contable = false;
            self.enviarEquipos()
            self.showDialog();
        };
        self.executeDialogAction = function (action) {
            if (typeof self[action] === "function") {
                self[action]();
            }
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