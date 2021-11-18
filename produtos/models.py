from django.db import models
from django.shortcuts import get_object_or_404
from more_itertools import divide


class Produto(models.Model):
    """
    Model para registrar um produto

    Attribute titulo: Uma string para ser o titulo do produto
    Attribute preco: Um número decimal que representa o preço do produto
    Attribute descricao: Uma string para ser uma breve descrição do produto
    Attribute imagem: Um arquivo de imagem do produto
    Attribute id_categoria: Uma fk para uma das categorias
    """

    titulo = models.CharField(max_length=30)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    descricao = models.CharField(max_length=500)
    imagem = models.ImageField()
    id_categoria = models.ForeignKey('CategoriasProduto', on_delete=models.CASCADE)
    estoque = models.IntegerField(default=100)

    def __str__(self):
        return self.titulo

    @staticmethod
    def receber_produtos(categorias, numero_produtos, partes):
        dicionario_produtos: dict = {}
        for categoria in categorias:
            produtos_da_categoria = Produto.objects.filter(id_categoria=categoria)[:numero_produtos]

            if produtos_da_categoria:
                produtos_divididos = divide(partes, produtos_da_categoria)
                produtos_divididos = [list(x) for x in produtos_divididos]
                dicionario_produtos.update({categoria: produtos_divididos.copy()})

        return dicionario_produtos

    @staticmethod
    def mesma_categoria(produto):
        produtos = Produto.objects.filter(id_categoria=produto.id_categoria)
        produtos = [prod for prod in produtos if prod.id != produto.id][:5]
        return produtos


class CategoriasProduto(models.Model):
    """
    Model para registrar uma categoria de produto

    Attribute titulo: Uma string para ser o titulo da categoria
    """

    titulo = models.CharField(max_length=20)

    def __str__(self):
        return self.titulo

    @staticmethod
    def receber_pagina(categoria):
        categoria = get_object_or_404(CategoriasProduto, titulo=categoria.title())
        produtos = list(Produto.objects.filter(id_categoria=categoria))

        return {
            'categoria': categoria,
            'produtos': produtos,
        }
