from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Libro, Autor, Categoria
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class BibliotecarioCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'categoria', 'isbn', 'fecha_publicacion',
                 'estado', 'descripcion', 'imagen', 'imagen_url']
        widgets = {
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        imagen = cleaned_data.get('imagen')
        imagen_url = cleaned_data.get('imagen_url')

        if imagen and imagen_url:
            raise ValidationError(_('Por favor, proporciona solo una imagen o una URL de imagen, no ambas.'))

        if not imagen and not imagen_url:
            raise ValidationError(_('Debes proporcionar una imagen o una URL de imagen.'))

        if imagen:
            if imagen.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError(_('El tamaño de la imagen no debe exceder 5MB.'))
            if not imagen.content_type.startswith('image/'):
                raise ValidationError(_('El archivo debe ser una imagen.'))

        return cleaned_data

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellido', 'nacionalidad', 'biografia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-select'}),
            'biografia': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del autor',
            'apellido': 'Apellido del autor',
            'nacionalidad': 'País de origen',
            'biografia': 'Biografía'
        }
        help_texts = {
            'nacionalidad': 'Seleccione el país de origen del autor'
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }