from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class RegistrarForm(forms.Form):
    usuario = forms.CharField(max_length=20, label='Usuário')
    senha = forms.CharField(max_length=30, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=30)

    def validar_senha(self):
        senha = self.cleaned_data.get('senha')

        if len(senha) < 6:
            raise ValidationError('A senha deve ter pelo menos 6 caracteres.')

    def registrar_usuario(self):
        usuario, senha, email = self.cleaned_data.values()

        if User.objects.filter(username=usuario).exists():
            raise ValidationError('Esse nome de usuário já está em uso.')

        else:
            user = User.objects.create_user(username=usuario, password=senha, email=email)
            return user


class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=20, label='Usuário')
    senha = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def autenticar_usuario(self, request):
        usuario, senha = self.cleaned_data.values()
        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            return user
        
        else:
            raise ValidationError('Usuário ou senha incorretos.')


class AlterarSenhaForm(forms.Form):
    antiga_senha = forms.CharField(max_length=30, label='Antiga senha')
    nova_senha = forms.CharField(max_length=30, label='Nova senha')
    confirmar_senha = forms.CharField(max_length=30, label='Confirmar nova senha')

    def verificar_senhas(self):
        antiga_senha, senha, senha_confirmacao = self.cleaned_data
        validate_password(senha)

        if senha == senha_confirmacao:
            pass
        else:
            raise ValidationError('Senha diferente.')
