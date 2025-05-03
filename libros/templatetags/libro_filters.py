from django import template
from datetime import timedelta, datetime

register = template.Library()

@register.filter(name='timedelta')
def timedelta_filter(value):
    """Convierte una cadena de texto en un objeto timedelta.
    Ejemplo: '3 días' -> timedelta(days=3)
    """
    try:
        amount, unit = value.split()
        amount = int(amount)
        
        if unit in ['day', 'days', 'día', 'días']:
            return timedelta(days=amount)
        elif unit in ['hour', 'hours', 'hora', 'horas']:
            return timedelta(hours=amount)
        elif unit in ['minute', 'minutes', 'minuto', 'minutos']:
            return timedelta(minutes=amount)
        else:
            return timedelta()
    except (ValueError, AttributeError):
        return timedelta()

@register.filter(name='timeuntil')
def timeuntil_filter(value, arg=None):
    """Calcula la diferencia de tiempo entre dos fechas.
    Si arg es None, se usa la fecha actual.
    Retorna un objeto timedelta para facilitar comparaciones en la plantilla.
    """
    if not value:
        return timedelta()
    
    if arg is None:
        arg = datetime.now()
    
    if isinstance(value, datetime):
        return value - arg
    return timedelta()