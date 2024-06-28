from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from . import views
from .views import AgendamentoViewSet, gerenciamento_cadastros_view, cadastros_api_view, contactos_api_view, \
    gerenciamento_contactos_view, user_list_api, atualizar_estado_cadastro

app_name = 'backoffice'
router = DefaultRouter()
router.register(r'agendamentos', AgendamentoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.Login, name='login'),  # Login do backoffice
    path('gerir-agendamentos/', TemplateView.as_view(template_name="backoffice/agendamentos/gerirAgendamentos.html"),
         name='gerir-agendamentos'),
    path('backoffice/', views.LadingPage, name='landingPage'),  # Criar novo usuário
    path('home/', views.LadingPage, name='home_backoffice'),
    path('gerir-cadastros/', gerenciamento_cadastros_view, name='gerenciamento_cadastros'),
    path('api/cadastros/', cadastros_api_view, name='cadastros_api'),  # Certifique-se de que esta URL está correta
    path('api/cadastros/<int:id>/atualizar-estado/', atualizar_estado_cadastro, name='atualizar_estado_cadastro'),

    path('api/contactos/', contactos_api_view, name='contactos_api'),
    path('gerir-contactos/', gerenciamento_contactos_view, name='gerenciamento_contactos'),
    path('api/contactos/<int:contacto_id>/validar/', views.validar_contacto_view, name='validar_contacto'),

    path('users/new/', views.user_create, name='user_create'),  # Criar novo usuário
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('gerir-acessos/', views.Gerir_Acessos, name='Gerir_Acessos'),  # Dashboard do backoffice
    path('api/users/', user_list_api, name='user_list_api'),  # API de listagem de usuários
    # Adicione outras URLs conforme necessário
]
