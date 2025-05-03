from django.db import models
from django.utils import timezone
from Usuarios.models import Usuario

class Autor(models.Model):
    NACIONALIDADES = [
        ('AR', 'Argentina'),
        ('BO', 'Bolivia'),
        ('BR', 'Brasil'),
        ('CL', 'Chile'),
        ('CO', 'Colombia'),
        ('EC', 'Ecuador'),
        ('ES', 'España'),
        ('MX', 'México'),
        ('PE', 'Perú'),
        ('PY', 'Paraguay'),
        ('UY', 'Uruguay'),
        ('VE', 'Venezuela'),
        ('OT', 'Otra')
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=2, choices=NACIONALIDADES, default='OT')
    biografia = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        ordering = ['apellido', 'nombre']

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('PRESTADO', 'Prestado'),
        ('RESERVADO', 'Reservado'),
        ('NO_DISPONIBLE', 'No Disponible')
    ]

    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='libros')
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')
    descripcion = models.TextField(default='Sin descripción')
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True)
    imagen_url = models.URLField(
        max_length=500,
        default='https://media.istockphoto.com/id/1415203156/es/vector/página-de-error-icono-vectorial-de-página-no-encontrada-en-el-diseño-de-estilo-de-línea.jpg?s=612x612&w=0&k=20&c=nss_aWPtTb0hpc4oiGfFs_PGfihrNwVX06wxkWVkBfQ=',
        null=True,
        blank=True
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['titulo']

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"