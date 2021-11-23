from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from .models import CarrinhoCompra
from produtos.models import Produto
from dados_comuns import dados_comuns


class PaginaCarrinhoView(LoginRequiredMixin, View):
    """
    View que renderiza a página do carrinho de compras do usuário

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    login_url = '/conta/login/'
    model_class = CarrinhoCompra
    template_name = 'carrinho_compra.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.update(dados_comuns(request.user))
        self.context.update(self.model_class.receber_pagina(request.user))
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return redirect(reverse('home'))


class AtualizarCarrinhoView(LoginRequiredMixin, View):
    """
    View que atualiza o carrinho de compras de um usuário em relação a um produto. Se ele já estiver
    no carrinho, será retirado do mesmo, do contrário, é adicionado a ele

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute mensagem_retirado: Mensagem que será mostrada ao usuário retirar o produto
    Attribute mensagem_adicionado: Mensagem que será mostrada ao usuário adicionar o produto
    """

    login_url = '/conta/login/'
    model_class = CarrinhoCompra
    mensagem_retirado = 'Produto retirado do carrinho de compras'
    mensagem_adicionado = 'Produto adicionado ao carrinho de compras'

    def get(self, request, *args, **kwargs):
        return redirect(reverse('home'))

    def post(self, request, id_produto, *args, **kwargs):
        query_model = self.model_class.receber(request.user)
        produto = get_object_or_404(Produto, id=id_produto)

        if produto in query_model:
            self.model_class.objects.filter(usuario=request.user, id_produto=produto).delete()
            messages.success(request, self.mensagem_retirado)

        else:
            self.model_class.objects.create(usuario=request.user, id_produto=produto)
            messages.success(request, self.mensagem_adicionado)

        # Variável utilizada para redirecionar o usuário à página em que ele estava
        next = request.POST.get('next', '/')

        return redirect(next)


class AlterarCarrinhoView(LoginRequiredMixin, View):
    """
    View utilizado para alterar a quantidade de um produto no carrinho de compras do usuário

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    """

    login_url = '/conta/login/'

    def get(self, request, id_produto, quantidade, *args, **kwargs):
        produto_carrinho = get_object_or_404(CarrinhoCompra, usuario=request.user, id_produto=id_produto)
        produto_carrinho.quantidade = quantidade
        produto_carrinho.save()
        return redirect(reverse('carrinho'))

    def post(self, request, *args, **kwargs):
        return redirect(reverse('home'))
