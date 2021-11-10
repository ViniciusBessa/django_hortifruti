from django.db import models
from django.shortcuts import get_object_or_404
from more_itertools import divide
from django.contrib.auth.models import User


class Produto(models.Model):
    titulo = models.CharField(max_length=30)
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

    def receber_pagina(usuario, categoria):
        categorias = CategoriasProduto.objects.all()
        categoria = get_object_or_404(CategoriasProduto, titulo=categoria.title())
        produtos = Produto.objects.filter(id_categoria=categoria)

        return {
            'categoria': categoria,
            'produtos': produtos,
        } 


class ListaDesejo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_produto = models.ForeignKey('Produto', on_delete=models.CASCADE)


    def receber(usuario):
        if usuario.is_authenticated:
            lista_desejos = ListaDesejo.objects.filter(usuario=usuario)
            lista_desejos = [lista.id_produto for lista in lista_desejos]

        else:
            lista_desejos = []

        return lista_desejos


    def receber_pagina(usuario):
        lista_desejos = ListaDesejo.receber(usuario)
        return {
            'lista_desejos': lista_desejos, 
        }


class CarrinhoCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)


    def receber(usuario):
        if usuario.is_authenticated:
            carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
            carrinho_compra = [lista.id_produto for lista in carrinho_compra]

        else:
            carrinho_compra = []

        return sorted(carrinho_compra, key=lambda produto: produto.titulo)


    def receber_soma_carrinho(usuario):
        carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
        subtotal = sum(lista.id_produto.preco * lista.quantidade for lista in carrinho_compra)
        return subtotal


    def receber_quantidade_produtos(usuario):
        carrinho_compra = CarrinhoCompra.objects.filter(usuario=usuario)
        quantidades = {lista.id_produto: lista.quantidade for lista in carrinho_compra}
        return quantidades


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
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_pedido = models.DateField(auto_now=True)
    id_transportadora = models.ForeignKey('Transportadora', on_delete=models.CASCADE, default=1)
    id_forma_pagamento = models.ForeignKey('FormaPagamento', on_delete=models.CASCADE, default=1)


    def receber(usuario):
        if usuario.is_authenticated:
            pedidos = Pedido.objects.filter(usuario=usuario)

        else:
            pedidos = []

        return pedidos

    def receber_pagina(usuario):
        pedidos = Pedido.receber(usuario)
        primeiro_produto_pedidos = {}
        for pedido in pedidos:
            produtos = PedidoProduto.objects.filter(id_pedido=pedido)
            primeiro_produto_pedidos.update({pedido.id: produtos[0]})

        return {
            'pedidos': sorted(pedidos, reverse=True, key=lambda pedido: pedido.id) ,
            'produto_pedidos': primeiro_produto_pedidos,
        }
    

    def receber_finalizacao(usuario):
        transportadoras = Transportadora.objects.all()
        formas_pagamento = FormaPagamento.objects.all()

        return {
            'transportadoras': transportadoras,
            'formas_pagamento': formas_pagamento,
        }


    def receber_pagina_pedido(usuario, pedido):
        produtos = list(PedidoProduto.objects.filter(id_pedido=pedido))
        soma_produtos = sum([produto.id_produto.preco * produto.quantidade for produto in produtos])
        valor_final = (soma_produtos - soma_produtos * pedido.id_forma_pagamento.desconto) + pedido.id_transportadora.frete
        return {
            'pedido': pedido, 'produtos': produtos, 'soma_produtos': soma_produtos, 
            'valor_final': valor_final,
        }


    def criar_pedido(form, usuario):
        transportadora, forma_pagamento = form.cleaned_data.values()
        transportadora = get_object_or_404(Transportadora, id=int(transportadora))
        forma_pagamento = get_object_or_404(FormaPagamento, id=int(forma_pagamento))
        carrinho = CarrinhoCompra.objects.filter(usuario=usuario)
        if carrinho:
            pedido = Pedido.objects.create(usuario=usuario, id_transportadora=transportadora, id_forma_pagamento=forma_pagamento)
            PedidoProduto.registrar_pedido(pedido, carrinho)


class PedidoProduto(models.Model):
    id_pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    id_produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)


    def registrar_pedido(pedido, carrinho):
        for queryset in carrinho:
            PedidoProduto.objects.create(id_pedido=pedido, id_produto=queryset.id_produto, quantidade=queryset.quantidade)
        carrinho.delete()


class Transportadora(models.Model):
    titulo = models.CharField(max_length=30)
    frete = models.DecimalField(max_digits=6, decimal_places=2)


class FormaPagamento(models.Model):
    titulo = models.CharField(max_length=30)
    desconto = models.DecimalField(max_digits=3, decimal_places=2)


def dados_comuns(usuario):
    carrinho_compra = CarrinhoCompra.receber(usuario)
    categorias = list(CategoriasProduto.objects.all())
    return {
        'categorias': categorias,
        'numero_produtos_carrinho': len(carrinho_compra),
    }
