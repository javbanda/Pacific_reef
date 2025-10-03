from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ROL Tabla
class Rol(models.Model):
    class Meta:
        db_table = 'MAIN_ROL'
    id_rol = models.AutoField(primary_key=True, db_column='ID_ROL')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')

    def __str__(self):
        return self.nombre


#Inicio Sesion Autenticacion
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es obligatorio')
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Aquí asignamos el rol de administrador
        from reefapp.models import Rol  
        rol_admin = Rol.objects.get(nombre='Administrador')
        extra_fields.setdefault('rol', rol_admin)

        return self.create_user(correo, password, **extra_fields)

#USUARIO
class Usuario(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'USUARIO'

    id_usuario = models.AutoField(primary_key=True, db_column='ID_USUARIO')
    nombre = models.CharField(max_length=100, db_column='NOMBRE', null=True)
    apellido = models.CharField(max_length=100, db_column='APELLIDO', null=True)
    rol = models.ForeignKey('Rol', on_delete=models.PROTECT, db_column='ID_ROL')
    correo = models.EmailField(unique=True, db_column='CORREO')
    direccion = models.CharField(max_length=255, db_column='DIRECCION', null=True, blank=True)
    telefono = models.CharField(max_length=20, db_column='TELEFONO', null=True, blank=True)
    password = models.CharField(max_length=255, db_column='PASSWORD')
    is_active = models.BooleanField(default=True, db_column='ACTIVO')
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']
    
    objects = UsuarioManager()

    def __str__(self):
        return self.correo