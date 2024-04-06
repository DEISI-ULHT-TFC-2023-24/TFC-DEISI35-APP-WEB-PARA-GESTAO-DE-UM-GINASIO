# Cliente/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('area-cliente/', views.cliente, name='area_cliente'),
    path('home/', views.home, name='home'),
    # Certifique-se de que o name='area_cliente' está correto aqui
]
