# backoffice/forms.py
from django import forms
from Cliente.models import CadastroImage, Servico


class CadastroImageForm(forms.ModelForm):
    class Meta:
        model = CadastroImage
        fields = ['image']


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['titulo', 'descricao', 'imagem', 'link',
                  'card2_titulo', 'card2_descricao', 'card2_imagem', 'card2_link',
                  'card3_titulo', 'card3_descricao', 'card3_imagem', 'card3_link',
                  'card4_titulo', 'card4_descricao', 'card4_imagem', 'card4_link']
