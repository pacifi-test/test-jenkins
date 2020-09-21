from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field, Fieldset
from dal import autocomplete
from django import forms
from django.forms import DateField

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.compra import Compra
from ...persona.models.proveedor import Proveedor
from ...sunat.models.tipo_comprobante_pago import TipoComprobantePago


class CompraForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        widget=autocomplete.ModelSelect2(url='compra:proveedor_autocomplete', attrs={
            'data-placeholder': 'Proveedor',
        })
    )

    class Meta:
        model = Compra
        exclude = (
            "user", "created_at", "updated_at", "nro_correlativo", "codigo_aduana", "estado", "procesado", "contable",
            "periodo")

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        # self.fields['fecha_emision'] = DateField(input_formats=['%d/%m/%Y'], widget=forms.DateTimeInput(attrs={
        #     'class': 'form-control datetimepicker-input',
        #     'data-target': '#datetimepicker1'
        # }))
        codigos_comprobante = ["01", "03", "99"]
        self.fields['fecha_emision'] = DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }))

        self.fields['fecha_vencimiento'] = DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }))
        codigos_comprobante = ["01", "03", "99"]
        self.fields['tipo_comprobante'].queryset = TipoComprobantePago.objects.filter(codigo__in=codigos_comprobante)

        # self.fields['proveedor'].widget = autocomplete.ModelSelect2(url='compra:proveedor_autocomplete',)
        self.fields['base_imponible'].widget.attrs['readonly'] = True
        self.fields['igv'].widget.attrs['readonly'] = True
        # self.fields['fecha_vencimiento'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.attrs['autocomplete'] = "off"
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'

        self.helper.layout = Layout(

            Row(
                Fieldset("Comprobate",
                         Div(Field('proveedor', css_class='input-required'),
                             css_class='col-md-3'),
                         Div(Field('serie_comprobante', css_class='input-required'),
                             css_class='col-md-2'),
                         Div(Field('nro_comprobante', css_class='input-required'),
                             css_class='col-md-3'),
                         Div(Field('fecha_emision', css_class='input-required'),
                             css_class='col-md-2'),
                         Div(Field('fecha_vencimiento', ),
                             css_class='col-md-2'), css_class="scheduler-border",
                         )
            ),
            Fieldset("Pago",

                     Row(
                         Div(Field('tipo_comprobante', css_class='input-required'),
                             css_class='col-md-4'),
                         Div(Field('tipo_moneda', css_class='input-required'),
                             css_class='col-md-2'),

                         Div(Field('total', css_class='input-required'),
                             css_class='col-md-2'),
                         Div(Field('base_imponible', css_class='input-required'),
                             css_class='col-md-2'),
                         Div(Field('igv', css_class='input-required'),
                             css_class='col-md-2'), css_class="scheduler-border"
                     ),
                     ),

            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                ),
            ),
        )


class CompraUpdateForm(forms.ModelForm):
    class Meta:
        model = Compra
        exclude = (
            "user", "created_at", "periodo", "updated_at", "nro_correlativo", "codigo_aduana", "estado", "procesado")

    def __init__(self, *args, **kwargs):
        url = kwargs.pop('url', None)
        compra = kwargs.pop('compra', None)

        super(CompraUpdateForm, self).__init__(*args, **kwargs)
        self.fields['base_imponible'].widget.attrs['readonly'] = True
        self.fields['igv'].widget.attrs['readonly'] = True

        codigos_comprobante = ["01", "03", "99"]
        self.fields['tipo_comprobante'].queryset = TipoComprobantePago.objects.filter(codigo__in=codigos_comprobante)

        self.fields['fecha_emision'] = DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }, format='%d/%m/%Y'))
        self.fields['fecha_vencimiento'] = DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }, format='%d/%m/%Y'))

        # self.fields['fecha_vencimiento'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = url
        self.helper.form_class = 'js-validate form-vertical'

        self.helper.layout = Layout(
            Row(
                Div(Field('proveedor', css_class='input-required'),
                    css_class='col-md-4'),
                Div(Field('tipo_comprobante', css_class='input-required'),
                    css_class='col-md-4'),
                Div(Field('tipo_moneda', css_class='input-required'),
                    css_class='col-md-4'),
            ),
            Row(
                Div(Field('fecha_emision', css_class='input-required'),
                    css_class='col-md-3'),
                Div(Field('fecha_vencimiento', css_class='input-required'),
                    css_class='col-md-3'),
                Div(Field('serie_comprobante', css_class='input-required'),
                    css_class='col-md-2'),
                Div(Field('nro_comprobante', css_class='input-required'),
                    css_class='col-md-4'),

            ),
            Row(
                Div(Field('base_imponible', css_class='input-required'),
                    css_class='col-md-4'),
                Div(Field('igv', css_class='input-required'),
                    css_class='col-md-4'),
                Div(Field('total', css_class='input-required'),
                    css_class='col-md-4'),

            ),

            Row(
                FormActions(
                    smtSave("Actualizar"),
                ), css_class="text-center"
            ),
        )
