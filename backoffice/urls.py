# backoffice/urls.py

from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('backoffice/login/', views.backoffice_login, name='login'),
    path('backoffice/home_backoffice', views.home_backoffice, name='home_backoffice'),
    path('editar-cadastro-imagem/<int:pk>/', views.editar_cadastro_imagem, name='editar_cadastro_imagem'),
    path('adicionar-cadastro-imagem/', views.adicionar_cadastro_imagem, name='adicionar_cadastro_imagem'),
    path('servico/editar/<str:card_id>/', views.editar_servico, name='editar_servico'),

    # Adicione outras URLs conforme necessário
]
