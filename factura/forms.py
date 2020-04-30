from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre','apellidos','tipo',
                  'celular', 'estado']
        exclude = ['user_modification','modificado','user', 'creado']
        widget = {'descripcion': forms.TextInput()}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in iter(self.fields):
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
