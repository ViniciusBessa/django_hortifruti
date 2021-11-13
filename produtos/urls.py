from django.urls import path
from . import views

urlpatterns = [
    path('produto/<int:id_produto>', views.PaginaProdutoView.as_view(), name='pagina_produto'),
    path('busca/<str:busca>', views.BuscaProdutoView.as_view(), name='busca'),
    path('lista_desejos', views.PaginaListaView.as_view(), name='lista_desejos'),
    path('atualizar_lista/<int:id_produto>', views.AtualizarListaView.as_view(), name='atualizar_lista'),
    path('carrinho', views.PaginaCarrinhoView.as_view(), name='carrinho'),
    path('atualizar_carrinho/<int:id_produto>', views.AtualizarCarrinhoView.as_view(), name='atualizar_carrinho'),
    path('alterar_carrinho/<int:id_produto>/<int:quantidade>', views.AlterarCarrinhoView.as_view(), name='alterar_carrinho'),
    path('categorias/<str:categoria>', views.PaginaCategoriasView.as_view(), name='categorias'),
    path('pedidos', views.PaginaTodosPedidosView.as_view(), name='pedidos'),
    path('pedido/<int:id_pedido>', views.PaginaPedidoView.as_view(), name='pagina_pedido'),
    path('finalizar_pedido', views.PaginaFinalizarPedidoView.as_view(), name='finalizar_pedido'),
]
