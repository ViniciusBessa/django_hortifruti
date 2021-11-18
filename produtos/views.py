from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from .models import CategoriasProduto, Produto
from lista_desejos.models import ListaDesejo
from carrinho_compras.models import CarrinhoCompra
from dados_comuns import dados_comuns


class PaginaProdutoView(View):
    """
    View que renderiza a página de um produto

    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    template_name = 'pagina_produto.html'
    context = {}

    def get(self, request, id_produto, *args, **kwargs):
        produto = get_object_or_404(Produto, id=id_produto)
        produtos_mesma_categoria = Produto.mesma_categoria(produto)
        lista_desejos = ListaDesejo.receber(request.user)
        carrinho_compra = CarrinhoCompra.receber(request.user)

        self.context.update({
            'produto': produto,
            'produtos_mesma_categoria': produtos_mesma_categoria,
            'categoria': produto.id_categoria,
            'lista_desejos': lista_desejos,
            'carrinho_compra': carrinho_compra,
        })
        self.context.update(dados_comuns(request.user))
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return redirect(reverse('home'))


class BuscaProdutoView(View):
    """
    View que renderiza a página de busca de produtos

    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    template_name = 'busca_produto.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return redirect(reverse('home'))

    def post(self, request, busca, *args, **kwargs):
        self.context.update(dados_comuns(request.user))
        produtos_encontrados = list(Produto.objects.filter(titulo__icontains=busca))

        self.context.update({
            'busca': busca,
            'produtos': produtos_encontrados,
        })

        return render(request, self.template_name, self.context)


class PaginaCategoriasView(View):
    """
    View que renderiza uma página com todos produtos de uma determinada categoria

    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = CategoriasProduto
    template_name = 'categorias.html'
    context = {}

    def get(self, request, categoria, *args, **kwargs):
        self.context.update(dados_comuns(request.user))
        self.context.update(self.model_class.receber_pagina(categoria))
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return redirect(reverse('home'))
