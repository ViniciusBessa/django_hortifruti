from django.db import models
from django.contrib.auth.models import User

from produtos.models import Produto


class ListaDesejo(models.Model):
    """
    Model para registrar produtos na lista de desejos de um usuário

    Attribute usuario: Um usuário registrado
    Attribute id_produto: Uma fk para um produto
    """

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    def __str__(self):
        return 'Usuário ' + self.usuario.username + ' Produto ' + self.id_produto.titulo

    @staticmethod
    def receber(usuario):
        """Método que retorna uma lista de todos produtos na lista de desejos do usuário"""

        if usuario.is_authenticated:
            lista_desejos = ListaDesejo.objects.filter(usuario=usuario)
            lista_desejos = [lista.id_produto for lista in lista_desejos]

        else:
            lista_desejos = []

        return lista_desejos

    @staticmethod
    def receber_pagina(usuario):
        """Método que retorna um dicionário com os dados utilizados pelo view PaginaListaView"""

        lista_desejos = ListaDesejo.receber(usuario)
        return {
            'lista_desejos': lista_desejos, 
        }
