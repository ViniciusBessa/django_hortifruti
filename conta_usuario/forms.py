from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login


class RegistrarForm(forms.Form):
    usuario = forms.CharField(max_length=20, label='Usuário')
    senha = forms.CharField(max_length=30, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=30)


    def registrar_usuario(self, request, form):
        usuario, senha, email = form.cleaned_data.values()
        usuario = usuario.title()

        if len(senha) < 6:
            raise ValidationError('A senha deve ter pelo menos 6 caracteres.')

        elif User.objects.filter(username=usuario).exists():
            raise ValidationError('Esse nome de usuário já está em uso.')

        user = User.objects.create_user(username=usuario, password=senha, email=email)
        login(request, user)


class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=20, label='Usuário')
    senha = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def logar_usuario(self, request, form):
        usuario, senha = form.cleaned_data.values()
        usuario = usuario.title()
        print(usuario)
        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)

        else:
            raise ValidationError('Usuário ou senha incorretos.')


class AlterarSenhaForm(forms.Form):
    senha_atual = forms.CharField(max_length=30, widget=forms.PasswordInput())
    nova_senha = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def alterar_senha(self, request, form):
        senha_atual, nova_senha, senha_confirmacao = form.cleaned_data.values()
        user = authenticate(request, username=request.user, password=senha_atual)

        if user is None:
            raise ValidationError('Senha atual incorreta.')

        elif len(nova_senha) < 6:
            raise ValidationError('A nova senha deve ter pelo menos 6 caracteres.')

        elif senha_atual != senha_confirmacao:
            raise ValidationError('Senhas nos dois últimos campos eram diferentes.')

        user.set_password(nova_senha)
        user.save()

        login(request, user)
