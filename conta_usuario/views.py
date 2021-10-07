from django.core.exceptions import ValidationError
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, RegistrarForm


def registrar_view(request):
    form = RegistrarForm()
    if request.method == 'POST':
        form = RegistrarForm(request.POST)

        if form.is_valid():
            try:
                form.validar_senha()
                user = form.registrar_usuario()

                login(request, user)
                return redirect(reverse('home'))

            except ValidationError as erro:
                messages.error(request, erro)

        else:
            form = RegistrarForm()

    context = {
        'form': form
    }

    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return render(request, 'registrar.html', context)


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():     
            try:
                user = form.autenticar_usuario(request)
                login(request, user)
                return redirect(reverse('home'))

            except ValidationError as erro:
                messages.error(request, erro)

        else:
            form = LoginForm()

    context = {
        'form': form
    }

    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return render(request, 'login.html', context)


@login_required(login_url=login_view)
def logout_view(request):
    logout(request)
    return redirect(reverse('home'))
