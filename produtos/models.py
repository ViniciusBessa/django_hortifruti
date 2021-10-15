from django.db import models
from more_itertools import divide
from django.contrib.auth.models import User


class Produto(models.Model):
    titulo = models.CharField(max_length=40)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    descricao = models.CharField(max_length=500)
    imagem = models.ImageField()
    id_categoria = models.ForeignKey('CategoriasProduto', on_delete=models.CASCADE)


    def receber_produtos(categorias, numero_produtos, partes):
        dicionario_produtos: dict = {}
        for categoria in categorias:
            produtos_da_categoria = Produto.objects.filter(id_categoria=categoria)[:numero_produtos]

            if produtos_da_categoria:
               produtos_divididos = divide(partes, produtos_da_categoria)
               produtos_divididos = [list(x) for x in produtos_divididos]
               dicionario_produtos.update({categoria: produtos_divididos.copy()})

        return dicionario_produtos


class CategoriasProduto(models.Model):
    titulo = models.CharField(max_length=20)


class CarrinhoCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_produto = models.ForeignKey('Produto', on_delete=models.CASCADE)

    def receber_carrinho(usuario):
        if usuario.is_authenticated:
            carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
            carrinho_compra = [lista.id_produto for lista in carrinho_compra]
        
        else:
            carrinho_compra = []

        return carrinho_compra


class ListaDesejo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_produto = models.ForeignKey('Produto', on_delete=models.CASCADE)

    def receber_lista_desejos(usuario):
        if usuario.is_authenticated:
            lista_desejos = ListaDesejo.objects.filter(usuario=usuario)
            lista_desejos = [lista.id_produto for lista in lista_desejos]

        else:
            lista_desejos = []

        return lista_desejos
