-- Creación de la base de datos
CREATE DATABASE PacificReef;
USE PacificReef;

-- Tabla Usuario
CREATE TABLE Usuario (
    id_usuario INT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    telefono VARCHAR(20)
);

-- Tabla Roles
CREATE TABLE Roles (
    id_rol INT PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL
);

-- Tabla Rol_usuario (relación N:M entre Usuario y Roles)
CREATE TABLE Rol_usuario (
    user_rol INT PRIMARY KEY,
    id_rol INT,
    id_usuario INT,
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Tabla Hotel
CREATE TABLE Hotel (
    id_hotel INT PRIMARY KEY,
    direccion VARCHAR(150),
    ciudad VARCHAR(100),
    pais VARCHAR(100),
    zona_horaria VARCHAR(50)
);

-- Tabla Categoría de habitación
CREATE TABLE Categoria_habitacion (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(50),
    descripcion TEXT
);

-- Tabla Habitación
CREATE TABLE Habitacion (
    id_room INT PRIMARY KEY,
    numero VARCHAR(20),
    piso VARCHAR(10),
    capacidad VARCHAR(10),
    nota VARCHAR(100),
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES Categoria_habitacion(id_categoria)
);

-- Tabla Precios
CREATE TABLE Precios (
    id_price INT PRIMARY KEY,
    efectivo_desde DATE,
    efectivo_hasta DATE,
    moneda CHAR(3),
    tarifa_diaria DECIMAL(10,2),
    id_categoria INT,
    id_room INT,
    FOREIGN KEY (id_categoria) REFERENCES Categoria_habitacion(id_categoria),
    FOREIGN KEY (id_room) REFERENCES Habitacion(id_room)
);

-- Tabla Reservas
CREATE TABLE Reservas (
    id_reservacion INT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    noches INT,
    qr_token DECIMAL(18,0),
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_room INT,
    id_usuario INT,
    FOREIGN KEY (id_room) REFERENCES Habitacion(id_room),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Tabla Métodos de pago
CREATE TABLE Metodos_pago (
    id_metodo INT PRIMARY KEY,
    method_name VARCHAR(50),
    method_code VARCHAR(50),
    id_pago INT
);

-- Tabla Pagos
CREATE TABLE Pagos (
    id_pago INT PRIMARY KEY,
    total DECIMAL(10,2),
    status VARCHAR(20),
    paid_at DATETIME,
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_reservacion INT,
    id_metodo INT,
    FOREIGN KEY (id_reservacion) REFERENCES Reservas(id_reservacion),
    FOREIGN KEY (id_metodo) REFERENCES Metodos_pago(id_metodo)
);

-- Ajuste de relación Métodos de pago con Pagos (1:N)
ALTER TABLE Metodos_pago
ADD CONSTRAINT fk_metodo_pago FOREIGN KEY (id_pago) REFERENCES Pagos(id_pago);
