from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date, timedelta
from .models import Prestamo

def enviar_notificacion_vencimiento(prestamo):
    """Envía una notificación por email sobre un préstamo próximo a vencer o vencido"""
    dias_restantes = (prestamo.fecha_devolucion_esperada - date.today()).days
    
    # Prepara el contexto para la plantilla
    context = {
        'usuario_nombre': prestamo.usuario.get_full_name() or prestamo.usuario.username,
        'libro_titulo': prestamo.libro.titulo,
        'libro_autor': str(prestamo.libro.autor),
        'fecha_prestamo': prestamo.fecha_prestamo,
        'fecha_devolucion': prestamo.fecha_devolucion_esperada,
        'dias_restantes': dias_restantes if dias_restantes > 0 else None,
        'dias_vencidos': abs(dias_restantes) if dias_restantes <= 0 else None,
        'titulo': 'Recordatorio de Préstamo' if dias_restantes > 0 else 'Aviso de Préstamo Vencido'
    }
    
    # Renderiza el HTML y obtiene la versión de texto plano
    html_message = render_to_string('email/prestamo_notification.html', context)
    plain_message = strip_tags(html_message)
    
    asunto = f"{'Recordatorio: Préstamo próximo a vencer' if dias_restantes > 0 else 'Aviso: Préstamo vencido'} - {prestamo.libro.titulo}"
    
    try:
        send_mail(
            subject=asunto,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[prestamo.usuario.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f'Error al enviar notificación: {e}')
        return False

def verificar_prestamos_pendientes():
    """Verifica préstamos próximos a vencer y vencidos para enviar notificaciones"""
    # Préstamos que vencen en 3 días
    fecha_proxima = date.today() + timedelta(days=3)
    prestamos_proximos = Prestamo.objects.filter(
        devuelto=False,
        fecha_devolucion_esperada=fecha_proxima
    )
    
    # Préstamos vencidos
    prestamos_vencidos = Prestamo.objects.filter(
        devuelto=False,
        fecha_devolucion_esperada__lt=date.today()
    )
    
    # Enviar notificaciones
    for prestamo in prestamos_proximos:
        enviar_notificacion_vencimiento(prestamo)
    
    for prestamo in prestamos_vencidos:
        enviar_notificacion_vencimiento(prestamo)