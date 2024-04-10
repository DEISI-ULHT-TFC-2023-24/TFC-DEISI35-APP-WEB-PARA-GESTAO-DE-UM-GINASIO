# Cliente/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('area-cliente/', views.cliente, name='area_cliente'),
    path('login/', views.login, name='login'),
    # Certifique-se de que o name='area_cliente' está correto aqui

]
