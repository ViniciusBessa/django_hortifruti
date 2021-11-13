from django.contrib import admin
from .models import Produto, CategoriasProduto, CarrinhoCompra, ListaDesejo, Pedido, PedidoProduto, FormaPagamento, \
                    Transportadora

admin.site.register((Produto, CategoriasProduto, CarrinhoCompra, ListaDesejo,
                     Pedido, PedidoProduto, FormaPagamento, Transportadora))
