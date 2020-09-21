from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field
from django import forms

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.producto import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ("created_at", "updated_at", 'slug', "codigo_general", 'imagen', 'marca')

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.helper = FormHelper()
        self.helper.attrs['autocomplete'] = "off"
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('producto_general', css_class='input-required'),
                    css_class='col-md-2'),
                Div(Field('color', css_class='form_control'),
                    css_class='col-md-2'),
                Div(Field('codigo', css_class='input-required'),
                    css_class='col-md-2'),

            ),

            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )


class ProductoSimpleForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = (
        "created_at", "updated_at", 'slug', "codigo_general", 'imagen', 'marca', 'producto_general', 'codigo')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('url', None)
        super(ProductoSimpleForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 3
        self.helper = FormHelper()
        self.helper.attrs['autocomplete'] = "off"
        self.helper.form_action = self.request
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(

                Div(Field('color', css_class='form_control'),
                    css_class='col-md-6'),

            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                ),
            ),
        )
