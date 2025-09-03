<!doctype html>

<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>README — Hotel Pacific Reef</title>
  <style>
    :root{--bg:#f7fafc;--card:#ffffff;--accent:#0ea5a4;--muted:#6b7280}
    body{font-family:Inter,system-ui,Segoe UI,Arial;margin:0;background:var(--bg);color:#111}
    .wrap{max-width:900px;margin:36px auto;padding:20px}
    .card{background:var(--card);border-radius:10px;box-shadow:0 6px 18px rgba(16,24,40,.06);padding:20px}
    h1{margin:0 0 8px;font-size:20px}
    p.lead{margin:0 0 16px;color:var(--muted)}
    ul{margin:8px 0 16px 20px}
    code{background:#f3f4f6;padding:2px 6px;border-radius:6px;font-family:monospace}
    .grid{display:grid;grid-template-columns:1fr 160px;gap:16px}
    .meta{font-size:13px;color:var(--muted)}
    .footer{margin-top:18px;font-size:13px;color:var(--muted)}
    a.btn{display:inline-block;padding:8px 12px;border-radius:8px;background:var(--accent);color:#fff;text-decoration:none}
    @media (max-width:640px){.grid{grid-template-columns:1fr} }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div class="grid">
        <div>
          <h1>Hotel Pacific Reef — Sistema de Reservas (README)</h1>
          <p class="lead">Prototipo funcional para reserva y gestión de hospedaje: catálogo visual, verificación de disponibilidad, cálculo de anticipo (30%), emisión de ticket con QR y administración por roles.</p>

```
      <h3>Características</h3>
      <ul>
        <li>Consulta de disponibilidad por rango de fechas.</li>
        <li>Catálogo de habitaciones con ≥3 fotos y equipamiento.</li>
        <li>Reserva autogestionada y cálculo automático del 30% de anticipo.</li>
        <li>Pagos (mock o pasarela), ticket con QR y envío por correo.</li>
        <li>Multilenguaje (es/en) y gestión de usuarios/roles (OWNER/ADMIN/STAFF/CUSTOMER).</li>
      </ul>

      <h3>Instalación rápida</h3>
      <p class="meta">Clonar repo → configurar <code>.env</code> → migrar y seed → levantar API + frontend</p>
      <ul>
        <li><code>git clone &lt;repo&gt;</code></li>
        <li><code>cp .env.example .env</code> y ajustar credenciales</li>
        <li><code>npm run db:migrate && npm run db:seed</code></li>
        <li><code>npm run dev</code> (API) y <code>npm run web:dev</code> (frontend)</li>
      </ul>

      <h3>Modelo de datos (resumen)</h3>
      <p class="meta">Entidades: Usuarios, Roles, Hoteles, Categorías, Habitaciones, Fotos, Equipamiento, Price_History, Reservas, Pagos.</p>

      <div class="footer">Licencia: MIT · Contacto: reservas@pacificreef.example</div>
    </div>

    <div>
      <div style="text-align:center;margin-bottom:12px">
        <img src="https://img.icons8.com/fluency/96/hotel.png" alt="hotel" style="max-width:96px">
      </div>
      <div style="background:#fcfbff;border-radius:8px;padding:12px">
        <strong>Rápido</strong>
        <p class="meta">Prototipo en 3 semanas: especificación → núcleo funcional → integración</p>
        <strong>Stack sugerido</strong>
        <p class="meta">Ionic/React o Angular · Node/Nest · PostgreSQL · Docker</p>
        <a class="btn" href="#">Ver DER</a>
      </div>
    </div>
  </div>
</div>
```

  </div>
</body>
</html>
