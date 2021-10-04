from django.shortcuts import render
from produtos.models import Produto, CategoriasProduto


def home_view(request):
    categorias = CategoriasProduto.objects.all()
    produtos = Produto.receber_produtos(categorias, 4)

    context = {
        'categorias': categorias,
        'produtos': produtos,
    }
    return render(request, 'home.html', context)
