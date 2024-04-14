# backoffice/urls.py

from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('backoffice/central/', views.central, name='central'),
    path('backoffice/login/', views.backoffice_login, name='login'),
    path('backoffice/home_backoffice', views.home_backoffice, name='home_backoffice'),
    path('editar-cadastro-imagem/<int:pk>/', views.editar_cadastro_imagem, name='editar_cadastro_imagem'),
    path('servico/editar/<str:card_id>/', views.editar_servico, name='editar_servico'),
    path('criar_cliente/', views.create_cliente_user, name='criar_cliente'),
    path('backoffice/logout/', views.backoffice_logout, name='backoffice_logout'),

    # Adicione outras URLs conforme necessário
]
