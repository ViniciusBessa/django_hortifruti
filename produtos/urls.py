from django.urls import path
from . import views

urlpatterns = [
    path('produto/<int:id_produto>', views.PaginaProdutoView.as_view(), name='pagina_produto'),
    path('busca/<str:busca>', views.BuscaProdutoView.as_view(), name='busca'),
    path('categorias/<str:categoria>', views.PaginaCategoriasView.as_view(), name='categorias'),
]
