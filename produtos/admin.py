from django.contrib import admin
from .models import Produto, CategoriasProduto, CarrinhoCompra

admin.site.register((Produto, CategoriasProduto, CarrinhoCompra))
