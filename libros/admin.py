from django.contrib import admin
from .models import Libro, Autor, Categoria, Prestamo

admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Categoria)
admin.site.register(Prestamo)