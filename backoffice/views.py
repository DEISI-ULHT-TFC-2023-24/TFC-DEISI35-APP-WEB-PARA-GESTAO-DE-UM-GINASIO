import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from backoffice.forms import UserCreationForm, UserEditForm
from backoffice.models import Agendamento, Cadastro, Contacto
from backoffice.serializers import AgendamentoSerializer
from cliente.models import CadastroImage

def check_is_staff(user):
    return user.is_staff
@login_required
@user_passes_test(check_is_staff)
def LadingPage(request):
    return render(request, 'backoffice/landingPage/landingPage.html')

@login_required
@user_passes_test(check_is_staff)
def gerenciamento_cadastros_view(request):
    return render(request, 'backoffice/cadastro/gerirCadastros.html')

@login_required
@user_passes_test(check_is_staff)
def cadastros_api_view(request):
    cadastros = Cadastro.objects.all().values('id', 'nome', 'email', 'telemovel', 'data_cadastro', 'estado', 'usuario_acao', 'data_acao')
    return JsonResponse(list(cadastros), safe=False)

@csrf_exempt
@login_required
@user_passes_test(check_is_staff)
def atualizar_estado_cadastro(request, id):
    if request.method == 'POST':
        try:
            cadastro = Cadastro.objects.get(id=id)
            data = json.loads(request.body)
            cadastro.estado = data['estado']
            cadastro.usuario_acao = data['usuario_acao']
            cadastro.data_acao = data['data_acao']
            cadastro.save()
            return JsonResponse({'success': True})
        except Cadastro.DoesNotExist:
            return HttpResponseBadRequest('Cadastro não encontrado')
        except Exception as e:
            return HttpResponseBadRequest(f'Erro: {str(e)}')
    else:
        return HttpResponseBadRequest('Método não permitido')

def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active and user.is_staff:
                    login(request, user)
                    return redirect(reverse('backoffice:landingPage'))
                else:
                    messages.error(request, 'A conta não tem permissões para acessar essa área.')
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'backoffice/login/login.html', {'form': form})

@login_required
@user_passes_test(check_is_staff)
def user_list_api(request):
    if request.method == 'GET':
        users = User.objects.filter(is_staff=True).values('id', 'username', 'email', 'date_joined')
        users_list = list(users)
        return JsonResponse(users_list, safe=False)

@login_required
@user_passes_test(check_is_staff)
def Gerir_Acessos(request):
    users = User.objects.filter(is_staff=True)  # Filtra apenas usuários que são staff
    return render(request, 'backoffice/admin/gerirAcessos.html', {'users': users})

@login_required
@user_passes_test(check_is_staff)
def user_create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo usuário adicionado com sucesso!')
            return redirect('backoffice:home_backoffice')
    else:
        form = UserCreationForm()
    return render(request, 'backoffice/admin/userCreate.html', {'form': form})

@login_required
@user_passes_test(check_is_staff)
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('backoffice:home_backoffice')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'backoffice/admin/userEdit.html', {'user': user, 'form': form})

@login_required
@user_passes_test(check_is_staff)
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário apagado com sucesso!')
        return redirect('backoffice:home_backoffice')
    return render(request, 'backoffice/admin/userDelete.html', {'user': user})

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all().order_by('-criado_em')
    serializer_class = AgendamentoSerializer

    def perform_create(self, serializer):
        agendamento = serializer.save()
        enviar_notificacao_email(agendamento)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        agendamento = Agendamento(**serializer.validated_data)

        try:
            agendamento.clean()  # Validações de horários e sobreposição
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def enviar_notificacao_email(agendamento):
    assunto = f'Novo Agendamento: {agendamento.nome}'
    mensagem = f'''
    Novo agendamento recebido.

    Nome: {agendamento.nome}
    Tipo: {agendamento.tipo}
    Data: {agendamento.data}
    Hora: {agendamento.hora}
    Email: {agendamento.email}
    Contato: {agendamento.contato}
    Nota: {agendamento.nota if agendamento.nota else 'N/A'}
    '''
    destinatario = settings.BACKOFFICE_EMAIL
    send_mail(assunto, mensagem, settings.DEFAULT_FROM_EMAIL, [destinatario])

@login_required
@user_passes_test(check_is_staff)
def gerenciamento_contactos_view(request):
    return render(request, 'backoffice/contactos/gerirContactos.html')

@login_required
@user_passes_test(check_is_staff)
def contactos_api_view(request):
    contactos = Contacto.objects.all().values('id', 'nome', 'email', 'mensagem', 'data_contacto', 'estado', 'validado_por', 'data_acao')
    return JsonResponse(list(contactos), safe=False)

@csrf_exempt
@login_required
@user_passes_test(check_is_staff)
def validar_contacto_view(request, contacto_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contacto = Contacto.objects.get(id=contacto_id)
            contacto.estado = data.get('estado', contacto.estado)
            contacto.validado_por = data.get('validado_por', contacto.validado_por)
            contacto.data_acao = timezone.now() if contacto.estado else None
            contacto.save()
            return JsonResponse({'success': True})
        except Contacto.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Contacto não encontrado'})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})
