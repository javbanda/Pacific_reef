-- Pruebas
USE PacificReef;

-- SELECT
SELECT * FROM Reservas WHERE codigo='R-0001';

-- CREATE
INSERT INTO Reservas (codigo,check_in,check_out,noches,id_room,id_usuario,estado,monto_total)
VALUES ('R-0002','2025-08-01','2025-08-04',3,2,1,'PENDIENTE',150000);
SELECT * FROM Reservas WHERE codigo='R-0002';

-- UPDATE
UPDATE Reservas SET estado='CONFIRMADA' WHERE codigo='R-0002';
SELECT codigo, estado FROM Reservas WHERE codigo='R-0002';

-- DELETE
DELETE FROM Reservas WHERE codigo='R-0002';
SELECT * FROM Reservas WHERE codigo='R-0002';