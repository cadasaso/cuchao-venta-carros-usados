from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Carro, Resena, Mensaje, Oferta


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


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'ciudad', 'bio', 'avatar']


class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = [
            'modelo', 'marca', 'anio', 'kilometraje', 'color',
            'transmision', 'combustible', 'categoria', 'estado',
            'ciudad', 'descripcion', 'imagen', 'precio',
            'precio_negociable', 'etiquetas',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'etiquetas': forms.CheckboxSelectMultiple(),
        }


class ResenaForm(forms.ModelForm):
    calificacion = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Resena
        fields = ['calificacion', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comparte tu experiencia...'}),
        }


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu mensaje...'}),
        }


class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['monto', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 2, 'placeholder': '¿Por qué esta oferta? (opcional)'}),
            'monto': forms.NumberInput(attrs={'placeholder': 'Tu oferta en $', 'min': '1'}),
        }
