from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
import re

regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class RegistrarForm(forms.Form):
    """
    Formulário para registrar um usuário

    Attribute usuario: Recebe uma string que é o nome do usuário
    Attribute senha: Recebe uma string que é a senha
    Attribute email: Recebe uma string que é um e-mail válido
    """

    usuario = forms.CharField(
        max_length=20, label=False, widget=forms.TextInput(attrs={'placeholder': 'Usuário'})
        )

    senha = forms.CharField(
        max_length=30, label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}) 
        )

    email = forms.CharField(
        max_length=20, label=False, widget=forms.TextInput(attrs={'placeholder': 'Email'}) 
        )

    @staticmethod
    def validacao(request, form):
        """Função que valida os dados no form para registrar o usuário"""

        usuario, senha, email = form.cleaned_data.values()
        usuario = usuario.title()

        if len(senha) < 6:
            raise ValidationError('A senha deve ter pelo menos 6 caracteres.')

        elif User.objects.filter(username=usuario).exists():
            raise ValidationError('Esse nome de usuário já está em uso.')

        elif not re.fullmatch(regex_email, email):
            raise ValidationError('E-mail inválido, coloque-o na sequência nome_do_email@dominio.com')

        user = User.objects.create_user(username=usuario, password=senha, email=email)
        login(request, user)


class LoginForm(forms.Form):
    """
    Formulário para verificar e logar um usuário

    Attribute usuario: Recebe uma string que é o nome do usuário
    Attribute senha: Recebe uma string que é a senha
    """

    usuario = forms.CharField(
        max_length=20, label=False, widget=forms.TextInput(attrs={'placeholder': 'Usuário'})
        )

    senha = forms.CharField(
        max_length=30, label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}) 
        )

    @staticmethod
    def validacao(request, form):
        """Função que valida os dados no form para efetuar o login"""

        usuario, senha = form.cleaned_data.values()
        usuario = usuario.title()
        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)

        else:
            raise ValidationError('Usuário ou senha incorretos.')


class AlterarSenhaForm(forms.Form):
    """
    Formulário para alterar a senha do usuário

    Attribute senha_atual: Recebe uma string que é a senha do usuário
    Attribute nova_senha: Recebe uma string que será a nova senha
    Attribute confirmar_senha: Recebe uma string que confirma a nova senha
    """

    senha_atual = forms.CharField(
        max_length=30, label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Senha atual'}) 
        )

    nova_senha = forms.CharField(
        max_length=30, label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Nova senha'}) 
        )

    confirmar_senha = forms.CharField(
        max_length=30, label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar senha'}) 
        )

    @staticmethod
    def validacao(request, form):
        """Função que valida os dados no form para alterar a senha"""

        senha_atual, nova_senha, senha_confirmacao = form.cleaned_data.values()
        user = authenticate(request, username=request.user, password=senha_atual)

        if user is None:
            raise ValidationError('Senha atual incorreta.')

        elif len(nova_senha) < 6:
            raise ValidationError('A nova senha deve ter pelo menos 6 caracteres.')

        elif nova_senha != senha_confirmacao:
            raise ValidationError('Senhas nos dois últimos campos eram diferentes.')

        user.set_password(nova_senha)
        user.save()
        login(request, user)
