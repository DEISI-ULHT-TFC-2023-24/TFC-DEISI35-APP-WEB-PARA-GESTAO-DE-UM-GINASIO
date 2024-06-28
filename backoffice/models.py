from datetime import time, timedelta, datetime, date

from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError

# models.py
from django.db import models

class Cadastro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telemovel = models.CharField(max_length=20)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    usuario_acao = models.CharField(max_length=100, null=True, blank=True)
    data_acao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    TIPO_CHOICES = [
        ('Consulta', 'Consulta'),
        ('Visita', 'Visita'),
        ('Avaliação Física', 'Avaliação Física'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    data = models.DateField()
    hora = models.TimeField()
    email = models.EmailField()
    contato = models.CharField(max_length=20)
    nota = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.tipo} em {self.data} às {self.hora}'

    def clean(self):
        # Verificar horário de funcionamento
        if self.data.weekday() == 6:  # Domingo
            raise ValidationError('O ginásio está fechado aos domingos.')

        hora_abertura, hora_fechamento = self.get_horarios_funcionamento()

        if not (hora_abertura <= self.hora <= hora_fechamento):
            raise ValidationError(
                f'Horário de agendamento inválido. O ginásio abre às {hora_abertura} e fecha às {hora_fechamento}.')

        # Verificar sobreposição
        duracao = self.get_duracao()
        hora_fim = (datetime.combine(date.today(), self.hora) + duracao).time()

        agendamentos_conflitantes = Agendamento.objects.filter(
            data=self.data,
            hora__lt=hora_fim,
            hora__gte=self.hora
        ).exclude(pk=self.pk)

        if agendamentos_conflitantes.exists():
            raise ValidationError('Já existe um agendamento neste horário.')

    def get_horarios_funcionamento(self):
        if self.data.weekday() in [0, 1, 2, 3, 4]:  # Segunda a sexta
            return time(7, 0), time(21, 30)
        elif self.data.weekday() == 5:  # Sábado
            return time(9, 0), time(13, 0)
        return None, None

    def get_duracao(self):
        if self.tipo == 'Consulta':
            return timedelta(hours=1)
        elif self.tipo == 'Visita':
            return timedelta(minutes=30)
        elif self.tipo == 'Avaliação Física':
            return timedelta(minutes=45)
        return timedelta(0)

    def save(self, *args, **kwargs):
        self.clean()  # Chamar validação antes de salvar
        super().save(*args, **kwargs)


class Contacto(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    mensagem = models.TextField()
    data_contacto = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    validado_por = models.CharField(max_length=255, null=True, blank=True)
    data_acao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nome

