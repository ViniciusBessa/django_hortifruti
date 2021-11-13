from django.core.exceptions import ValidationError
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View

from .forms import RegistrarForm, LoginForm, AlterarSenhaForm
from produtos.models import dados_comuns


class RegistrarView(View):
    form_class = RegistrarForm
    template_name = 'registrar.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))

        form = self.form_class()
        self.context.update(dados_comuns(request.user))
        self.context.update({'form': form})
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))

        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                self.form_class.validacao(request, form)
                return redirect(reverse('home'))

            except ValidationError as erro:
                messages.error(request, erro)

        self.context.update(dados_comuns(request.user))
        self.context.update({'form': form})
        return render(request, self.template_name, self.context)


class LoginView(RegistrarView):
    form_class = LoginForm
    template_name = 'login.html'


class AlterarSenhaView(LoginRequiredMixin, RegistrarView):
    login_url = '/conta/login/'
    form_class = AlterarSenhaForm
    template_name = 'alterar_senha.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context.update(dados_comuns(request.user))
        self.context.update({'form': form})

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                self.form_class.validacao(request, form)
                return redirect(reverse('home'))

            except ValidationError as erro:
                messages.error(request, erro)

        self.context.update(dados_comuns(request.user))
        self.context.update({'form': form})
        return render(request, self.template_name, self.context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('home'))
