from django.shortcuts import render, redirect

#NEW
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegistroUsuarioForm, PerfilUsuarioForm

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

def registro(request):
    return render(request, "registro.html")

#NEW
def Registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.rol_id = 2 
            usuario.save()
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

 

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
    

def logout_usuario(request):
    logout(request)
    return redirect('login')

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