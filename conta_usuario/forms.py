from django import forms
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.Form):
    usuario = forms.CharField(max_length=20, label='Usuário')
    senha = forms.CharField(max_length=30, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=30)
    nome = forms.CharField(max_length=20)
    sobrenome = forms.CharField(max_length=30)

    def validating_password(self):
        senha = self.cleaned_data['senha']
        validate_password(senha)


class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=20, label='Usuário')
    senha = forms.CharField(max_length=30, widget=forms.PasswordInput())
