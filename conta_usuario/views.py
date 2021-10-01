from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, RegisterForm
from home.views import home_view


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                form.validating_password()
                usuario, senha, email, nome, sobrenome = form.cleaned_data.values()
                if User.objects.filter(username=usuario).exists():
                    raise ValidationError('Esse nome de usuário já está em uso')
                User.objects.create_user(username=usuario, password=senha, email=email, first_name=nome, last_name=sobrenome)
            except ValidationError as erro:
                messages.error(request, erro)

        else:
            print(form.errors)
            form = RegisterForm()

    context = {'form': form}

    if request.user.is_authenticated:
        return redirect(home_view)
    return render(request, 'register.html', context)


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            usuario, senha = form.cleaned_data.values()
            user = authenticate(request, username=usuario, password=senha)

            if user is not None:
                login(request, user)
                return redirect(home_view)

            # TODO Adicionar uma mensagem avisando que o usuário não logou
            else:
                pass

        else:
            print(form.errors)
        form = LoginForm()

    context = {
        'form': form
    }

    # Caso o usuário já esteja logado, ele é redirecionado à home
    if request.user.is_authenticated:
        return redirect(home_view)
    return render(request, 'login.html', context)


@login_required(login_url=login_view)
def logout_view(request):
    logout(request)
    return redirect(home_view)
