from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import CategoriasProduto, Produto, CarrinhoCompra, ListaDesejo, dados_comuns


class PaginaProdutoView(View):
    """
    View que renderiza a página de um produto

    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = Produto
    template_name = 'pagina_produto.html'
    context = {}

    def get(self, request, id_produto, *args, **kwargs):
        produto = get_object_or_404(Produto, id=id_produto)
        self.context.update(dados_comuns(request.user))
        self.context.update(self.model_class.receber_pagina(produto, request.user))

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return redirect('home')


class BuscaProdutoView(View):
    """
    View que renderiza a página de busca de produtos

    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    template_name = 'busca_produto.html'
    context = {}

    def get(self, request, busca, *args, **kwargs):
        self.context.update(dados_comuns(request.user))
        produtos_encontrados = list(Produto.objects.filter(titulo__icontains=busca))

        self.context.update({
            'busca': busca,
            'produtos': produtos_encontrados,
        })

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return redirect('home')


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
        return redirect('home')


class PaginaCarrinhoView(LoginRequiredMixin, View):
    """
    View que renderiza a página do carrinho de compras do usuário

    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = CarrinhoCompra
    template_name = 'carrinho_compra.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.update(dados_comuns(request.user))
        self.context.update(self.model_class.receber_pagina(request.user))
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return redirect('home')


class PaginaListaView(PaginaCarrinhoView):
    """
    View que renderiza a página da lista de desejos do usuário

    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = ListaDesejo
    template_name = 'lista_desejos.html'


class AtualizarCarrinhoView(LoginRequiredMixin, View):
    """
    View que atualiza o carrinho de compras de um usuário em relação a um produto. Se ele já estiver
    no carrinho, será retirado do mesmo, caso contrário é adicionado a ele

    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute mensagem_retirado: Mensagem que será mostrada ao usuário retirar o produto
    Attribute mensagem_adicionado: Mensagem que será mostrada ao usuário adicionar o produto
    """

    model_class = CarrinhoCompra
    mensagem_retirado = 'Produto retirado do carrinho de compras'
    mensagem_adicionado = 'Produto adicionado ao carrinho de compras'

    def get(self, request, *args, **kwargs):
        return redirect('home')

    def post(self, request, id_produto, *args, **kwargs):
        query_model = self.model_class.receber(request.user)
        produto = get_object_or_404(Produto, id=id_produto)

        if produto in query_model:
            self.model_class.objects.filter(usuario=request.user, produto=produto).delete()
            messages.success(request, self.mensagem_retirado)

        else:
            self.model_class.objects.create(usuario=request.user, produto=produto)
            messages.success(request, self.mensagem_adicionado)

        # Variável utilizada para redirecionar o usuário à página em que ele estava
        next = request.POST.get('next', '/')
        return redirect(next)


class AtualizarListaView(AtualizarCarrinhoView):
    """
    View que atualiza a lista de desejos de um usuário em relação a um produto. Se ele já estiver
    na lista, será retirado da mesma, caso contrário é adicionado a ela

    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute mensagem_retirado: Mensagem que será mostrada ao usuário retirar o produto
    Attribute mensagem_adicionado: Mensagem que será mostrada ao usuário adicionar o produto
    """

    model_class = ListaDesejo
    mensagem_retirado = 'Produto retirado da lista de desejos'
    mensagem_adicionado = 'Produto adicionado à lista de desejos'


class AlterarCarrinhoView(LoginRequiredMixin, View):
    """
    View utilizado para alterar a quantidade de um produto no carrinho de compras do usuário
    """

    def get(self, request, id_produto, quantidade, *args, **kwargs):
        produto_carrinho = get_object_or_404(CarrinhoCompra, usuario=request.user, produto=id_produto)
        produto_carrinho.quantidade = quantidade
        produto_carrinho.save()
        return redirect('carrinho')

    def post(self, request, *args, **kwargs):
        return redirect('home')
