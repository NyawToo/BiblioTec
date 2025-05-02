from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        ordering = ['apellido', 'nombre']

class Libro(models.Model):
    CATEGORIAS = [
        ('FICCION', 'Ficción'),
        ('NO_FICCION', 'No Ficción'),
        ('CIENCIA', 'Ciencia'),
        ('TECNOLOGIA', 'Tecnología'),
        ('HISTORIA', 'Historia'),
        ('ARTE', 'Arte'),
    ]

    ESTADOS = [
        ('DISPONIBLE', 'Disponible'),
        ('PRESTADO', 'Prestado'),
        ('RESERVADO', 'Reservado'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
    ]

    titulo = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor, related_name='libros')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    isbn = models.CharField(max_length=13, unique=True)
    descripcion = models.TextField(blank=True)
    fecha_publicacion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='DISPONIBLE')
    fecha_adquisicion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['titulo']

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateTimeField(default=timezone.now)
    fecha_devolucion_esperada = models.DateTimeField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"

    def esta_vencido(self):
        if not self.devuelto and timezone.now() > self.fecha_devolucion_esperada:
            return True
        return False

    class Meta:
        ordering = ['-fecha_prestamo']
