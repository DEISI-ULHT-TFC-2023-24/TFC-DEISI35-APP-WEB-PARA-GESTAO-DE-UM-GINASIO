# backoffice/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from Cliente.models import CadastroImage, Servico
from .forms import CadastroImageForm, ServicoForm


# backoffice/views.py


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


@login_required
@user_passes_test(check_is_staff)
def adicionar_cadastro_imagem(request):
    if request.method == 'POST':
        form = CadastroImageForm(request.POST, request.FILES)
        if form.is_valid():
            nova_imagem = form.save(commit=False)
            nova_imagem.save()
            # Redirecionar para onde você precisa após o sucesso
            return redirect('backoffice:home_backoffice')
        else:
            # Se o formulário não for válido, você pode querer ver os erros
            print(form.errors)
    else:
        form = CadastroImageForm()

    return render(request, 'backoffice/home/adicionar_cadastro_imagem.html', {'form': form})
