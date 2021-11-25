from django.urls import path
from . import views

urlpatterns = [
    path('produto/<int:id_produto>/', views.PaginaProdutoView.as_view(), name='pagina_produto'),
    path('busca/<str:busca>/', views.BuscaProdutoView.as_view(), name='busca'),
    path('categorias/<str:categoria>/', views.PaginaCategoriasView.as_view(), name='categorias'),
    path('carrinho/', views.PaginaCarrinhoView.as_view(), name='carrinho'),
    path('carrinho/atualizar/<int:id_produto>/', views.AtualizarCarrinhoView.as_view(), name='atualizar_carrinho'),
    path('carrinho/alterar/<int:id_produto>/<int:quantidade>/', views.AlterarCarrinhoView.as_view(), name='alterar_carrinho'),
    path('lista_desejos/', views.PaginaListaView.as_view(), name='lista_desejos'),
    path('lista_desejos/atualizar/<int:id_produto>/', views.AtualizarListaView.as_view(), name='atualizar_lista'),
]
