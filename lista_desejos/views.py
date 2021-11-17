from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from produtos.models import Produto
from .models import ListaDesejo
from dados_comuns import dados_comuns


class PaginaListaView(LoginRequiredMixin, View):
    """
    View que renderiza a página da lista de desejos do usuário

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute template_name: Recebe o template que deve ser renderizado pelo view
    Attribute context: Um dicionário que será utilizado no template
    """

    login_url = '/conta/login/'
    model_class = ListaDesejo
    template_name = 'lista_desejos.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context.update(dados_comuns(request.user))
        self.context.update(self.model_class.receber_pagina(request.user))
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        return redirect(reverse('home'))


class AtualizarListaView(LoginRequiredMixin, View):
    """
    View que atualiza a lista de desejos de um usuário em relação a um produto. Se ele já estiver
    na lista, será retirado da mesma, do contrário, é adicionado a ela

    Attribute login_url: URL que o usuário será redirecionado caso não esteja logado
    Attribute model_class: Recebe o model que será utilizado pelo view
    Attribute mensagem_retirado: Mensagem que será mostrada ao usuário retirar o produto
    Attribute mensagem_adicionado: Mensagem que será mostrada ao usuário adicionar o produto
    """

    login_url = '/conta/login/'
    model_class = ListaDesejo
    mensagem_retirado = 'Produto retirado da lista de desejos'
    mensagem_adicionado = 'Produto adicionado à lista de desejos'

    def get(self, request, *args, **kwargs):
        return redirect(reverse('home'))

    def post(self, request, id_produto, *args, **kwargs):
        query_model = self.model_class.receber(request.user)
        produto = get_object_or_404(Produto, id=id_produto)

        if produto in query_model:
            self.model_class.objects.filter(usuario=request.user, id_produto=produto).delete()
            messages.success(request, self.mensagem_retirado)

        else:
            self.model_class.objects.create(usuario=request.user, id_produto=produto)
            messages.success(request, self.mensagem_adicionado)

        return redirect(reverse('pagina_produto', args=(produto.id,)))
