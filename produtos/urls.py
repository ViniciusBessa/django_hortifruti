from django.urls import path
from . import views

urlpatterns = [
    path('produto/<int:id_produto>', views.pagina_produto_view, name='pagina_produto'),
    path('filtro_busca/', views.filtro_busca_view, name='filtro_busca'),
    path('busca/<str:busca>', views.busca_produto_view, name='busca'),
    path('lista_desejos/', views.pagina_lista_desejos_view, name='lista_desejos'),
    path('atualizar_lista/<int:id_produto>', views.AtualizarListaView.as_view(), name='atualizar_lista'),
    path('carrinho/', views.pagina_carrinho_view, name='carrinho'),
    path('atualizar_carrinho/<int:id_produto>', views.AtualizarCarrinhoView.as_view(), name='atualizar_carrinho'),
    path('alterar_carrinho/<int:id_produto>/<int:quantidade>/', views.alterar_carrinho_view, name='alterar_carrinho'),
]
