from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field
from django import forms

from backend_apps.utils.forms import smtSave, btnCancel, btnReset
from ..models.departamento import Departamento
from ..models.proveedor import Proveedor
from ..models.provincia import Provincia


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        exclude = ('created_at', 'updated_at', "user")

    def clean_nro_documento(self):
        cleaned_data = super(ProveedorForm, self).clean()
        tipo_documento_identidad = cleaned_data.get("tipo_documento_identidad")
        nro_documento = cleaned_data.get("nro_documento")
        try:
            int(nro_documento)
        except:
            raise forms.ValidationError(u"No es número")
        if tipo_documento_identidad.codigo == '1':  # es dni
            if len(str(nro_documento)) != 8:
                raise forms.ValidationError('No son 8 Digitos para DNI')
        if tipo_documento_identidad.codigo == '6':  # es RUnc
            if len(str(nro_documento)) != 11:
                raise forms.ValidationError('No son 11 Digitos para RUC')
        if tipo_documento_identidad.codigo == '6':  # es RUnc
            if len(str(nro_documento)) != 4:
                raise forms.ValidationError('No son 11 Digitos para C.E.')

        return nro_documento

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
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
                Div(Field('razon_social', css_class='input-required'),
                    css_class='col-md-4'),
                Div(Field('tipo_documento_identidad', css_class='input-required'),
                    css_class='col-md-4'),
                Div(Field('nro_documento', css_class='input-required'),
                    css_class='col-md-4'),
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
                    smtSave(),
                    btnCancel(),
                ),
            ),
        )
