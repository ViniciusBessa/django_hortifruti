from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaginaCarrinhoView.as_view(), name='carrinho'),
    path('atualizar/<int:id_produto>', views.AtualizarCarrinhoView.as_view(), name='atualizar_carrinho'),
    path('alterar/<int:id_produto>/<int:quantidade>', views.AlterarCarrinhoView.as_view(), name='alterar_carrinho'),
]
