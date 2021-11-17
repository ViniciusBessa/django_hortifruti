from django.urls import path
from . import views

urlpatterns = [
    path('pedidos/', views.PaginaTodosPedidosView.as_view(), name='pedidos'),
    path('pedido/<int:id_pedido>', views.PaginaPedidoView.as_view(), name='pagina_pedido'),
    path('finalizar_pedido', views.PaginaFinalizarPedidoView.as_view(), name='finalizar_pedido'),
]
