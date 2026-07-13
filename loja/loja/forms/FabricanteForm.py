from django import forms
from django.forms import ModelForm
from loja.models import Fabricante 

class FabricanteForm(ModelForm):
    class Meta:
        model = Fabricante
        fields = '__all__'
        widgets = {
            'Fabricante': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_Fabricante(self):
        nome = self.cleaned_data.get('Fabricante')
        if Fabricante.objects.filter(Fabricante__iexact=nome).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Já existe um fabricante registrado com este nome.')
        return nome