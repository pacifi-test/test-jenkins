(function () {
    angular.module("myApp")
        .controller("ventaDetailCtrl", ventaDetailCtrl);

    function ventaDetailCtrl() {
        var self = this;


        self.exportPdf = function () {

            var columns = [
                {title: "Código", dataKey: "codigo"},
                {title: "Cód. Tributario", dataKey: "codigo_tributario"},
                {title: "Razón Social", dataKey: "razon_social"},
                {title: "Nombre", dataKey: "cliente_nombre"},
                {title: "Tipo", dataKey: "tipo_cliente_nombre"},
                {title: "Dirección", dataKey: "direccion"},
                {title: "Teléfono", dataKey: "telefono"},

            ];
            var rows = self.clientes;

            // Only pt supported (not mm or in)
            var doc = new jsPDF('landscape');

            doc.setFontSize(10);
            doc.text(35, 25, "CLIENTES");
            doc.autoTable(columns, rows,
                {
                    margin: {top: 30},
                }
            );
            doc.save('clientes.pdf');
        }
    }
}());