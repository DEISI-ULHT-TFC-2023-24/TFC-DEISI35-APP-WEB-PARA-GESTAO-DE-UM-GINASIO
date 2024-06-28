from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from cliente.forms import CadastroForm, ContactoForm
from cliente.models import CadastroImage, Servico


# Create your views here.

def LadingPage(request):
    cadastro_image = CadastroImage.objects.first()  # Apenas uma imagem de cadastro
    servicos = Servico.objects.all()  # Obtém todos os objetos Servico
    context = {
        'cadastro_image': cadastro_image,
        'servicos': servicos,
    }
    return render(request, 'cliente/ladingPage/index.html')

def Agendamento(resquest):
    return render(resquest, 'cliente/agendamento/agendar.html')


def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            cadastro = form.save()
            send_mail(
                'Novo Cadastro Recebido',
                f'Nome: {cadastro.nome}\nEmail: {cadastro.email}\nTelemóvel: {cadastro.telemovel}',
                settings.EMAIL_HOST_USER,
                [settings.BACKOFFICE_EMAIL],
                fail_silently=False,
            )
            return render(request, 'cliente/ladingPage/index.html', {'form': form, 'success': True})
    else:
        form = CadastroForm()
    return render(request, 'cliente/ladingPage/index.html', {'form': form})


def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save()
            send_mail(
                'Novo Contacto Recebido',
                f'Nome: {contacto.nome}\nEmail: {contacto.email}\nMensagem: {contacto.mensagem}',
                settings.EMAIL_HOST_USER,
                [settings.BACKOFFICE_EMAIL],
                fail_silently=False,
            )
            return render(request, 'cliente/ladingPage/index.html', {'form': form, 'success': True})
    else:
        form = ContactoForm()
    return render(request, 'cliente/ladingPage/index.html', {'form': form})