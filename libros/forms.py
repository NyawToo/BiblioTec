from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BibliotecarioCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Marca como bibliotecario
        if commit:
            user.save()
        return user