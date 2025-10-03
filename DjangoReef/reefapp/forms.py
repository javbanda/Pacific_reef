#NEW
import re
from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'direccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"



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


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'direccion', 'telefono']


  