from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('buscar/', views.buscar_libros, name='buscar_libros'),
    path('prestamo/<int:libro_id>/', views.registrar_prestamo, name='registrar_prestamo'),
    path('devolver/<int:prestamo_id>/', views.devolver_libro, name='devolver_libro'),
    path('prestamos/', views.lista_prestamos_activos, name='lista_prestamos'),
    path('autores-ranking/', views.autores_mas_libros, name='autores_mas_libros'),
    path('registrar-bibliotecario/', views.registrar_bibliotecario, name='registrar_bibliotecario'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
]