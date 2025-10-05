from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#NEW
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

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
        # Asignar rol de Administrador al superusuario
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


#NEW
# CATEGORIA_HABITACION
class CategoriaHabitacion(models.Model):
    class Meta:
        db_table = 'CATEGORIA_HABITACION'

    id_categoria = models.AutoField(primary_key=True, db_column='ID_CATEGORIA')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    descripcion = models.TextField(db_column='DESCRIPCION')

    def __str__(self):
        return self.nombre

# CARACTERISTICA_HABITACION
class CaracteristicaHabitacion(models.Model):
    class Meta:
        db_table = 'CARACTERISTICA_HABITACION'
        
    id_caracteristica = models.AutoField(primary_key=True, db_column='ID_CARACTERISTICA')
    nombre = models.CharField(max_length=100, db_column='NOMBRE')
    icono = models.CharField(max_length=50, blank=True, db_column='ICONO')

    def __str__(self):
        return self.nombre

# HABITACION
class Habitacion(models.Model):
    class Meta:
        db_table = 'HABITACION'
    ESTADOS = [('disponible', 'Disponible'), ('ocupada', 'Ocupada'), 
               ('mantenimiento', 'Mantenimiento'), ('reservada', 'Reservada')]
    TIPOS = [('individual', 'Individual'), ('doble', 'Doble'), 
             ('familiar', 'Familiar'), ('suiteD', 'SuiteD'), ('suiteF', 'SuiteF')]
    
    id_habitacion = models.AutoField(primary_key=True, db_column='ID_HABITACION')
    numero = models.CharField(max_length=10, unique=True, db_column='NUMERO')
    piso = models.IntegerField(db_column='PISO')
    categoria = models.ForeignKey(CategoriaHabitacion, on_delete=models.PROTECT, db_column='ID_CATEGORIA')
    tipo = models.CharField(max_length=20, choices=TIPOS, db_column='TIPO')
    capacidad_adultos = models.IntegerField(default=1, db_column='CAPACIDAD_ADULTOS')
    capacidad_ninos = models.IntegerField(default=0, db_column='CAPACIDAD_NINOS')
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, db_column='PRECIO_BASE')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible', db_column='ESTADO')
    descripcion = models.TextField(db_column='DESCRIPCION')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    updated_at = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    def __str__(self):
        return f"Habitación {self.numero} - {self.get_tipo_display()}"

# HABITACION_CARACTERISTICA
class HabitacionCaracteristica(models.Model):
    class Meta:
        db_table = 'HABITACION_CARACTERISTICA'

    id = models.AutoField(primary_key=True, db_column='ID')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, db_column='ID_HABITACION')
    caracteristica = models.ForeignKey(CaracteristicaHabitacion, on_delete=models.CASCADE, db_column='ID_CARACTERISTICA')

# IMAGEN_HABITACION
class ImagenHabitacion(models.Model):
    class Meta:
        db_table = 'IMAGEN_HABITACION'
    id_imagen = models.AutoField(primary_key=True, db_column='ID_IMAGEN')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, db_column='ID_HABITACION')
    imagen = models.ImageField(upload_to='habitaciones/', db_column='IMAGEN')
    es_principal = models.BooleanField(default=False, db_column='ES_PRINCIPAL')

# RESERVA
class Reserva(models.Model):
    class Meta:
        db_table = 'RESERVA'
    ESTADOS_RESERVA = [('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), 
                       ('activa', 'Activa'), ('completada', 'Completada'), ('cancelada', 'Cancelada')]
    
    id_reserva = models.AutoField(primary_key=True, db_column='ID_RESERVA')
    codigo_reserva = models.CharField(max_length=15, unique=True, db_column='CODIGO_RESERVA')
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='ID_CLIENTE')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT, db_column='ID_HABITACION')
    fecha_checkin = models.DateField(db_column='FECHA_CHECKIN')
    fecha_checkout = models.DateField(db_column='FECHA_CHECKOUT')
    fecha_reserva = models.DateTimeField(auto_now_add=True, db_column='FECHA_RESERVA')
    adultos = models.IntegerField(db_column='ADULTOS')
    ninos = models.IntegerField(default=0, db_column='NINOS')
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default='pendiente', db_column='ESTADO')
    total_estadia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pago_reserva = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 30%
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return f"Reserva {self.codigo_reserva}"

    @property
    def impuestos(self):
        """Calcula impuestos (19% IVA)"""
        return self.total_estadia * Decimal('0.19')
        
    def save(self, *args, **kwargs):
        if self.fecha_checkin and self.fecha_checkout and self.habitacion:
            dias = (self.fecha_checkout - self.fecha_checkin).days
            self.total_estadia = dias * self.habitacion.precio_base
            self.pago_reserva = (self.total_estadia * Decimal('0.3')) + self.impuestos
            self.saldo_pendiente = self.total_estadia - self.pago_reserva
            
        super().save(*args, **kwargs)
    
    @property
    def dias_estadia(self):
        """Calcula los días de estadía"""
        if self.fecha_checkin and self.fecha_checkout:
            return (self.fecha_checkout - self.fecha_checkin).days
        return 0
       
# PAGO
class Pago(models.Model):
    class Meta:
        db_table = 'PAGO'
        
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    ]
    
    METODOS_PAGO = [
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('transferencia', 'Transferencia Bancaria'),
        ('paypal', 'PayPal'),
    ]
    
    id_pago = models.AutoField(primary_key=True, db_column='ID_PAGO')
    reserva = models.ForeignKey(
        Reserva, 
        on_delete=models.CASCADE, 
        related_name='pagos',
        db_column='ID_RESERVA'
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2, db_column='MONTO')
    metodo_pago = models.CharField(
        max_length=20, 
        choices=METODOS_PAGO,
        db_column='METODO_PAGO'
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS_PAGO, 
        default='pendiente',
        db_column='ESTADO'
    )
    fecha_pago = models.DateTimeField(null=True, blank=True, db_column='FECHA_PAGO')
    transaccion_id = models.CharField(
        max_length=100, 
        blank=True, 
        db_column='TRANSACCION_ID'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return f"Pago {self.id_pago} - {self.reserva.codigo_reserva}"    
