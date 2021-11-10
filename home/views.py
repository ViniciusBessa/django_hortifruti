from django.shortcuts import render
from django.views import View
from produtos.models import Produto, CategoriasProduto, CarrinhoCompra, dados_comuns


class HomeView(View):
    template_name = 'home.html'
    context = {}


    def get(self, request, *args, **kwargs):
        categorias = list(CategoriasProduto.objects.all())
        produtos_categorias = Produto.receber_produtos(categorias, 4, 2)
        self.context.update(dados_comuns(request.user))
        self.context.update({
            'produtos_categorias': produtos_categorias,
        })

        return render(request, self.template_name, self.context)
