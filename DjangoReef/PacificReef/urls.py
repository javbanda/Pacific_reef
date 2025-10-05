"""
URL configuration for PacificReef project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from reefapp import views   

urlpatterns = [
    # Páginas principales
    path('', views.inicio),
    path('home/', views.home, name='home'),
    path('acerca/', views.acerca, name='acerca'),
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('spa/', views.spa, name='spa'),
    path('restaurante/', views.restaurante, name='restaurante'),
    path('proximamente/', views.proximamente, name='proximamente'),
    path('reserva/', views.reserva_view, name='reserva'),
    path('admin/', admin.site.urls),

    path('login/', views.login_usuario, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_usuario, name='logout'),
    path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),  

    path('perfil/', views.perfil, name='perfil'),
    path('perfil/admin/', views.perfilAdmin, name='perfilAdmin'),   

    path('api/habitaciones-disponibles/', views.api_habitaciones_disponibles, name='api_habitaciones_disponibles'),
    path('reservar/<int:habitacion_id>/', views.crear_reserva_view, name='crear_reserva'),
    path('reserva/confirmacion/<int:reserva_id>/', views.confirmacion_reserva, name='confirmacion_reserva'),
    path('listar_reservas/', views.listar_reservas, name='listar_reservas'),
    path('reservas/eliminar/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'), 

]
