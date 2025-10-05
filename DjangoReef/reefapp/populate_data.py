#NEW
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

from reefapp.models import Rol, CategoriaHabitacion, CaracteristicaHabitacion, Habitacion

def populate_initial_data():
    # Crear roles
    roles = ['Administrador', 'Recepcionista', 'Cliente']
    for rol_nombre in roles:
        Rol.objects.get_or_create(nombre=rol_nombre)
    
    # Crear categorías de habitación
    categorias = [
        {'nombre': 'Turista', 'descripcion': 'Habitaciones económicas con comodidades básicas'},
        {'nombre': 'Premium', 'descripcion': 'Habitaciones de lujo con amenities exclusivas'},
    ]
    
    for cat_data in categorias:
        CategoriaHabitacion.objects.get_or_create(**cat_data)
    
    # Crear características
    caracteristicas = [
        {'nombre': 'WiFi Gratuito', 'icono': 'wifi'},
        {'nombre': 'TV Cable', 'icono': 'tv'},
        {'nombre': 'Aire Acondicionado', 'icono': 'snowflake'},
        {'nombre': 'Minibar', 'icono': 'glass'},
        {'nombre': 'Jacuzzi', 'icono': 'hot-tub'},
        {'nombre': 'Vista al Mar', 'icono': 'mountain'},
    ]
    
    for carac_data in caracteristicas:
        CaracteristicaHabitacion.objects.get_or_create(**carac_data)
    
    print("Datos iniciales creados exitosamente!")

if __name__ == '__main__':
    populate_initial_data()