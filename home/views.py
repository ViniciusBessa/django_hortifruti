from django.shortcuts import render
from produtos.models import Produto, CategoriasProduto


def home_view(request):
    categorias = CategoriasProduto.objects.all()
    produtos_categorias = Produto.receber_produtos(categorias, 4, 2)

    context = {
        'categorias': categorias,
        'produtos_categorias': produtos_categorias,
    }
    return render(request, 'home.html', context)
