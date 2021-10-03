from django.shortcuts import render
from produtos.models import Produto


def home_view(request):
    produtos = Produto.objects.all()
    context = {
        'produto1': produtos[0],
        'produtos': produtos[1::]
    }
    return render(request, 'home.html', context)
