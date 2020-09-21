(function () {
    'use strict';
    // Convertir a excel
    angular
        .module('myApp')
        .factory('Convert', Convert);

    /** @ngInject */
    function Convert(FileSaver) {

        return {
            ToExcel: toExcel
        };

        function toExcel(document, name) {
            var header = '<meta http-equiv="content-type" content="application/vnd.ms-excel; charset=UTF-8">';
            var blob = new Blob([header + document], {
                type: "data:application/vnd.ms-excel;charset=UTF-8"
            });
            return FileSaver.saveAs(blob, name + ".xls");

        }
    }

}());