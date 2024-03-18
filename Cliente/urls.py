from django.urls import path
from . import views

urlpatterns = [
    path('area-cliente/', views.area_cliente, name='area-cliente'),
]
