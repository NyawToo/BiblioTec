from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('buscar/', views.buscar_libros, name='buscar_libros'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('prestar/<int:libro_id>/', views.prestar_libro, name='prestar_libro'),
    path('devolver/<int:prestamo_id>/', views.devolver_libro, name='devolver_libro'),
]