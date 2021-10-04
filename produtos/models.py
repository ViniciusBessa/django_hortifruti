from django.db import models
from more_itertools import divide


class Produto(models.Model):
    titulo = models.CharField(max_length=40)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    descricao = models.CharField(max_length=500)
    imagem = models.ImageField()
    id_categoria = models.ForeignKey('CategoriasProduto', on_delete=models.CASCADE)

    def receber_produtos(categorias, numero_produtos, partes):
        dicio = {}
        for categoria in categorias:
            produtos_divididos = divide(partes, Produto.objects.filter(id_categoria=categoria)[:numero_produtos])
            produtos_divididos = [list(x) for x in produtos_divididos]
            dicio.update({categoria: produtos_divididos.copy()})
        return dicio


class CategoriasProduto(models.Model):
    titulo = models.CharField(max_length=20)
