# 🏨 Hotel Pacific Reef — Sistema de Reservas

Prototipo funcional para gestión de hospedaje: catálogo visual, verificación de disponibilidad, cálculo de anticipo (30%), emisión de ticket con QR y administración por roles.

---

## 🚀 Características principales
- Consulta de disponibilidad por fechas.
- Catálogo de habitaciones con fotos y equipamiento.
- Reserva autogestionada y cálculo automático del **30% de anticipo**.
- Pagos en línea (mock o pasarela), ticket con **QR** enviado por correo.
- Multilenguaje **ES/EN**.
- Gestión de usuarios y roles (**CLIENTE / TURISTA / ADMINISTRADORES / EMPLEADOS**).

## 🗃️ Modelo de datos (resumen)

- **Usuarios** ↔ Roles

- **Hoteles** → Categorías → Habitaciones → Fotos

- **Habitaciones** ↔ Equipamiento

- **Reservas** → Pagos

## 📌 Contenido del repositorio
- **Diagramas UML mejorados**
  - Caso de uso
  - Actividad
  - Clases
  - Links en `Diagramas_Links.txt`
- **Pantallas Figma**
  - PDF con diseño de pantallas principales de Cliente y Administrador.
- **Base de datos**
  - `esquema_pacificreef.sql`: Script de creación del esquema de BD.
  - `datos_pacificreef.sql`: Datos de prueba con usuarios, habitaciones, reservas y pagos.
  - `datos2_pacificreef.sql`: Datos de prueba 2.
  - `crud_pacificreef.sql`: Script de prueba CRUD con SELECT antes/después.
  - `pacific_reef_bd`: Script completo con el esquema, datos de prueba y script CRUD
- **Capturas**
  - En Trello y Git: evidencias de ejecución de los scripts (SELECT antes/después, reservas creadas, etc.).
- **DOD**
  - Documento actualizado con valores de la semana 6.
 
## 🚀 Requerimientos
- MySQL 8.0 o superior
- Cliente SQL (Workbench, DBeaver, CLI)

## ⚙️ Ejecución
1. Crear la base de datos ejecutando: source esquema_pacificreef.sql;
2. Insertar datos de prueba: source datos_pacificreef.sql o datos2_pacificreef.sql;
3. Probar operaciones CRUD: source crud_pacificreef.sql;

---

  </div>
</body>
</html>
