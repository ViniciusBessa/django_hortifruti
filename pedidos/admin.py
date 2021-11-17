from django.contrib import admin
from .models import Pedido, PedidoProduto, Transportadora, FormaPagamento

admin.site.register((Pedido, PedidoProduto, Transportadora, FormaPagamento))
