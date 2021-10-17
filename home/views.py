from django.shortcuts import render
from produtos.models import Produto, CategoriasProduto, CarrinhoCompra


def home_view(request):
    categorias = CategoriasProduto.objects.all()
    produtos_categorias = Produto.receber_produtos(categorias, 4, 2)
    carrinho_compra = CarrinhoCompra.receber_carrinho(request.user)

    context = {
        'categorias': categorias,
        'produtos_categorias': produtos_categorias,
        'numero_produtos_carrinho': len(carrinho_compra),
    }

    return render(request, 'home.html', context)
