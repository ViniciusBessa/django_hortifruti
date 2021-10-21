from django.core.exceptions import ValidationError
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from .forms import LoginForm, RegistrarForm, AlterarSenhaForm


class RegistrarView(View):
    form_class = RegistrarForm
    template_name = 'registrar.html'
    form_validacao = RegistrarForm.registrar_usuario


    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {
            'form': form
        }

        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                self.form_validacao(request, form)
                return redirect(reverse('home'))

            except ValidationError as erro:
                messages.error(request, erro)

        context = {
            'form': form
        }
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request, self.template_name, context)


class LoginView(RegistrarView):
    form_class = LoginForm
    template_name = 'login.html'
    form_validacao = LoginForm.logar_usuario


class AlterarSenhaView(RegistrarView):
    form_class = AlterarSenhaForm
    template_name = 'alterar_senha.html'
    form_validacao = AlterarSenhaForm.verificar_senhas


    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('home'))
