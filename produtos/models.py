from django.db import models
from django.shortcuts import get_object_or_404
from more_itertools import divide
from django.contrib.auth.models import User


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
        produtos = Produto.objects.filter(id_categoria=categoria)

        return {
            'categoria': categoria,
            'produtos': produtos,
        }


class ListaDesejo(models.Model):
    """
    Model para registrar produtos na lista de desejos de um usuário

    Attribute usuario: Um usuário registrado
    Attribute id_produto: Uma fk para um produto
    """

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_produto = models.ForeignKey('Produto', on_delete=models.CASCADE)

    def __str__(self):
        return 'Usuário ' + self.usuario.username + ' Produto ' + self.id_produto.titulo

    @staticmethod
    def receber(usuario):
        if usuario.is_authenticated:
            lista_desejos = ListaDesejo.objects.filter(usuario=usuario)
            lista_desejos = [lista.id_produto for lista in lista_desejos]

        else:
            lista_desejos = []

        return lista_desejos

    @staticmethod
    def receber_pagina(usuario):
        lista_desejos = ListaDesejo.receber(usuario)
        return {
            'lista_desejos': lista_desejos, 
        }


class CarrinhoCompra(models.Model):
    """
    Model para registrar produtos no carrinho de compras de um usuário

    Attribute usuario: Um usuário registrado
    Attribute id_produto: Uma fk para um produto
    Attribute quantidade: Um número inteiro para ser a quantidade do produto
    """

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
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


class Pedido(models.Model):
    """
    Model para registrar um pedido realizado pelo usuário

    Attribute usuario: Um usuário registrado
    Attribute data_pedido: A data em que foi efetuado o pedido
    Attribute id_transportadora: Uma fk para uma transportadora
    Attribute id_forma_pagamento: Uma fk para uma forma de pagamento
    """

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_pedido = models.DateField(auto_now=True)
    id_transportadora = models.ForeignKey('Transportadora', on_delete=models.CASCADE, default=1)
    id_forma_pagamento = models.ForeignKey('FormaPagamento', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return 'Pedido ' + str(self.id) + ' Usuário ' + self.usuario.username

    @staticmethod
    def receber(usuario):
        if usuario.is_authenticated:
            pedidos = Pedido.objects.filter(usuario=usuario)

        else:
            pedidos = []

        return pedidos

    @staticmethod
    def receber_pagina(usuario):
        pedidos = Pedido.receber(usuario)
        primeiro_produto_pedidos = {}
        for pedido in pedidos:
            produtos = PedidoProduto.objects.filter(id_pedido=pedido)
            primeiro_produto_pedidos.update({pedido.id: produtos[0]})

        return {
            'pedidos': sorted(pedidos, reverse=True, key=lambda pedido: pedido.id),
            'produto_pedidos': primeiro_produto_pedidos,
        }

    @staticmethod
    def receber_pagina_pedido(pedido):
        produtos = list(PedidoProduto.objects.filter(id_pedido=pedido))
        soma_produtos = sum([produto.id_produto.preco * produto.quantidade for produto in produtos])
        valor_final = (soma_produtos - soma_produtos * pedido.id_forma_pagamento.desconto) + pedido.id_transportadora.frete
        return {
            'pedido': pedido, 'produtos': produtos, 'soma_produtos': soma_produtos, 
            'valor_final': valor_final,
        }

    @staticmethod
    def criar_pedido(form, usuario):
        transportadora, forma_pagamento = form.cleaned_data.values()
        transportadora = get_object_or_404(Transportadora, id=int(transportadora))
        forma_pagamento = get_object_or_404(FormaPagamento, id=int(forma_pagamento))
        carrinho = CarrinhoCompra.objects.filter(usuario=usuario)
        if carrinho:
            pedido = Pedido.objects.create(usuario=usuario, id_transportadora=transportadora, id_forma_pagamento=forma_pagamento)
            PedidoProduto.registrar_pedido(pedido, carrinho, usuario)


class PedidoProduto(models.Model):
    """
    Model para registrar os produtos e suas quantidades em um pedido

    Attribute id_pedido: Uma fk de um pedido
    Attribute id_produto: Uma fk de um produto
    Attribute quantidade: Um número inteiro para ser a quantidade do produto
    """

    id_pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    id_produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return 'Pedido ' + str(self.id_pedido.id) + ' Produto ' + self.id_produto.titulo

    @staticmethod
    def registrar_pedido(pedido, carrinho, usuario):
        for queryset in carrinho:
            PedidoProduto.objects.create(id_pedido=pedido, id_produto=queryset.id_produto, quantidade=queryset.quantidade)
            
            # Retirando da lista de desejos os produtos comprados
            lista_desejo = ListaDesejo.objects.filter(usuario=usuario, id_produto=queryset.id_produto)
            lista_desejo.delete()

            # Diminuindo o estoque do produto pela quantidade comprada
            produto = queryset.id_produto
            produto.estoque -= queryset.quantidade
            if produto.estoque <= 0:
                produto.estoque = 100

            produto.save()
        carrinho.delete()


class Transportadora(models.Model):
    """
    Model para registrar as transportadoras disponíveis

    Attribute titulo: Uma string para ser o titulo da transportadora
    Attribute frete: Uma número decimal que será o preço do frete da transportadora
    """

    titulo = models.CharField(max_length=30)
    frete = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.titulo

    @staticmethod
    def receber():
        transportadoras = [[transportadora.id, transportadora.titulo] for transportadora in Transportadora.objects.all()]
        return transportadoras


class FormaPagamento(models.Model):
    """
    Model para registrar as formas de pagamento disponíveis

    Attribute titulo: Uma string para ser o titulo da forma de pagamento
    Attribute desconto: O desconto aplicado no pedido com determinada forma de pagamento
    """

    titulo = models.CharField(max_length=30)
    desconto = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.titulo

    @staticmethod
    def receber():
        formas_pagamento = [[forma_pagamento.id, forma_pagamento.titulo] for forma_pagamento in FormaPagamento.objects.all()]
        return formas_pagamento


def dados_comuns(usuario):
    """Função que retorna o número de produtos no carrinho e todas categorias registradas, 
       dados que são utilizados em diversas partes do projeto"""

    carrinho_compra = CarrinhoCompra.receber(usuario)
    categorias = list(CategoriasProduto.objects.all())
    return {
        'categorias': categorias,
        'numero_produtos_carrinho': len(carrinho_compra),
    }
