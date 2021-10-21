from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.RegistrarView.as_view(), name='registrar'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('alterar_senha/', views.AlterarSenhaView.as_view(), name='alterar_senha'),
]
