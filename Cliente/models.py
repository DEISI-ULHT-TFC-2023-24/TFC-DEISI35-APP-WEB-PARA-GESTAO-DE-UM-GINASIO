from django.core.mail import send_mail
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


# Create your models here.
# Continua armazenando informações sobre os clientes do ginásio.
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome


# Um novo modelo para definir diferentes serviços que podem ser agendados, como avaliações físicas, nutrição, etc.
class Servico(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


# Relaciona um cliente a um serviço em uma data e hora específicas.
class Agendamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="agendamento")
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.servico.nome} em {self.data_hora.strftime('%Y-%m-%d %H:%M')} - {self.cliente.nome}"

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


class CadastroImage(models.Model):
    image = models.ImageField(upload_to='cadastro_images')

    def __str__(self):
        return "Imagem de Cadastro"

