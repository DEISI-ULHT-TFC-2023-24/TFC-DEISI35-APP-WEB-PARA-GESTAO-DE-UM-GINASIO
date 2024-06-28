# ptclinic/cliente/urls.py
from django.urls import path
from . import views
from .views import cadastro_view, contacto_view

urlpatterns = [
    path('', views.LadingPage, name='cliente_base'),
    path('cliente/agendar', views.Agendamento, name='agendar'),
    path('cadastro/', cadastro_view, name='cadastro'),  # URL de cadastro
    path('contacto/', contacto_view, name='contacto'),  # URL de contato
]
