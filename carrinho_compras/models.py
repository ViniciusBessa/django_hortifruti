from django.contrib.auth.models import User
from django.db import models

from produtos.models import Produto


class CarrinhoCompra(models.Model):
    """
    Model para registrar produtos no carrinho de compras de um usuário

    Attribute usuario: Um usuário registrado
    Attribute id_produto: Uma fk para um produto
    Attribute quantidade: Um número inteiro para ser a quantidade do produto
    """

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return 'Usuário ' + self.usuario.username + ' Produto ' + self.id_produto.titulo

    @staticmethod
    def receber(usuario):
        if usuario.is_authenticated:
            carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
            carrinho_compra = [lista.id_produto for lista in carrinho_compra]

        else:
            carrinho_compra = []

        return sorted(carrinho_compra, key=lambda produto: produto.titulo)

    @staticmethod
    def receber_soma_carrinho(usuario):
        carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
        subtotal = sum(lista.id_produto.preco * lista.quantidade for lista in carrinho_compra)
        return subtotal

    @staticmethod
    def receber_quantidade_produtos(usuario):
        carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
        quantidades = {lista.id_produto: lista.quantidade for lista in carrinho_compra}
        return quantidades

    @staticmethod
    def receber_pagina(usuario):
        carrinho_compra = CarrinhoCompra.receber(usuario)
        subtotal = CarrinhoCompra.receber_soma_carrinho(usuario)
        produtos_quantidades = CarrinhoCompra.receber_quantidade_produtos(usuario)
        return {
            'carrinho_compra': carrinho_compra,
            'numero_produtos_carrinho': len(carrinho_compra),
            'subtotal': subtotal,
            'quantidades': produtos_quantidades,
            'range': [1, 2, 3, 4, 5]
        }
