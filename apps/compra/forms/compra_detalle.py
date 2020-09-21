from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Field, HTML
from dal import autocomplete
from django import forms

from ..models.compra_detalle import CompraDetalle
from ...producto.models.producto_general import ProductoGeneral


class CompraDetalleForm(forms.ModelForm):
    producto_general = forms.ModelChoiceField(
        queryset=ProductoGeneral.objects.all(),
        widget=autocomplete.ModelSelect2(url='compra:producto_autocomplete', attrs={
            'data-placeholder': 'Producto',
        })
    )

    class Meta:
        model = CompraDetalle
        exclude = ("created_at", "updated_at", "user", "compra", "igv", "total")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('url', None)
        super(CompraDetalleForm, self).__init__(*args, **kwargs)
        self.fields['precio_unitario'].widget.attrs['readonly'] = True
        self.fields['igv_total'].widget.attrs['readonly'] = True
        self.fields['precio_total'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.attrs['autocomplete'] = "off"
        self.helper.form_method = 'post'
        self.helper.form_action = self.request
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('producto_general', css_class="input-required"),
                    css_class='col-md-3'),
                Div(Field('cantidad', css_class="input-required"),
                    css_class='col-md-1'),
                Div(Field('valor_unitario', css_class="input-required"),
                    css_class='col-md-2'),
                Div(Field('precio_unitario', css_class="input-required"),
                    css_class='col-md-2'),
                Div(Field('igv_total', css_class="input-required"),
                    css_class='col-md-1'),
                Div(Field('precio_total', css_class="input-required"),
                    css_class='col-md-2'),
                Div(HTML(
                    "<button class='btn btn-primary'  id='detalle_save_id' type='submit'><i class='fa fa-save'></i></button>")
                    , css_class='col-md-1'),

            ),

        )
