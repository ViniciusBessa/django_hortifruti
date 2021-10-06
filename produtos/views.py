from django.shortcuts import render
from .models import Produto


def pagina_produto_view(request, id_produto):
    produto = Produto.objects.get(id=id_produto)

    context = {
        'produto': produto
    }
    return render(request, 'pagina_produto.html', context)


def busca_produto_view(request, busca):
    produtos_encontrados = Produto.objects.filter(titulo__icontains=busca)

    context = {
        'produtos': produtos_encontrados
    }

    return render(request, 'busca_produto.html', context)
