from django.shortcuts import render
from django.views import View
from produtos.models import Produto, CategoriasProduto, CarrinhoCompra


class HomeView(View):
    template_name = 'home.html'


    def get(self, request, *args, **kwargs):
        categorias = list(CategoriasProduto.objects.all())
        produtos_categorias = Produto.receber_produtos(categorias, 4, 2)
        carrinho_compra = CarrinhoCompra.receber(request.user)

        context = {
            'categorias': categorias,
            'produtos_categorias': produtos_categorias,
            'numero_produtos_carrinho': len(carrinho_compra),
        }

        return render(request, self.template_name, context)
