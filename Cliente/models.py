from django.db import models

# Create your models here.
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

    def __str__(self):
        return self.nome
