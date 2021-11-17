from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaginaListaView.as_view(), name='lista_desejos'),
    path('atualizar/<int:id_produto>', views.AtualizarListaView.as_view(), name='atualizar_lista'),
]
