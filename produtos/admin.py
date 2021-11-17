from django.contrib import admin
from .models import Produto, CategoriasProduto

admin.site.register((Produto, CategoriasProduto))
