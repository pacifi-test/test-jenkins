from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field
from django import forms

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.cliente import Cliente
from ..models.departamento import Departamento
from ..models.provincia import Provincia


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ('created_at', 'updated_at', "user", "es_juridico")

    def clean_nro_documento(self):
        cleaned_data = super(ClienteForm, self).clean()
        tipo_documento = cleaned_data.get("tipo_documento")
        nro_documento = cleaned_data.get("nro_documento")
        try:
            int(nro_documento)
        except:
            raise forms.ValidationError(u"No es número")
        if tipo_documento.codigo == '1':  # es dni
            if len(str(nro_documento)) != 8:
                raise forms.ValidationError('No son 8 Digitos para DNI')
        if tipo_documento.codigo == '6':  # es RUnc
            if len(str(nro_documento)) != 11:
                raise forms.ValidationError('No son 11 Digitos para RUC')

        return nro_documento

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = forms.ModelChoiceField(
            label="Departamento", required=False,
            queryset=Departamento.objects.all(),
            help_text=u'<small class="help-error"></small> %s' %
                      u' ',
        )
        self.fields['provincia'] = forms.ModelChoiceField(
            label="Provincia", required=False,
            queryset=Provincia.objects.all(),
            help_text=u'<small class="help-error"></small> %s' %
                      u' ',
        )
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs['autocomplete'] = "off"
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('nombres', css_class='input-required'), css_class='col-md-3'),
                Div(Field('apellidos', ), css_class='col-md-3'),
                Div(Field('tipo_documento', css_class='input-required'), css_class='col-md-3'),
                Div(Field('nro_documento', css_class='input-required'), css_class='col-md-3'),
            ),
            Row(
                Div(Field('departamento', css_class='input-required'), css_class='col-md-2'),
                Div(Field('provincia', css_class='input-required'), css_class='col-md-2'),
                Div(Field('lugar', css_class='input-required'), css_class='col-md-2', ),

                Div(Field('direccion', css_class='input-required'), css_class='col-md-3'),
                Div(Field('nro_telefono', css_class='input-required'), css_class='col-md-3'),
            ),

            Row(
                FormActions(
                    smtSave("Guardar"),
                    btnCancel(),
                ),
            ),
        )
