from django.shortcuts import render
from django.views import View

from core.models import Produto
from dados_comuns import dados_comuns


class HomeView(View):
    """
    View que renderiza a home do projeto

    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    template_name = 'home.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.update(dados_comuns(request.user))
        produtos_mais_vendidos = Produto.mais_vendidos()
        produtos_categorias = Produto.receber_produtos(self.context.get('categorias'), 4, 2)

        self.context.update({
            'produtos_categorias': produtos_categorias,
            'produtos_mais_vendidos': produtos_mais_vendidos,
        })

        return render(request, self.template_name, self.context)
