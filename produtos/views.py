from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from .models import Produto, CarrinhoCompra, ListaDesejo


def pagina_produto_view(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)
    produtos_mesma_categoria = Produto.objects.filter(id_categoria=produto.id_categoria)
    lista_desejos = ListaDesejo.receber(request.user)
    carrinho_compra = CarrinhoCompra.receber(request.user)

    context = {
        'produto': produto,
        'produtos_mesma_categoria': produtos_mesma_categoria,
        'categoria': produto.id_categoria,
        'lista_desejos': lista_desejos,
        'carrinho_compra': carrinho_compra,
        'numero_produtos_carrinho': len(carrinho_compra),
    }

    return render(request, 'pagina_produto.html', context)


class BuscaProdutoView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('home'))


    def post(self, request, busca, *args, **kwargs):
        produtos_encontrados = Produto.objects.filter(titulo__icontains=busca)
        carrinho_compra = CarrinhoCompra.receber(request.user)

        context = {
            'busca': busca,
            'produtos': produtos_encontrados,
            'numero_produtos_carrinho': len(carrinho_compra),
        }

        if produtos_encontrados:
            return render(request, 'busca_produto.html', context)

        return redirect(reverse('home'))


class PaginaListaView(LoginRequiredMixin, View):
    login_url = '/conta/login/'
    model_class = ListaDesejo
    template_name = 'lista_desejos.html'
    context = {}


    def get(self, request, *args, **kwargs):
        self.context.update(self.model_class.receber_pagina(request))
        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):
        return redirect(reverse('home'))


class PaginaCarrinhoView(PaginaListaView):
    model_class = CarrinhoCompra
    template_name = 'carrinho_compra.html'


class AtualizarListaView(LoginRequiredMixin, View):
    login_url = '/conta/login/'
    model_class = ListaDesejo
    mensagem_retirado = 'Produto retirado da lista de desejos'
    mensagem_adicionado = 'Produto adicionado à lista de desejos'


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

        return redirect(reverse('pagina_produto', args=(produto.id,)))    


class AtualizarCarrinhoView(AtualizarListaView):
    model_class = CarrinhoCompra
    mensagem_retirado = 'Produto retirado do carrinho'
    mensagem_adicionado = 'Produto adicionado ao carrinho'


class AlterarCarrinhoView(LoginRequiredMixin, View):
    login_url = '/conta/login/'

    def get(self, request, id_produto, quantidade, *args, **kwargs):
        produto_carrinho = get_object_or_404(CarrinhoCompra, usuario=request.user, id_produto=id_produto)
        produto_carrinho.quantidade = quantidade
        produto_carrinho.save()
        return redirect(reverse('carrinho'))


    def post(self, request, *args, **kwargs):
        return redirect(reverse('home'))
