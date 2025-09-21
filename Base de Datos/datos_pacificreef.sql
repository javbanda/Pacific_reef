-- Datos
USE PacificReef;

INSERT INTO Roles (code,name) VALUES ('ADMIN','Administrador'),('CLIENT','Cliente');

INSERT INTO Usuario (email,password_hash,nombre,apellido,telefono)
VALUES ('cliente@ejemplo.com','hash-demo','María','Perez','+56912345678');

INSERT INTO Categoria_habitacion (nombre,capacidad) VALUES ('Doble',2),('Suite',4);

INSERT INTO Habitacion (numero,id_categoria,estado) VALUES ('101',1,'DISPONIBLE'),('102',2,'DISPONIBLE');

INSERT INTO Metodos_pago (method_name) VALUES ('Tarjeta'),('Transferencia');

-- Reserva ejemplo R-0001
INSERT INTO Reservas (codigo,check_in,check_out,noches,id_room,id_usuario,estado,monto_total)
VALUES ('R-0001','2025-07-10','2025-07-12',2,1,1,'PENDIENTE',100000);

-- Pago ejemplo
INSERT INTO Pagos (id_reservacion,id_metodo,monto,status,paid_at)
VALUES (1,1,100000,'EXITOSO','2025-06-01 10:00:00');