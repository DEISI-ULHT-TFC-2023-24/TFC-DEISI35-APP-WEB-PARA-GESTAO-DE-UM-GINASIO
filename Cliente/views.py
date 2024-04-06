from django.shortcuts import render
from .models import CampanhaPromocional, BlogPost, EventoDestaque
def cliente(request):
    campanhas = CampanhaPromocional.objects.all()
    posts = BlogPost.objects.all()
    eventos = EventoDestaque.objects.all()
    return render(request, 'area-cliente.html', {
        'campanhas': campanhas,
        'posts': posts,
        'eventos': eventos
    })

def home(request):
    return render(request, 'home.html')