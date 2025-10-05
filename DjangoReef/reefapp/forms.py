#NEW
import re
from django import forms
from .models import Usuario, Reserva, Habitacion
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'direccion', 'password1', 'password2']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus nombres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus apellidos'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su dirección'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"
        
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme su contraseña'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirmar = cleaned_data.get("password2")

        if password and confirmar and password != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if password:
            if len(password) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
            if not any(c.isdigit() for c in password):
                raise forms.ValidationError("Debe contener al menos un número.")
            if not any(c.isupper() for c in password):
                raise forms.ValidationError("Debe contener al menos una letra mayúscula.")
            if not any(c in "!@#$%^&*()_+-=[]{}|;':,.<>?/~`" for c in password):
                raise forms.ValidationError("Debe contener al menos un carácter especial.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Asignar automáticamente el rol de Cliente
        from .models import Rol
        try:
            rol_cliente = Rol.objects.get(nombre='Cliente')
            user.rol = rol_cliente
        except Rol.DoesNotExist:
            # Crear rol si no existe
            rol_cliente = Rol.objects.create(nombre='Cliente')
            user.rol = rol_cliente
        
        if commit:
            user.save()
        return user
      
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'direccion', 'telefono']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Correo Electrónico")

#NEW
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_checkin', 'fecha_checkout', 'adultos', 'ninos']