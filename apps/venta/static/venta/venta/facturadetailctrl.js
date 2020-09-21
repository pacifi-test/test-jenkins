(function () {
    angular.module("myApp")
        .controller("facturaDetailCtrl", facturaDetailCtrl);

    function facturaDetailCtrl(Servicio) {
        var self = this;


        self.exportPdf = function (item) {
            Servicio.VentaGet.get({'venta_id': item}, function (r) {
                self.data = r;
                console.log(r);
                var columns = [
                    {title: "Cantidad", dataKey: "cantidad"},
                    {title: "Código", dataKey: "codigo"},
                    {title: "Descripción", dataKey: "descripcion"},
                    {title: "Precio Unitario", dataKey: "precio_unitario"},
                    {title: "Base I,", dataKey: "base_imponible"},
                    {title: "Total", dataKey: "precio_total"},

                ];
                var rows = self.data.items;

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

            });


        };
    }
}());