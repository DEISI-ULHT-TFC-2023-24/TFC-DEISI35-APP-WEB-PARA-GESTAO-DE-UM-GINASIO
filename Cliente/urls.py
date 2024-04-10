# Cliente/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cliente/area-cliente/', views.cliente, name='area_cliente'),
    path('cliente/login/', views.login_view, name='login_view'),
    path('cliente/logout/', views.logout_view, name='logout'),
    # Certifique-se de que o name='area_cliente' está correto aqui
]
