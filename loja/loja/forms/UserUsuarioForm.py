from django.forms import ModelForm
from django import forms
from django.utils import timezone
from loja.models.Usuario import Usuario
from django.contrib.auth.models import User

class UserUsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['user', 'perfil', 'aniversario']
        widgets = {
            'user': forms.HiddenInput(),
            'perfil': forms.Select(attrs={'class': "form-control"}),
            'aniversario': forms.DateInput(attrs={'class': "form-control", "type": "date"}),
        }

    def clean_aniversario(self):
        aniversario = self.cleaned_data.get('aniversario')
        if aniversario and aniversario > timezone.localdate():
            raise forms.ValidationError('A data de aniversário não pode ser no futuro.')
        return aniversario


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este e-mail já está sendo usado por outro usuário.')
        return email