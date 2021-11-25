from django.contrib.auth.models import User
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
    vendas = models.IntegerField(default=0)

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
        """Método que retorna alguns produtos da mesma categoria do argumento produto"""

        produtos = Produto.objects.filter(id_categoria=produto.id_categoria)
        produtos = [prod for prod in produtos if prod.id != produto.id][:4]
        return produtos

    @staticmethod
    def mais_vendidos():
        """Método que retorna os produtos mais vendidos"""

        produtos = Produto.objects.all()
        produtos = sorted(produtos, key=lambda produto: produto.vendas, reverse=True)
        return produtos[:4]

    @staticmethod
    def receber_pagina(produto, usuario):
        produtos_mesma_categoria = Produto.mesma_categoria(produto)
        lista_desejos = ListaDesejo.receber(usuario)
        carrinho_compra = CarrinhoCompra.receber(usuario)

        return {
            'produto': produto,
            'produtos_mesma_categoria': produtos_mesma_categoria,
            'categoria': produto.id_categoria,
            'lista_desejos': lista_desejos,
            'carrinho_compra': carrinho_compra,
        }


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
        """Método que retorna uma lista dos produtos no carrinho do usuário, ordenados em 
        ordem alfabética"""

        if usuario.is_authenticated:
            carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
            carrinho_compra = [lista.id_produto for lista in carrinho_compra]

        else:
            carrinho_compra = []

        return sorted(carrinho_compra, key=lambda produto: produto.titulo)

    @staticmethod
    def receber_soma_carrinho(usuario):
        """Método que retorna a soma de todos produtos no carrinho do usuário"""

        carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
        subtotal = sum(lista.id_produto.preco * lista.quantidade for lista in carrinho_compra)
        return subtotal

    @staticmethod
    def receber_quantidade_produtos(usuario):
        """Método que retorna um dicionário com a quantidade de cada produto no carrinho do usuário"""

        carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
        quantidades = {lista.id_produto: lista.quantidade for lista in carrinho_compra}
        return quantidades

    @staticmethod
    def receber_pagina(usuario):
        """Método que retorna um dicionário com os dados utilizados pelo view PaginaCarrinhoView"""

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
