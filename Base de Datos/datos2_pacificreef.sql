USE PacificReef;

-- Roles
INSERT INTO Roles (code,name) VALUES 
('ADMIN','Administrador'),
('CLIENT','Cliente');

-- Usuarios
INSERT INTO Usuario (email,password_hash,nombre,apellido,telefono)
VALUES 
('admin@pacificreef.com','hash-admin','Ana','Gómez','+56911111111'),
('cliente1@pacificreef.com','hash-client1','Luis','Martínez','+56922222222'),
('cliente2@pacificreef.com','hash-client2','Sofía','Rojas','+56933333333');

-- Asignación de roles
INSERT INTO Rol_usuario (id_rol,id_usuario) VALUES (1,1),(2,2),(2,3);

-- Categorías de habitación
INSERT INTO Categoria_habitacion (nombre,capacidad) VALUES 
('Individual',1),
('Doble',2),
('Suite Familiar',4);

-- Habitaciones
INSERT INTO Habitacion (numero,id_categoria,estado) VALUES
('101',1,'DISPONIBLE'),
('102',2,'DISPONIBLE'),
('201',2,'OCUPADA'),
('301',3,'DISPONIBLE');

-- Métodos de pago
INSERT INTO Metodos_pago (method_name) VALUES ('Tarjeta'),('Transferencia');

-- Reservas
INSERT INTO Reservas (codigo,check_in,check_out,noches,id_room,id_usuario,estado,monto_total)
VALUES 
('R-0001','2025-07-10','2025-07-12',2,1,2,'CONFIRMADA',80000),
('R-0002','2025-08-01','2025-08-04',3,4,3,'PENDIENTE',200000);

-- Pagos
INSERT INTO Pagos (id_reservacion,id_metodo,monto,status,paid_at)
VALUES 
(1,1,80000,'EXITOSO','2025-07-01 09:00:00');
