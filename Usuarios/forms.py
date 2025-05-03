from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingrese una dirección de correo electrónico válida.')
    direccion = forms.CharField(max_length=200)
    telefono = forms.CharField(max_length=20)
    codigo_autenticacion = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.PasswordInput,
        help_text='Si desea registrarse como bibliotecario, ingrese el código de autenticación.'
    )
    role = forms.ChoiceField(
        choices=[
            ('USUARIO', 'Usuario'),
            ('BIBLIOTECARIO', 'Bibliotecario')
        ],
        initial='USUARIO',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'direccion', 'telefono', 'role')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        codigo = cleaned_data.get('codigo_autenticacion')

        if role == 'BIBLIOTECARIO':
            if not codigo:
                raise forms.ValidationError('El código de autenticación es requerido para registrarse como bibliotecario.')
            elif codigo != 'NYAW123456789':
                raise forms.ValidationError('Código de autenticación inválido.')

        return cleaned_data

class NotificacionesForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'notificacion_prestamo', 'notificacion_vencimiento', 'notificacion_devolucion']
        labels = {
            'email': 'Correo electrónico',
            'notificacion_prestamo': 'Notificaciones de préstamos nuevos',
            'notificacion_vencimiento': 'Recordatorios de vencimiento',
            'notificacion_devolucion': 'Confirmaciones de devolución'
        }
        help_texts = {
            'email': 'Dirección de correo electrónico donde recibirás las notificaciones',
            'notificacion_prestamo': 'Recibe un correo cuando tomes prestado un libro',
            'notificacion_vencimiento': 'Recibe recordatorios cuando un préstamo esté por vencer',
            'notificacion_devolucion': 'Recibe confirmación cuando devuelvas un libro'
        }