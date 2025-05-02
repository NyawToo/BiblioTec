from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Libro, Autor, Prestamo

class UsuarioForm(UserCreationForm):
    direccion = forms.CharField(max_length=200)
    telefono = forms.CharField(max_length=20)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('direccion', 'telefono')

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autores', 'categoria', 'isbn', 'descripcion', 'fecha_publicacion']

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellido', 'biografia']

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'fecha_devolucion_esperada']
        widgets = {
            'fecha_devolucion_esperada': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }