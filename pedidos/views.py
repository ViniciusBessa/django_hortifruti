from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.core.exceptions import ValidationError

from .forms import FinalizarPedido
from .models import Pedido
from core.models import dados_comuns


class PaginaTodosPedidosView(LoginRequiredMixin, View):
    """
    View que renderiza uma página com todos os pedidos já efetuados pelo usuário

    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = Pedido
    template_name = 'todos_pedidos.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.update(dados_comuns(request.user))
        self.context.update(self.model_class.receber_pagina(request.user))
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return redirect(reverse('home'))


class PaginaPedidoView(PaginaTodosPedidosView):
    """
    View que renderiza a página de um pedido escolhido pelo usuário, mostrando informações
    como data do pedido, forma de pagamento, quantidade dos produtos, etc

    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = Pedido
    template_name = 'pedido.html'

    def get(self, request, id_pedido, *args, **kwargs):
        pedido = get_object_or_404(self.model_class, usuario=request.user, id=id_pedido)
        self.context.update(dados_comuns(request.user))
        self.context.update(self.model_class.receber_pagina_pedido(pedido))
        return render(request, self.template_name, self.context)


class PaginaFinalizarPedidoView(PaginaTodosPedidosView):
    """
    View que renderiza um form em que o usuário escolhe a transportadora e a forma de pagamento
    do pedido

    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute form_class: Recebe o form que será utilizado no view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = Pedido
    form_class = FinalizarPedido
    template_name = 'finalizar_pedido.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context.update({'form': form})
        self.context.update(dados_comuns(request.user))
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                self.model_class.criar_pedido(form, request.user)
                messages.success(request, 'Pedido efetuado com sucesso')
                return redirect(reverse('home'))

            except ValidationError as erro:
                messages.error(request, erro)

        return redirect(reverse('finalizar_pedido'))
