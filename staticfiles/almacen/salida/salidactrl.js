(function () {
    angular.module("myApp")
        .controller("salidaCtrl", salidaCtrl);
    salidaCtrl.$inject = ["AlmacenService", "toastr", "$window"];

    function salidaCtrl(AlmacenService, toastr, $window) {
        self = this;
        self.equipos = [];

        self.salidaSave = function () {
            AlmacenService.SalidaPost.save({
                "distribuidor": self.distribuidor,
                "ruta": self.ruta,
                "equipos": self.equipos
            }, function (r) {
                $window.location.href = "/almacen/salida/detallar/" + r.id;
            }, function (error) {
                console.log(error);
            });
        };

        self.buscarEquipo = function () {
            AlmacenService.EquipoGet.get({'imei': self.imei, 'estado': 'ALMACEN'}, function (r) {
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

            }, function (r) {
                toastr.error("Equipo no disponible");
                self.focusAdd = true;
                self.imei = '';
            });
        };

        self.removeEquipo = function (item) {
            var index = self.equipos.indexOf(item);
            self.equipos.splice(index, 1);

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

    }


}());