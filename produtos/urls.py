from django.urls import path
from . import views

urlpatterns = [
    path('produto/<int:id_produto>', views.pagina_produto_view, name='pagina_produto'),
    path('filtro_busca/', views.filtro_busca_view, name='filtro_busca'),
    path('busca/<str:busca>', views.busca_produto_view, name='busca'),
]
