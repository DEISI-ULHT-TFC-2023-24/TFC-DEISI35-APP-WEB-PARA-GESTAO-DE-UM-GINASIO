from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    # Adicione campos adicionais aqui, se você tiver um modelo de perfil de usuário

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

