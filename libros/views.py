from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from datetime import date, timedelta
from .models import Libro, Autor, Categoria, Prestamo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

@login_required
def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros/lista_libros.html', {'libros': libros})

def buscar_libros(request):
    query = request.GET.get('q')
    categoria = request.GET.get('categoria')
    autor = request.GET.get('autor')
    
    libros = Libro.objects.all()
    if query:
        libros = libros.filter(titulo__icontains=query)
    if categoria:
        libros = libros.filter(categoria__id=categoria)
    if autor:
        libros = libros.filter(autor__id=autor)
    
    categorias = Categoria.objects.all()
    autores = Autor.objects.all()
    return render(request, 'libros/buscar_libros.html', {
        'libros': libros,
        'categorias': categorias,
        'autores': autores
    })

@login_required
def registrar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if not libro.disponible:
        messages.error(request, 'Este libro no está disponible actualmente.')
        return redirect('lista_libros')
    
    prestamo = Prestamo.objects.create(
        libro=libro,
        usuario=request.user,
        fecha_devolucion_esperada=date.today() + timedelta(days=14)
    )
    libro.disponible = False
    libro.save()
    messages.success(request, 'Préstamo registrado exitosamente.')
    return redirect('lista_prestamos')

@login_required
def lista_prestamos_activos(request):
    if request.user.is_staff:
        prestamos = Prestamo.objects.filter(devuelto=False)
    else:
        prestamos = Prestamo.objects.filter(usuario=request.user, devuelto=False)
    return render(request, 'libros/lista_prestamos.html', {'prestamos': prestamos})

@login_required
@user_passes_test(lambda u: u.is_staff)
def devolver_libro(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    prestamo.devuelto = True
    prestamo.fecha_devolucion_real = date.today()
    prestamo.save()
    prestamo.libro.disponible = True
    prestamo.libro.save()
    messages.success(request, 'Libro devuelto exitosamente.')
    return redirect('lista_prestamos')

def autores_mas_libros(request):
    autores = Autor.objects.annotate(num_libros=Count('libros')).order_by('-num_libros')
    return render(request, 'libros/autores_mas_libros.html', {'autores': autores})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada exitosamente para {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser)
def panel_admin(request):
    return render(request, 'libros/panel_admin.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('panel_admin')
            elif user.is_staff:
                return redirect('vista_bibliotecario')  # Cambia por la vista de bibliotecario
            else:
                return redirect('lista_libros')
        else:
            return render(request, 'registration/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'registration/login.html')


from .forms import BibliotecarioCreationForm
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def registrar_bibliotecario(request):
    if request.method == 'POST':
        form = BibliotecarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Bibliotecario registrado exitosamente!')
            return redirect('registrar_bibliotecario')
    else:
        form = BibliotecarioCreationForm()
    return render(request, 'libros/registrar_bibliotecario.html', {'form': form})