from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from .models import Produto, CarrinhoCompra, ListaDesejo
from django.contrib.auth.decorators import login_required


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


def filtro_busca_view(request):
    busca = request.POST.get('busca')

    if request.method == 'POST' and busca:
        return redirect(reverse('busca', args=(busca,)))

    return redirect(reverse('home'))


def busca_produto_view(request, busca):
    produtos_encontrados = Produto.objects.filter(titulo__icontains=busca)
    carrinho_compra = CarrinhoCompra.receber(request.user)

    context = {
        'busca': busca,
        'produtos': produtos_encontrados,
        'numero_produtos_carrinho': len(carrinho_compra),
    }

    return render(request, 'busca_produto.html', context)


@login_required(login_url='/conta/login/')
def pagina_lista_desejos_view(request):
    lista_desejos = ListaDesejo.receber(request.user)
    carrinho_compra = CarrinhoCompra.receber(request.user)

    context = {
        'lista_desejos': lista_desejos,
        'numero_produtos_carrinho': len(carrinho_compra),
    }

    return render(request, 'lista_desejos.html', context)


@login_required(login_url='/conta/login/')
def pagina_carrinho_view(request):
    carrinho_compra = CarrinhoCompra.receber(request.user)
    subtotal = CarrinhoCompra.receber_soma_carrinho(request.user)
    produtos_quantidades = CarrinhoCompra.receber_quantidade_produtos(request.user)

    context = {
        'carrinho_compra': carrinho_compra,
        'numero_produtos_carrinho': len(carrinho_compra),
        'subtotal': subtotal,
        'quantidades': produtos_quantidades,
        'range': [1, 2, 3, 4, 5]
    }

    return render(request, 'carrinho_compra.html', context)


class AtualizarListaView(LoginRequiredMixin, View):
    login_url = '/conta/login/'
    model_class = ListaDesejo
    mensagem_retirada = 'Produto retirado da lista de desejos'
    mensagem_adicionado = 'Produto adicionado à lista de desejos'


    def get(self, request, *args, **kwargs):
        return redirect(reverse('home'))


    def post(self, request, id_produto, *args, **kwargs):
        query_model = self.model_class.receber(request.user)
        produto = get_object_or_404(Produto, id=id_produto)

        if produto in query_model:
            self.model_class.objects.filter(usuario=request.user, id_produto=produto).delete()
            messages.success(request, self.mensagem_retirada)

        else:
            self.model_class.objects.create(usuario=request.user, id_produto=produto)
            messages.success(request, self.mensagem_adicionado)

        return redirect(reverse('pagina_produto', args=(produto.id,)))    


class AtualizarCarrinhoView(AtualizarListaView):
    model_class = CarrinhoCompra
    mensagem_retirada = 'Produto retirado do carrinho'
    mensagem_adicionado = 'Produto adicionado ao carrinho'


@login_required(login_url='/conta/login/')
def alterar_carrinho_view(request, id_produto, quantidade):
    produto_carrinho = get_object_or_404(CarrinhoCompra, usuario=request.user, id_produto=id_produto)
    produto_carrinho.quantidade = quantidade
    produto_carrinho.save()
    return redirect(reverse('carrinho'))
