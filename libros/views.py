from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date, timedelta
from .models import Libro, Autor, Categoria, Prestamo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .notifications import enviar_notificacion_vencimiento
from django.db.models.functions import Coalesce
from .forms import LibroForm, AutorForm, CategoriaForm

def home(request):
    return render(request, 'home.html')

@login_required
def lista_libros(request):
    libros = Libro.objects.all().order_by('-fecha_creacion')
    return render(request, 'libros/lista_libros.html', {'libros': libros})

@login_required
def ver_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    return render(request, 'libros/detalle_libro.html', {'libro': libro})

@login_required
@user_passes_test(lambda u: u.is_staff)
def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save()
            messages.success(request, 'Libro creado exitosamente.')
            return redirect('lista_libros')
    else:
        form = LibroForm()
    return render(request, 'libros/libro_form.html', {'form': form, 'action': 'Crear'})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            libro = form.save()
            messages.success(request, 'Libro actualizado exitosamente.')
            return redirect('lista_libros')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libros/libro_form.html', {'form': form, 'libro': libro, 'action': 'Editar'})

@login_required
def ver_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    return render(request, 'libros/detalle_libro.html', {'libro': libro})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado exitosamente.')
        return redirect('lista_libros')
    return render(request, 'libros/confirmar_eliminar.html', {'libro': libro})

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
@user_passes_test(lambda u: u.is_staff)
def gestionar_autores(request):
    autores = Autor.objects.all().order_by('apellido', 'nombre')
    form_autor = AutorForm()
    forms_edicion = {autor.id: AutorForm(instance=autor) for autor in autores}
    return render(request, 'libros/gestionar_autores.html', {
        'autores': autores,
        'form_autor': form_autor,
        'forms_edicion': forms_edicion
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def gestionar_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    form_categoria = CategoriaForm()
    forms_edicion = {}
    for categoria in categorias:
        forms_edicion[categoria.id] = CategoriaForm(instance=categoria)
    return render(request, 'libros/gestionar_categorias.html', {
        'categorias': categorias,
        'form_categoria': form_categoria,
        'forms_edicion': forms_edicion
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def crear_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            autor = form.save()
            messages.success(request, 'Autor creado exitosamente.')
            return redirect('gestionar_autores')
    else:
        form = AutorForm()
    return render(request, 'libros/autor_form.html', {'form': form, 'action': 'Crear'})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            autor = form.save()
            if form.changed_data:
                campos_modificados = [form.fields[campo].label for campo in form.changed_data]
                messages.success(
                    request,
                    f'Autor actualizado exitosamente. Campos modificados: {(", ").join(campos_modificados)}'
                )
                return redirect('gestionar_autores')
            else:
                messages.info(request, 'No se detectaron cambios en los datos del autor.')
                return redirect('gestionar_autores')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = AutorForm(instance=autor)
    
    context = {
        'form': form,
        'autor': autor,
        'action': 'Editar',
        'titulo': f'Editar autor: {autor.nombre} {autor.apellido}'
    }
    return render(request, 'libros/autor_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        autor.delete()
        messages.success(request, 'Autor eliminado exitosamente.')
        return redirect('gestionar_autores')
    return render(request, 'libros/confirmar_eliminar.html', {'autor': autor})

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'libros/lista_categorias.html', {'categorias': categorias})

@login_required
@user_passes_test(lambda u: u.is_staff)
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, 'La categoría se ha creado correctamente.')
            return redirect('gestionar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'libros/categoria_form.html', {'form': form, 'action': 'Crear'})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, 'La categoría se ha actualizado correctamente.')
            return redirect('gestionar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'libros/categoria_form.html', {'form': form, 'categoria': categoria, 'action': 'Editar'})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'La categoría se ha eliminado correctamente.')
        return redirect('gestionar_categorias')
    return render(request, 'libros/confirmar_eliminar.html', {'categoria': categoria})

@login_required
def registrar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if libro.estado != 'DISPONIBLE':
        messages.error(request, 'Este libro no está disponible actualmente.')
        return redirect('lista_libros')
    
    prestamo = Prestamo.objects.create(
        libro=libro,
        usuario=request.user,
        fecha_devolucion_esperada=date.today() + timedelta(days=14)
    )
    libro.estado = 'PRESTADO'
    libro.save()
    
    # Enviar notificación de confirmación
    enviar_notificacion_vencimiento(prestamo)
    messages.success(request, 'Préstamo registrado exitosamente.')
    return redirect('lista_prestamos')

from django.utils import timezone

@login_required
def lista_prestamos(request):
    # Filtrar préstamos según el rol del usuario
    if request.user.is_staff:
        # Los bibliotecarios ven todos los préstamos activos
        prestamos = Prestamo.objects.filter(devuelto=False).order_by('fecha_devolucion_esperada')
    else:
        # Los usuarios normales solo ven sus propios préstamos
        prestamos = Prestamo.objects.filter(usuario=request.user, devuelto=False).order_by('fecha_devolucion_esperada')
    
    # Calcular la fecha actual para comparaciones
    now = timezone.now().date()
    
    return render(request, 'libros/lista_prestamos.html', {
        'prestamos': prestamos,
        'now': now
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def lista_prestamos_activos(request):
    # This view is an alias to lista_prestamos for backward compatibility
    return lista_prestamos(request)

@login_required
@user_passes_test(lambda u: u.is_staff)
def devolver_libro(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    prestamo.devuelto = True
    prestamo.fecha_devolucion_real = date.today()
    prestamo.save()
    prestamo.libro.estado = 'DISPONIBLE'
    prestamo.libro.save()
    messages.success(request, 'Libro devuelto exitosamente.')
    return redirect('lista_prestamos')

@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    # Estadísticas generales
    total_libros = Libro.objects.count()
    libros_disponibles = Libro.objects.filter(estado='DISPONIBLE').count()
    libros_prestados = Libro.objects.filter(estado='PRESTADO').count()
    prestamos_activos = Prestamo.objects.filter(devuelto=False).count()
    prestamos_vencidos = Prestamo.objects.filter(
        devuelto=False,
        fecha_devolucion_esperada__lt=date.today()
    ).count()

    # Libros más prestados
    libros_mas_prestados = Libro.objects.annotate(
        total_prestamos=Count('prestamos')
    ).order_by('-total_prestamos')[:5]

    # Usuarios más activos
    usuarios_mas_activos = User.objects.annotate(
        total_prestamos=Count('prestamos'),
        prestamos_activos=Count('prestamos', filter=Q(prestamos__devuelto=False))
    ).order_by('-total_prestamos')[:5]

    # Datos para el gráfico de préstamos por categoría
    prestamos_categoria = Categoria.objects.annotate(
        total_prestamos=Count('libros__prestamos')
    ).order_by('-total_prestamos')

    categorias_labels = [cat.nombre for cat in prestamos_categoria]
    categorias_data = [cat.total_prestamos for cat in prestamos_categoria]

    context = {
        'total_libros': total_libros,
        'libros_disponibles': libros_disponibles,
        'prestamos_activos': prestamos_activos,
        'prestamos_vencidos': prestamos_vencidos,
        'libros_mas_prestados': libros_mas_prestados,
        'usuarios_mas_activos': usuarios_mas_activos,
        'categorias_labels': categorias_labels,
        'categorias_data': categorias_data,
    }

    return render(request, 'libros/dashboard.html', context)

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