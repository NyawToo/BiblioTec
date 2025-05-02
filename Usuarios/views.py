from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Usuario, Libro, Autor, Prestamo
from .forms import UsuarioForm

def home(request):
    libros_recientes = Libro.objects.filter(estado='DISPONIBLE').order_by('-fecha_adquisicion')[:5]
    return render(request, 'home.html', {'libros_recientes': libros_recientes})

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def home(request):
    libros = Libro.objects.all()
    prestamos_activos = Prestamo.objects.filter(usuario=request.user, devuelto=False)
    return render(request, 'home.html', {
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
