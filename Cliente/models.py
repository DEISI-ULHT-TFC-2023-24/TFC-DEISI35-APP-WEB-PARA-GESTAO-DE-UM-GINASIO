from django.core.mail import send_mail
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


# Create your models here.
from django.contrib.auth.models import User

class CampanhaPromocional(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='campanhas')
    data_validade = models.DateField()

class BlogPost(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='posts')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    data_publicacao = models.DateTimeField(auto_now_add=True)

class EventoDestaque(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='eventos')
    data_evento = models.DateTimeField()
    link = models.URLField()






class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    nif = models.CharField(max_length=9, unique=True)
    data_nascimento = models.DateField()
    email = models.EmailField(unique=True)
    contacto = models.CharField(max_length=15)
    endereco = models.TextField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')])
    data_inicio = models.DateField()
    plano = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo'), ('Cancelado', 'Cancelado')])

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.method = None
        self.POST = None

    def __str__(self):
        return self.nome

    def enviar_email(request):
        if request.method == 'POST':
            # Aqui você processaria os dados do formulário, por exemplo:
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            mensagem = request.POST.get('mensagem')
            # Lógica para enviar o e-mail
            try:
                send_mail(
                    'Assunto do Email',
                    f'Mensagem de {nome} ({email}): {mensagem}',
                    'email_do_remetente@seusite.com',  # O e-mail que você está enviando.
                    ['destinatario@example.com'],  # Para quem você está enviando.
                    fail_silently=False,
                )
                return HttpResponse("Email enviado com sucesso!")
            except Exception as e:
                return HttpResponse("Falha ao enviar o email.")
        else:
            # Se não for um POST, redirecionar para o formulário, por exemplo
            return redirect(reverse('nome_da_url_para_o_formulário'))

