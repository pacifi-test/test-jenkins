from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field
from django import forms

from backend_apps.utils.forms import smtSave, btnCancel
from ..models.equipo import Equipo



class EquipoUpdateModelForm(forms.ModelForm):
    u"""Aun no esta en uso"""

    class Meta:
        model = Equipo
        exclude = ("id", "created_at", "updated_at", "user", "producto", "estado", "compra_detalle", "imei")

    def __init__(self, *args, **kwargs):
        super(EquipoUpdateModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs['autocomplete'] = "off"
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('contable'),
                    css_class='col-md-4'),
            ),

            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                ),
            ),
        )
