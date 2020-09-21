from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Layout, Div, Field
from django import forms

from backend_apps.utils.forms import smtSave, btnCancel
from ..models.precio_venta import PrecioVenta


class PrecioVentaForm(forms.ModelForm):
    class Meta:
        model = PrecioVenta
        exclude = ("producto_general", "estado", "user", "created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('url', None)

        super(PrecioVentaForm, self).__init__(*args, **kwargs)
        # self.fields['fecha_emision'] = DateField(input_formats=['%d/%m/%Y'], widget=forms.DateTimeInput(attrs={
        #     'class': 'form-control datetimepicker-input',
        #     'data-target': '#datetimepicker1'
        # }))

        self.helper = FormHelper()
        self.helper.attrs['autocomplete'] = "off"
        self.helper.form_method = 'post'
        self.helper.form_action = self.request
        self.helper.form_class = 'js-validate form-vertical'

        self.helper.layout = Layout(
            Row(Div(Field('ruta', css_class='input-required'),
                    css_class='col-md-4'),
                Div(Field('precio', css_class='input-required'),
                    css_class='col-md-4'),
                ),

            Row(
                FormActions(
                    smtSave(),

                ),
            ),
        )
