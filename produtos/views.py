from django.shortcuts import render
from .models import Produto


def produto_view(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    context = {
        'produto': produto
    }
    return render(request, 'pagina_produto.html', context)
