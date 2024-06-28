from django import forms
from backoffice.models import Cadastro, Contacto


class CadastroForm(forms.ModelForm):
    class Meta:
        model = Cadastro
        fields = ['nome', 'email', 'telemovel']

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nome', 'email', 'mensagem']