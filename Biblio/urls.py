"""
URL configuration for Biblio project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from libros import views as libros_views
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', libros_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('libros/', include('libros.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', libros_views.register, name='register'),
]
