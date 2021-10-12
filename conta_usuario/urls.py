from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_view, name='registrar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('alterar_senha/', views.alterar_senha_view, name='alterar_senha'),
]
