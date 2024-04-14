# backoffice/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.cache import never_cache

from Cliente.models import CadastroImage, Servico
from backoffice.forms import ServicoForm, ClienteUserForm, CadastroImageForm


# backoffice/views.py

def central(request):
    return render(request, 'backoffice/central-page/central.html')

def home_backoffice(request):
    cadastro_image = CadastroImage.objects.first()  # Assume-se que haja apenas uma imagem de cadastro
    servicos = Servico.objects.first()  # Assume-se que haja apenas um conjunto de serviços
    context = {
        'cadastro_image': cadastro_image,
        'servicos': servicos,
    }
    return render(request, 'backoffice/home/home_backoffice.html', context)


@login_required
def editar_cadastro_imagem(request, pk):
    imagem = get_object_or_404(CadastroImage, pk=pk)
    if not request.user.is_staff:
        return redirect(
            'backoffice:home_backoffice')  # Assumindo que 'home' é a view que você quer redirecionar usuários não-admin

    if request.method == 'POST':
        form = CadastroImageForm(request.POST, request.FILES, instance=imagem)
        if form.is_valid():
            form.save()
            return redirect('backoffice:home_backoffice')  # Use o namespace apropriado e o nome da view
    else:
        form = CadastroImageForm(instance=imagem)

    return render(request, 'backoffice/home/editar_cadastro_imagem.html', {'form': form})


# Sua view no views.py
@login_required
def editar_servico(request, card_id):
    # Supondo que sempre haverá apenas um objeto Servico.
    servico, created = Servico.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('backoffice:home_backoffice')
    else:
        form = ServicoForm(instance=servico)

    # Você passa card_id para o contexto para saber qual card está editando
    context = {
        'form': form,
        'card_id': card_id,
    }

    return render(request, 'backoffice/home/editar_servico.html', context)


def check_is_staff(user):
    return user.is_staff


def backoffice_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active and user.is_staff:
                    login(request, user)
                    return redirect(reverse('backoffice:home_backoffice'))
                else:
                    messages.error(request, 'A conta não tem permissões para acessar essa área.')
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'backoffice/login-backoffice/login.html', {'form': form})


@never_cache
def backoffice_logout(request):
        logout(request)
        return redirect('backoffice:login')

def create_cliente_user(request):
    if request.method == 'POST':
        form = ClienteUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            # Aqui você pode redirecionar para a página de sucesso ou de listagem de usuários
            return redirect('backoffice:central')
    else:
        form = ClienteUserForm()
    return render(request, 'backoffice/cliente-user-account/criar_cliente.html', {'form': form})
