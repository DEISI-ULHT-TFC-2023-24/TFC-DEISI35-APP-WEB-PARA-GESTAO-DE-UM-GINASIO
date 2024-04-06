from django import forms
from .models import CampanhaPromocional, BlogPost, EventoDestaque

class CampanhaPromocionalForm(forms.ModelForm):
    class Meta:
        model = CampanhaPromocional
        fields = '__all__'

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'

class EventoDestaqueForm(forms.ModelForm):
    class Meta:
        model = EventoDestaque
        fields = '__all__'
