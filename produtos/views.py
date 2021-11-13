from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.core.exceptions import ValidationError

from .models import CategoriasProduto, Produto, CarrinhoCompra, ListaDesejo, Pedido, dados_comuns
from .forms import FinalizarPedido


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
        produtos_mesma_categoria = Produto.objects.filter(id_categoria=produto.id_categoria)
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
        produtos_encontrados = Produto.objects.filter(titulo__icontains=busca)

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


class PaginaListaView(LoginRequiredMixin, View):
    """
    View que renderiza a página da lista de desejos do usuário

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    login_url = '/conta/login/'
    model_class = ListaDesejo
    template_name = 'lista_desejos.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.update(dados_comuns(request.user))
        self.context.update(self.model_class.receber_pagina(request.user))
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return redirect(reverse('home'))


class PaginaCarrinhoView(PaginaListaView):
    """
    View que renderiza a página do carrinho de compras do usuário

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = CarrinhoCompra
    template_name = 'carrinho_compra.html'


class PaginaTodosPedidosView(PaginaListaView):
    """
    View que renderiza uma página com todos os pedidos já efetuados pelo usuário

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = Pedido
    template_name = 'todos_pedidos.html'


class PaginaPedidoView(PaginaListaView):
    """
    View que renderiza a página de um pedido escolhido pelo usuário, mostrando informações
    como data do pedido, forma de pagamento, quantidade dos produtos, etc

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    model_class = Pedido
    template_name = 'pedido.html'

    def get(self, request, id_pedido, *args, **kwargs):
        pedido = get_object_or_404(self.model_class, id=id_pedido)
        self.context.update(dados_comuns(request.user))
        self.context.update(Pedido.receber_pagina_pedido(pedido))
        return render(request, self.template_name, self.context)


class PaginaFinalizarPedidoView(PaginaListaView):
    """
    View que renderiza um form em que o usuário escolhe a transportadora e a forma de pagamento
    do pedido

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
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
                return redirect(reverse('home'))

            except ValidationError as erro:
                messages.error(request, erro)

        return redirect(reverse('lista_desejos')) 


class AtualizarListaView(LoginRequiredMixin, View):
    """
    View que atualiza a lista de desejos de um usuário em relação a um produto, se ele já estiver
    na lista, será retirado da mesma, do contrário, é adicionado a ela

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute mensagem_retirado: Mensagem que será mostrada ao usuário retirar o produto
    Attribute mensagem_adicionado: Mensagem que será mostrada ao usuário adicionar o produto
    """

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
    """
    View que atualiza o carrinho de compras de um usuário em relação a um produto, se ele já estiver
    no carrinho, será retirado do mesmo, do contrário, é adicionado a ele

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute mensagem_retirado: Mensagem que será mostrada ao usuário retirar o produto
    Attribute mensagem_adicionado: Mensagem que será mostrada ao usuário adicionar o produto
    """

    model_class = CarrinhoCompra
    mensagem_retirado = 'Produto retirado do carrinho'
    mensagem_adicionado = 'Produto adicionado ao carrinho'


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
