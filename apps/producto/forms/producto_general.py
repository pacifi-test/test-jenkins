from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field, Fieldset
from dal import autocomplete
from django import forms

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.marca import Marca
from ..models.producto import Producto
from ..models.producto_general import ProductoGeneral


class ProductoGeneralForm(forms.ModelForm):
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        widget=autocomplete.ModelSelect2(url='producto:marca_autocomplete', attrs={
            'data-placeholder': 'Marca',
        })
    )
    precio_local_id = forms.CharField(widget=forms.HiddenInput(), required=False, )
    precio_regional_id = forms.CharField(widget=forms.HiddenInput(), required=False, )
    precio_nacional_id = forms.CharField(widget=forms.HiddenInput(), required=False, )

    class Meta:
        model = ProductoGeneral
        exclude = ("created_at", "updated_at", 'slug',)

    def __init__(self, *args, **kwargs):
        super(ProductoGeneralForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 2
        self.fields['precio_local'] = forms.DecimalField(label="Precio Local")
        self.fields['precio_regional'] = forms.DecimalField(label="Precio Regional")
        self.fields['precio_nacional'] = forms.DecimalField(label="Precio Nacional")
        self.helper = FormHelper()
        self.helper.attrs['autocomplete'] = "off"
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Fieldset('Producto', Row(
                Div(Field('marca', css_class='input-required'),
                    css_class='col-md-3'),
                Div(Field('codigo', css_class='input-required'),
                    css_class='col-md-3'),
                Div(Field('descripcion', css_class='input-required '),
                    css_class='col-md-3'),
                Div(Field('imagen', ),
                    css_class='col-md-3'),
            ), ),
            Fieldset('Precios',
                     Field('precio_local_id'),
                     Field('precio_regional_id'),
                     Field('precio_nacional_id'),
                     Row(
                         Div(Field('precio_local', css_class='input-required'),
                             css_class='col-md-4'),
                         Div(Field('precio_regional', css_class='input-required'),
                             css_class='col-md-4'),
                         Div(Field('precio_nacional', css_class='input-required'),
                             css_class='col-md-4'),
                     )

                     ),

            Row(
                FormActions(
                    smtSave(msg="Guardar"),
                    btnCancel(),
                ),
            ),
        )
