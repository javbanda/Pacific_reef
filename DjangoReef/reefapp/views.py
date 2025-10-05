from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.utils import timezone
from .models import Usuario, Habitacion, Reserva, Rol, CategoriaHabitacion
from .forms import RegistroUsuarioForm, LoginForm, ReservaForm
import json
from decimal import Decimal
from datetime import datetime, date


# General
def inicio(request):
    return render(request, 'home.html')
def home(request):
    return render(request, "home.html")
def acerca(request):
    return render(request, "acerca.html")
def habitaciones(request):
    return render(request, "habitaciones.html")
def spa(request):
    return render(request, "spa.html")
def restaurante(request):
    return render(request, "restaurante.html")
def proximamente(request):
    return render(request, "proximamente.html")

def reserva(request):
    return render(request, "reserva.html")

#NEW

#Vista registro
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'registro.html', {'form': form})
 
#Vista login
def login_usuario(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        user = authenticate(request, correo=correo, password=password)
        if user is not None:
            login(request, user)
            # Redireccionar según el rol
            if user.rol.nombre == "Administrador":
                return redirect('perfilAdmin') 
            else:
                return redirect('perfil')
        else:
            messages.error(request, "Correo o contraseña inválidos.")
            return redirect('home')
    else:
        return redirect('home')
    
#Vista logout
@login_required
def logout_usuario(request):
    logout(request)
    return redirect('login')

#Vista recuperar contraseña
def recuperar_contrasena(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        Usuario = get_user_model()
        try:
            Usuario = Usuario.objects.get(correo=correo)
            messages.success(request, f'Se ha enviado un enlace de recuperación a {correo}.')
        except Usuario.DoesNotExist:
            messages.error(request, 'El correo ingresado no está registrado.')
        return redirect('home')
    
#Vista habitaciones
def habitaciones_view(request):
    habitaciones = Habitacion.objects.filter(estado='disponible')
    return render(request, 'habitaciones.html', {'habitaciones': habitaciones})

# Vista de reserva
@login_required
def reserva_view(request):
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    adultos = request.GET.get('adults', '1')  
    niños = request.GET.get('children', '0')  
    rooms = request.GET.get('rooms', '1')
    
    habitaciones = Habitacion.objects.filter(estado='disponible')
    
    context = {
        'habitaciones_json': json.dumps([{
            'id': h.id_habitacion,
            'name': f"Habitación {h.numero} - {h.get_tipo_display()}",
            'category': h.categoria.nombre,
            'type': h.tipo,
            'price': float(h.precio_base),
            'capacity': f"{h.capacidad_adultos} adultos",
            'description': h.descripcion,
            'available': True
        } for h in habitaciones]),
        'checkin': checkin,
        'checkout': checkout,
        'adultos': adultos,  
        'niños': niños,      
        'rooms': rooms
    }
    
    return render(request, 'reserva.html', context)

# API para habitaciones disponibles
def api_habitaciones_disponibles(request):
    fecha_inicio = request.GET.get('checkin')
    fecha_fin = request.GET.get('checkout')
    adultos = int(request.GET.get('adultos', 1))
    ninos = int(request.GET.get('ninos', 0))
    
    try:
        if fecha_inicio and fecha_fin:
            fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y').date()
            fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y').date()
            
            habitaciones_reservadas = Reserva.objects.filter(
                fecha_checkin__lt=fecha_fin,
                fecha_checkout__gt=fecha_inicio,
                estado__in=['confirmada', 'activa', 'pendiente']
            ).values_list('habitacion__id_habitacion', flat=True) 
            
            habitaciones = Habitacion.objects.filter(
                estado='disponible',
                capacidad_adultos__gte=adultos
            ).exclude(id_habitacion__in=habitaciones_reservadas)
        else:
            habitaciones = Habitacion.objects.filter(
                estado='disponible',
                capacidad_adultos__gte=adultos
            )
        
        data = []
        for hab in habitaciones:
            data.append({
                'id': hab.id_habitacion,
                'numero': hab.numero,
                'categoria': hab.categoria.nombre,
                'tipo': hab.tipo,
                'precio': float(hab.precio_base),
                'capacidad': f"{hab.capacidad_adultos} adultos + {hab.capacidad_ninos} niños",
                'descripcion': hab.descripcion,
            })
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        print(f"Error en API: {e}")  #Debugging
        return JsonResponse({'error': str(e)}, status=400)

# Vista crear reserva
@login_required
def crear_reserva_view(request, habitacion_id):
    try:
        habitacion = Habitacion.objects.get(id_habitacion=habitacion_id)
        
        checkin_str = request.GET.get('checkin')
        checkout_str = request.GET.get('checkout')
        
        if request.method == 'POST':
            form = ReservaForm(request.POST)
            if form.is_valid():
                reserva = form.save(commit=False)
                reserva.cliente = request.user
                reserva.habitacion = habitacion
                
                codigo = f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}"
                reserva.codigo_reserva = codigo
                
                reserva.save()
                
                return redirect('confirmacion_reserva', reserva_id=reserva.pk)
                
        else:
            initial_data = {}
            if checkin_str and '-' in checkin_str:
                try:
                    day, month, year = checkin_str.split('-')
                    checkin_str = f"{year}-{month}-{day}"
                except:
                    pass
            
            if checkout_str and '-' in checkout_str:
                try:
                    day, month, year = checkout_str.split('-')
                    checkout_str = f"{year}-{month}-{day}"
                except:
                    pass
            
            form = ReservaForm(initial=initial_data)
        
        precios = {}
        if checkin_str and checkout_str:
            try:
                fecha_inicio = datetime.strptime(checkin_str, '%d-%m-%Y').date()
                fecha_fin = datetime.strptime(checkout_str, '%d-%m-%Y').date()
                dias = (fecha_fin - fecha_inicio).days
                
                precios = {
                    'dias': dias,
                    'precio_noche': habitacion.precio_base,
                    'total_estadia': dias * habitacion.precio_base,
                    'pago_reserva': (dias * habitacion.precio_base * Decimal('0.3')) + (dias * habitacion.precio_base * Decimal('0.19')),
                    'saldo_pendiente': dias * habitacion.precio_base * Decimal('0.7'),
                }
            except ValueError:
                precios = {}
        
        context = {
            'habitacion': habitacion,
            'form': form,
            'precios': precios,
        }
        return render(request, 'crear_reserva.html', context)
        
    except Habitacion.DoesNotExist:
        return render(request, 'error.html', {'message': 'Habitación no encontrada'})

#Vista perfil cliente
@login_required
def perfil(request):
    """Vista del perfil del usuario"""
    try:
        reservas = Reserva.objects.filter(cliente=request.user).order_by('-fecha_reserva')
    except:
        reservas = []
    
    context = {
        'reservas': reservas,
        'usuario': request.user
    }
    return render(request, 'perfil.html', context)

#Vista perfil admin
@login_required
def perfilAdmin(request):
    """Vista del perfil de administrador"""
    return render(request, 'perfilAdmin.html', {'usuario': request.user})


def solo_admins(user):
    return user.is_staff or user.is_superuser

#Vista listar reservas (solo admin)
@login_required
@user_passes_test(solo_admins)
def listar_reservas(request):
    """Listar todas las reservas"""
    reservas = Reserva.objects.select_related('cliente', 'habitacion').all().order_by('-fecha_checkin')
    
    return render(request, 'listar_reservas.html', {'reservas': reservas})

#Vista eliminar reserva (solo admin)
@login_required
@user_passes_test(solo_admins)
def eliminar_reserva(request, reserva_id):
    """Eliminar una reserva específica"""
    try:
        reserva = get_object_or_404(Reserva, pk=reserva_id)
        
        if request.method == 'POST':
            codigo_reserva = reserva.codigo_reserva
            habitacion_numero = reserva.habitacion.numero
            
            reserva.delete()
            
            messages.success(request, f'Reserva {codigo_reserva} para habitación {habitacion_numero} eliminada correctamente.')
            return redirect('listar_reservas')
        
        return redirect('listar_reservas')
        
    except Exception as e:
        messages.error(request, f'Error al eliminar la reserva: {str(e)}')
        return redirect('listar_reservas')

#Vista confirmación de reserva
@login_required
def confirmacion_reserva(request, reserva_id):
    """Vista para mostrar la confirmación de reserva"""
    try:
        reserva = Reserva.objects.get(pk=reserva_id, cliente=request.user)
        
        dias_estadia = (reserva.fecha_checkout - reserva.fecha_checkin).days
        total_estadia = reserva.habitacion.precio_base * dias_estadia
        pago_reserva = total_estadia * Decimal('0.3')
        saldo_pendiente = total_estadia * Decimal('0.7')
        
        context = {
            'reserva': reserva,
            'dias_estadia': dias_estadia,
            'total_estadia': total_estadia,
            'pago_reserva': pago_reserva,
            'saldo_pendiente': saldo_pendiente,
        }
        
        return render(request, 'confirmacion_reserva.html', context)
        
    except Reserva.DoesNotExist:
        return render(request, 'error.html', {'message': 'Reserva no encontrada'})