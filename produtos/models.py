from django.db import models


class Produto(models.Model):
    titulo = models.CharField(max_length=40)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    descricao = models.CharField(max_length=500)
    imagem = models.ImageField()
    categoria = models.ForeignKey('CategoriasProduto', on_delete=models.CASCADE)


class CategoriasProduto(models.Model):
    titulo = models.CharField(max_length=20)
