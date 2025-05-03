from django.urls import path
from . import views

urlpatterns = [
    path('libro/<int:libro_id>/', views.ver_libro, name='ver_libro'),
    path('libro/crear/', views.crear_libro, name='crear_libro'),
    path('libro/<int:libro_id>/editar/', views.editar_libro, name='editar_libro'),
    path('libro/<int:libro_id>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
    path('', views.lista_libros, name='lista_libros'),
    path('buscar/', views.buscar_libros, name='buscar_libros'),
    path('prestamo/<int:libro_id>/', views.registrar_prestamo, name='registrar_prestamo'),
    path('devolver/<int:prestamo_id>/', views.devolver_libro, name='devolver_libro'),
    path('prestamos/', views.lista_prestamos_activos, name='lista_prestamos'),
    path('autores-ranking/', views.autores_mas_libros, name='autores_mas_libros'),
    path('registrar-bibliotecario/', views.registrar_bibliotecario, name='registrar_bibliotecario'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    # URLs para gestión de autores
    path('autores/', views.gestionar_autores, name='gestionar_autores'),
    path('autor/crear/', views.crear_autor, name='crear_autor'),
    path('autor/<int:autor_id>/editar/', views.editar_autor, name='editar_autor'),
    path('autor/<int:autor_id>/eliminar/', views.eliminar_autor, name='eliminar_autor'),
    # URLs para gestión de categorías
    path('categorias/', views.gestionar_categorias, name='gestionar_categorias'),
    path('categoria/crear/', views.crear_categoria, name='crear_categoria'),
    path('categoria/<int:categoria_id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categoria/<int:categoria_id>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
]