from django.db import models


class Produto(models.Model):
    titulo = models.CharField(max_length=40)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    descricao = models.CharField(max_length=500)
    imagem = models.ImageField()
    id_categoria = models.ForeignKey('CategoriasProduto', on_delete=models.CASCADE)

    def receber_produtos(categorias, numero_produtos):
        lista_produtos = []
        for categoria in categorias:
            lista_produtos.append(Produto.objects.filter(id_categoria=categoria)[:numero_produtos])
        return lista_produtos


class CategoriasProduto(models.Model):
    titulo = models.CharField(max_length=20)
