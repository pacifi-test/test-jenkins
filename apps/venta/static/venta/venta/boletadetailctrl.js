(function () {
    angular.module("myApp")
        .controller("boletaCtrl", boletaCtrl);

    function boletaCtrl(Servicio) {
        var self = this;


        self.exportPdf = function (item) {
            Servicio.VentaGet.get({'venta_id': item}, function (r) {
                self.data = r;


                var columns = [
                    {title: "Descripción", dataKey: "descripcion"},
                    {title: "Cantidad", dataKey: "cantidad"},

                    {title: "Precio Unitario", dataKey: "precio_unitario"},

                    // {title: "Base Imponible", dataKey: "base_imponible"},

                    // {title: "Igv", dataKey: "igv"},
                    {title: "Precio Total", dataKey: "precio_total"},
                ];
                var rows = self.data.items;

                // Only pt supported (not mm or in)
                const doc = new jsPDF({
                    orientation: "p",
                    unit: "pt",
                    format: "a4",

                });
                doc.setProperties({
                    title: "new Report"
                });
                doc.setFontSize(14);
                doc.text(110, 35, self.data.empresa);

                doc.setLineWidth(2);
                doc.rect(435, 40, 120, 60);
                doc.setFontSize(12);
                doc.text(450, 55, "Boleta de Venta");
                doc.text(465, 68, "Electronica");

                doc.text(453, 81, "RUC: " + self.data.nro_ruc);
                doc.text(480, 92, self.data.serie_numero);

                doc.line(0, 125, 595, 125);

                //Cliente
                doc.setFontSize(8);
                doc.setFontType('bold');
                doc.text(40, 145, "Cliente");
                doc.text(40, 155, "Dirección");
                doc.text(40, 165, "Documento");
                doc.text(40, 175, "Fecha de Emisión");
                doc.text(240, 175, "Moneda");

                doc.setFontType('normal');
                doc.text(150, 145, ": " + self.data.cliente.nombre_completo);
                doc.text(150, 155, ": " + self.data.cliente.direccion);


                doc.text(150, 165, ": " + self.data.cliente.tipo_documento + " " + self.data.cliente.nro_documento);
                doc.text(150, 175, ": " + self.data.fecha);
                doc.text(300, 175, ": " + "Sol");


                // doc.addImage(self.qr_img, 'PNG', 15, 40, 180, 160);
                doc.autoTable(columns, rows,
                    {
                        startY: 200,
                        "styles": {
                            "overflow": "linebreak",
                            // "cellWidth": "wrap",
                            // "rowPageBreak": "avoid",
                            "halign": "justify",
                            "fontSize": "8",
                            "lineColor": "100",

                        },
                        columnStyles: {
                            'descripcion': {
                                font: 'courier',
                                cellWidth: 350
                            },

                        },

                        "theme": 'striped',
                        "pageBreak": "auto",
                        "tableWidth": "auto",
                        "showHead": "everyPage",
                        "showFoot": "everyPage",
                        "tableLineWidth": 0,
                        "tableLineColor": 200,
                        "margin": {"top": 30},
                    }
                );


                doc.addImage(self.data.qr_img, 'PNG', 200, 600, 50, 50);


                // doc.save('venta.pdf');
                // doc.output('save', 'filename.pdf');
                doc.output('dataurlnewwindow');


            });


        };
    }
}());

// https://chaturbate.com/sexybeth1248/
// https://chaturbate.com/_blackbee_/