from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from .models import Produto


def pagina_produto_view(request, id_produto):
    produto = Produto.objects.get(id=id_produto)

    context = {
        'produto': produto
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
