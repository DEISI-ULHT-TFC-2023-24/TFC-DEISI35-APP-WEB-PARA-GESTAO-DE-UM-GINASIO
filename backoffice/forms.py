# forms.py

from django import forms
from django.contrib.auth.models import User

from backoffice.models import Cadastro
from cliente.models import CadastroImage


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirme a senha")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.pk is None and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nome de usuário já está em uso.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Inclua outros campos que você deseja permitir que sejam editados

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        # Customize os campos se necessário
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CadastroForm(forms.ModelForm):
    class Meta:
        model = Cadastro
        fields = ['nome', 'email', 'telemovel']
