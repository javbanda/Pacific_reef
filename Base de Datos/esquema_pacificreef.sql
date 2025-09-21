-- Creacion de la base de datos
-- BD
DROP DATABASE IF EXISTS PacificReef;
CREATE DATABASE PacificReef CHARACTER SET = 'utf8mb4' COLLATE = 'utf8mb4_unicode_ci';
USE PacificReef;

-- Usuarios
CREATE TABLE Usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  nombre VARCHAR(80),
  apellido VARCHAR(80),
  telefono VARCHAR(30),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Roles y relación simple
CREATE TABLE Roles (
  id_rol INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL
);

CREATE TABLE Rol_usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_rol INT NOT NULL,
  id_usuario INT NOT NULL,
  FOREIGN KEY (id_rol) REFERENCES Roles(id_rol),
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Categoria y Habitacion
CREATE TABLE Categoria_habitacion (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(80),
  capacidad INT
);

CREATE TABLE Habitacion (
  id_room INT AUTO_INCREMENT PRIMARY KEY,
  numero VARCHAR(20),
  id_categoria INT,
  estado VARCHAR(30) DEFAULT 'DISPONIBLE',
  FOREIGN KEY (id_categoria) REFERENCES Categoria_habitacion(id_categoria)
);

-- Reservas (1 reserva = 1 habitacion para simplificar)
CREATE TABLE Reservas (
  id_reservacion INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(100) NOT NULL UNIQUE,
  check_in DATE NOT NULL,
  check_out DATE NOT NULL,
  noches INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  id_room INT NOT NULL,
  id_usuario INT NOT NULL,
  estado VARCHAR(30) DEFAULT 'PENDIENTE',
  monto_total DECIMAL(10,2) DEFAULT 0,
  FOREIGN KEY (id_room) REFERENCES Habitacion(id_room),
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Metodos de pago y Pagos (simple)
CREATE TABLE Metodos_pago (
  id_metodo INT AUTO_INCREMENT PRIMARY KEY,
  method_name VARCHAR(80)
);

CREATE TABLE Pagos (
  id_pago INT AUTO_INCREMENT PRIMARY KEY,
  id_reservacion INT NOT NULL,
  id_metodo INT,
  monto DECIMAL(10,2),
  status VARCHAR(30) DEFAULT 'PENDIENTE',
  paid_at DATETIME NULL,
  FOREIGN KEY (id_reservacion) REFERENCES Reservas(id_reservacion),
  FOREIGN KEY (id_metodo) REFERENCES Metodos_pago(id_metodo)
);