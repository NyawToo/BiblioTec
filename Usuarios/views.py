from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from .models import Usuario
from libros.models import Libro, Autor, Prestamo
from .forms import UsuarioForm, NotificacionesForm

def home(request):
    if request.user.is_authenticated:
        libros = Libro.objects.all()
        prestamos_activos = Prestamo.objects.filter(usuario=request.user, devuelto=False)
        return render(request, 'usuarios/dashboard.html', {
            'libros': libros,
            'prestamos_activos': prestamos_activos
        })
    else:
        libros_recientes = Libro.objects.filter(estado='DISPONIBLE').order_by('-fecha_creacion')[:5]
        return render(request, 'home.html', {'libros_recientes': libros_recientes})

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                if user.role == 'BIBLIOTECARIO':
                    if form.cleaned_data['codigo_autenticacion'] != 'NYAW123456789':
                        return render(request, 'registration/codigo_invalido.html')
                user.save()
                login(request, user)
                messages.success(request, '¡Registro exitoso!')
                return redirect('home')
            except forms.ValidationError as e:
                messages.error(request, str(e))
    else:
        form = UsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.role == 'BIBLIOTECARIO':
        # Vista para bibliotecarios
        todos_libros = Libro.objects.all().order_by('titulo')
        prestamos_activos = Prestamo.objects.filter(devuelto=False).order_by('fecha_devolucion_esperada')
        return render(request, 'usuarios/dashboard_bibliotecario.html', {
            'todos_libros': todos_libros,
            'prestamos_activos': prestamos_activos
        })
    else:
        # Vista para usuarios regulares
        libros = Libro.objects.all()
        prestamos_activos = Prestamo.objects.filter(usuario=request.user, devuelto=False)
        return render(request, 'usuarios/dashboard.html', {
            'libros': libros,
            'prestamos_activos': prestamos_activos
        })

@login_required
def buscar_libros(request):
    query = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')
    libros = Libro.objects.all()
    
    if query:
        libros = libros.filter(
            Q(titulo__icontains=query) |
            Q(autor__nombre__icontains=query) |
            Q(autor__apellido__icontains=query)
        )
    
    if categoria:
        libros = libros.filter(categoria=categoria)
        
    return render(request, 'buscar_libros.html', {
        'libros': libros,
        'query': query,
        'categoria': categoria,
        'categorias': Libro.CATEGORIAS
    })

@login_required
def prestar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if not libro.disponible:
        messages.error(request, 'Este libro no está disponible actualmente.')
        return redirect('home')
    
    fecha_devolucion = timezone.now() + timedelta(days=14)  # 2 semanas de préstamo
    Prestamo.objects.create(
        libro=libro,
        usuario=request.user,
        fecha_devolucion_esperada=fecha_devolucion
    )
    libro.disponible = False
    libro.save()
    
    messages.success(request, f'Has tomado prestado el libro {libro.titulo}')
    return redirect('home')

@login_required
def devolver_libro(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id, usuario=request.user)
    if not prestamo.devuelto:
        prestamo.devuelto = True
        prestamo.fecha_devolucion_real = timezone.now()
        prestamo.save()
        prestamo.libro.disponible = True
        prestamo.libro.save()
        messages.success(request, f'Has devuelto el libro {prestamo.libro.titulo}')
    return redirect('home')

@login_required
def estadisticas(request):
    autores_top = Autor.objects.annotate(
        num_libros=Count('libros')
    ).order_by('-num_libros')
    
    prestamos_vencidos = Prestamo.objects.filter(
        devuelto=False,
        fecha_devolucion_esperada__lt=timezone.now()
    )
    
    return render(request, 'estadisticas.html', {
        'autores_top': autores_top,
        'prestamos_vencidos': prestamos_vencidos
    })

@login_required
def configurar_notificaciones(request):
    if request.method == 'POST':
        form = NotificacionesForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tus preferencias de notificaciones han sido actualizadas.')
            return redirect('configurar_notificaciones')
    else:
        form = NotificacionesForm(instance=request.user)
    
    return render(request, 'usuarios/configuracion_notificaciones.html', {'form': form})
