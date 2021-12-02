from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from core.models import Produto, CarrinhoCompra, ListaDesejo


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
        """Método que retorna todos os pedidos feitos por um usuário"""

        if usuario.is_authenticated:
            pedidos = Pedido.objects.filter(usuario=usuario)

        else:
            pedidos = []

        return pedidos

    @staticmethod
    def receber_pagina(usuario):
        """Método que retorna um dicionário com os dados utilizados pelo view PaginaTodosPedidosView"""

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
        """Método que retorna um dicionário com os dados utilizados pelo view PaginaPedidoView"""

        produtos = list(PedidoProduto.objects.filter(id_pedido=pedido))
        soma_produtos = sum([produto.id_produto.preco * produto.quantidade for produto in produtos])
        valor_final = (soma_produtos - soma_produtos * pedido.id_forma_pagamento.desconto) + pedido.id_transportadora.frete
        return {
            'pedido': pedido, 'produtos': produtos, 'soma_produtos': soma_produtos, 
            'valor_final': valor_final,
        }

    @staticmethod
    def criar_pedido(form, usuario):
        """Método utilizado para criar um novo pedido do usuário"""

        transportadora, forma_pagamento = form.cleaned_data.values()
        transportadora = get_object_or_404(Transportadora, id=int(transportadora))
        forma_pagamento = get_object_or_404(FormaPagamento, id=int(forma_pagamento))
        carrinho = CarrinhoCompra.objects.filter(usuario=usuario)
        if carrinho:
            pedido = Pedido.objects.create(usuario=usuario, id_transportadora=transportadora, id_forma_pagamento=forma_pagamento)
            PedidoProduto.registrar_pedido(pedido, carrinho, usuario)

        raise ValidationError('Seu carrinho de compras está vazio')


class PedidoProduto(models.Model):
    """
    Model para registrar os produtos e suas quantidades em um pedido

    Attribute id_pedido: Uma fk de um pedido
    Attribute id_produto: Uma fk de um produto
    Attribute quantidade: Um número inteiro para ser a quantidade do produto
    """

    id_pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return 'Pedido ' + str(self.id_pedido.id) + ' Produto ' + self.id_produto.titulo

    @staticmethod
    def registrar_pedido(pedido, carrinho, usuario):
        """Método utilizado para registrar todos produtos de um pedido, retirar produtos comprados da
        lista de desejos, retira a quantidade comprada do estoque e aumenta o número de vendas do
        produto"""

        for queryset in carrinho:
            PedidoProduto.objects.create(id_pedido=pedido, id_produto=queryset.id_produto, quantidade=queryset.quantidade)
            
            # Retirando da lista de desejos os produtos comprados
            lista_desejo = ListaDesejo.objects.filter(usuario=usuario, id_produto=queryset.id_produto)
            lista_desejo.delete()

            # Retirando do estoque a quantidade comprada, e aumentando o número de vendas
            produto = queryset.id_produto
            produto.estoque -= queryset.quantidade
            produto.vendas += queryset.quantidade

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
        """Método que retorna uma lista com sublistas contendo o id de cada transportadora e seu nome"""

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
        """Método que retorna uma lista com sublistas contendo o id de cada forma de pagamento 
        e seu nome"""

        formas_pagamento = [[forma_pagamento.id, forma_pagamento.titulo] for forma_pagamento in FormaPagamento.objects.all()]
        return formas_pagamento
