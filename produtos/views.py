from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from conta_usuario.views import login_view
from .models import Produto, CategoriasProduto, CarrinhoCompra, ListaDesejo
from django.contrib.auth.decorators import login_required


def pagina_produto_view(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    produtos_mesma_categoria = Produto.objects.filter(id_categoria=produto.id_categoria)
    lista_desejos = ListaDesejo.receber_lista_desejos(request.user)
    carrinho_compra = CarrinhoCompra.receber_carrinho(request.user)

    context = {
        'produto': produto,
        'produtos_mesma_categoria': produtos_mesma_categoria,
        'categoria': produto.id_categoria,
        'lista_desejos': lista_desejos,
        'carrinho_compra': carrinho_compra,
    }

    return render(request, 'pagina_produto.html', context)


def filtro_busca_view(request):
    busca = request.POST.get('busca')

    if request.method == 'POST' and busca:
        return redirect(reverse('busca', args=(busca,)))

    return redirect(reverse('home'))


def busca_produto_view(request, busca):
    produtos_encontrados = Produto.objects.filter(titulo__icontains=busca)

    context = {
        'busca': busca,
        'produtos': produtos_encontrados
    }

    return render(request, 'busca_produto.html', context)


@login_required(login_url=login_view)
def atualizar_lista_desejos_view(request, id_produto):
    if request.method == 'POST':
        lista_desejos = ListaDesejo.receber_lista_desejos(request.user)
        produto = Produto.objects.get(id=id_produto)

        if produto in lista_desejos:
            ListaDesejo.objects.filter(usuario=request.user, id_produto=produto).delete()

        else:
            ListaDesejo.objects.create(usuario=request.user, id_produto=produto)

        return redirect(reverse('pagina_produto', args=(produto.id,)))

    return redirect(reverse('home'))


@login_required(login_url=login_view)
def buscar_lista_desejos_view(request):
    lista_desejos = ListaDesejo.receber_lista_desejos(request.user)

    context = {
        'lista_desejos': lista_desejos,
    }

    return render(request, 'lista_desejos.html', context)


@login_required(login_url=login_view)
def atualizar_carrinho_view(request, id_produto):
    if request.method == 'POST':
        carrinho_compra = CarrinhoCompra.receber_carrinho(request.user)
        produto = Produto.objects.get(id=id_produto)

        if produto in carrinho_compra:
            CarrinhoCompra.objects.filter(usuario=request.user, id_produto=produto).delete()

        else:
            CarrinhoCompra.objects.create(usuario=request.user, id_produto=produto)

        return redirect(reverse('pagina_produto', args=(produto.id,)))

    return redirect(reverse('home'))


@login_required(login_url=login_view)
def buscar_carrinho_view(request):
    carrinho_compra = CarrinhoCompra.receber_carrinho(request.user)

    context = {
        'carrinho_compra': carrinho_compra,
    }

    return render(request, 'carrinho_compra.html', context)
