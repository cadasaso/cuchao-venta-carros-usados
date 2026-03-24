from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Carro

class UsuarioCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Email válido.')
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('Este usuario ya existe.')
        return username

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ['modelo', 'descripcion', 'imagen', 'precio']