from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field
from django import forms

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.marca import Marca


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        exclude = ('created_at', 'updated_at',)

    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs['autocomplete'] = "off"
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('nombre', css_class='input-required'),
                    css_class='col-md-4'),

            ),

            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                ),
            ),
        )
