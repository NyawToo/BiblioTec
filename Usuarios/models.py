from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class Usuario(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('BIBLIOTECARIO', 'Bibliotecario'),
        ('USUARIO', 'Usuario Regular')
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USUARIO',
        verbose_name='Rol'
    )
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    notificacion_prestamo = models.BooleanField(default=True, help_text='Recibir notificaciones cuando tomes prestado un libro')
    notificacion_vencimiento = models.BooleanField(default=True, help_text='Recibir notificaciones próximos a vencer')
    notificacion_devolucion = models.BooleanField(default=True, help_text='Recibir notificaciones cuando devuelvas un libro')
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        permissions = [
            ('can_manage_books', 'Puede gestionar libros'),
            ('can_manage_users', 'Puede gestionar usuarios'),
            ('can_view_statistics', 'Puede ver estadísticas')
        ]

    def save(self, *args, **kwargs):
        # Guardar el usuario primero para mantener la lógica predeterminada de Django
        super().save(*args, **kwargs)
        
        # No modificar los permisos si es superusuario
        if self.is_superuser:
            return
            
        # Configurar permisos basados en el rol para usuarios no superusuarios
        if self.role == 'BIBLIOTECARIO':
            self.is_staff = True
            bibliotecario_group, _ = Group.objects.get_or_create(name='Bibliotecarios')
            self.groups.add(bibliotecario_group)
            # Asignar permisos específicos para bibliotecarios
            biblioteca_perms = Permission.objects.filter(
                codename__in=['can_manage_books', 'can_view_statistics']
            )
            self.user_permissions.add(*biblioteca_perms)
        else:
            self.is_staff = False
            usuario_group, _ = Group.objects.get_or_create(name='Usuarios')
            self.groups.add(usuario_group)
            
        # Guardar los cambios de permisos
        super().save(update_fields=['is_staff'])


    def get_notification_settings(self):
        return {
            'prestamo': self.notificacion_prestamo,
            'vencimiento': self.notificacion_vencimiento,
            'devolucion': self.notificacion_devolucion
        }

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Los modelos Autor, Libro y Prestamo se encuentran en la aplicación 'libros'
