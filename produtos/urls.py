from django.urls import path
from . import views

urlpatterns = [
    path('produto/<int:id_produto>', views.pagina_produto_view, name='pagina_produto'),
    path('busca/<str:busca>', views.BuscaProdutoView.as_view(), name='busca'),
    path('lista_desejos', views.PaginaListaView.as_view(), name='lista_desejos'),
    path('atualizar_lista/<int:id_produto>', views.AtualizarListaView.as_view(), name='atualizar_lista'),
    path('carrinho', views.PaginaCarrinhoView.as_view(), name='carrinho'),
    path('atualizar_carrinho/<int:id_produto>', views.AtualizarCarrinhoView.as_view(), name='atualizar_carrinho'),
    path('alterar_carrinho/<int:id_produto>/<int:quantidade>', views.AlterarCarrinhoView.as_view(), name='alterar_carrinho'),
    path('pedidos', views.PaginaTodosPedidos.as_view(), name='pedidos'),
    path('finalizar_pedido', views.PaginaFinalizarPedido.as_view(), name='finalizar_pedido'),
    path('pedido/<int:id_pedido>', views.PaginaPedido.as_view(), name='pagina_pedido')
]
