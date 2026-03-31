# SPECS — Beneficios + Directorio de Socios
## CMRB App — Nuevas Features (mocks HTML estáticos)

**Diseñado por:** R2-D2 (UX/UI)
**Última actualización:** 2026-03-31
**Destino:** 4 páginas HTML → `admin-beneficios.html`, `mobile-beneficios.html`, `admin-directorio.html`, `mobile-directorio.html`

---

## FEATURE 1: BENEFICIOS PARA EL SOCIO

### 1.1 — ADMIN PANEL: `admin-beneficios.html`

#### Propósito
Panel de gestión para administradores. Crear, editar, filtrar y visualizar beneficios disponibles para socios del CMRB.

#### Layout — Estructura HTML

```
Sidebar (240px fixed, navy #0B2340)
  ├─ Logo CMRB
  ├─ Nav items (active: Beneficios)
  └─ User info

Main content (margin-left: 240px)
  ├─ Topbar (white, 60px, "Beneficios para Socios")
  └─ Content area
      ├─ Page header
      │   ├─ H1: "Beneficios para Socios"
      │   └─ Subtitle: "Gestiona descuentos, promociones y servicios..."
      ├─ Controls row
      │   ├─ Filtros (state, category) — dropdowns
      │   ├─ Search input (buscar por nombre/partner)
      │   └─ [+ Nuevo Beneficio] button — abre modal
      ├─ Benefits grid (auto-fill, minmax 320px)
      │   └─ Benefit cards (× 6+ ejemplo)
      │       ├─ Partner logo/image area
      │       ├─ Title + description
      │       ├─ Category badge
      │       ├─ State badge (Disponible / Próximamente)
      │       ├─ Date range (desde–hasta)
      │       └─ Actions (Edit, Delete buttons)
      └─ Create/Edit Benefit Modal
          ├─ Form fields:
          │   ├─ Título
          │   ├─ Descripción (textarea)
          │   ├─ Categoría (select)
          │   ├─ Estado (select: Disponible / Próximamente)
          │   ├─ Fecha desde
          │   ├─ Fecha hasta (opcional)
          │   ├─ Logo/Imagen (file input)
          │   └─ Link externo (URL)
          └─ Actions: [Cancelar] [Guardar]
```

#### CSS Classes Necesarias

```css
/* Benefit Card */
.benefit-card {
  background: white;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  padding: 16px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: all 0.2s;
  cursor: pointer;
}
.benefit-card:hover {
  border-color: #00A896;
  box-shadow: 0 8px 16px rgba(0,168,150,0.12);
}

.benefit-image {
  width: 100%;
  height: 140px;
  background: #F3F6F9;
  border-radius: 10px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #94a3b8;
  overflow: hidden;
}
.benefit-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.benefit-title {
  font-family: 'Lora', serif;
  font-size: 16px;
  font-weight: 700;
  color: #0B2340;
  margin-bottom: 6px;
  line-height: 1.35;
}

.benefit-desc {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 10px;
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.benefit-meta {
  display: flex;
  gap: 6px;
  margin-bottom: 10px;
  flex-wrap: wrap;
  padding-bottom: 10px;
  border-bottom: 1px solid #f1f5f9;
}

.badge-category {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}
.badge-cat-descuentos { background: #D6F5F1; color: #00A896; }
.badge-cat-salud { background: #dbeafe; color: #0284c7; }
.badge-cat-educacion { background: #fce7f3; color: #be185d; }
.badge-cat-viajes { background: #fef3c7; color: #F0A500; }
.badge-cat-otros { background: #f3e8ff; color: #7c3aed; }

.badge-state {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}
.badge-disponible { background: #D6F5F1; color: #00A896; }
.badge-proximo { background: #fef3c7; color: #F0A500; }

.benefit-dates {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 12px;
}

.benefit-actions {
  display: flex;
  gap: 8px;
}
.btn-edit, .btn-delete {
  flex: 1;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Poppins', sans-serif;
  border: none;
  transition: all 0.15s;
}
.btn-edit {
  background: #E8EFF8;
  color: #0B2340;
}
.btn-edit:hover {
  background: #D1DFF2;
}
.btn-delete {
  background: #fecaca;
  color: #dc2626;
}
.btn-delete:hover {
  background: #fca5a5;
}

/* Filters & Controls */
.controls-row {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Poppins', sans-serif;
  color: #0B2340;
  background: white;
  cursor: pointer;
  transition: all 0.15s;
}
.filter-select:hover {
  border-color: #cbd5e1;
  background: #F3F6F9;
}

.search-input {
  flex: 1;
  min-width: 200px;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Poppins', sans-serif;
  color: #0B2340;
  transition: all 0.15s;
}
.search-input:focus {
  outline: none;
  border-color: #00A896;
  box-shadow: 0 0 0 3px rgba(0,168,150,0.1);
}

.btn-new-benefit {
  margin-left: auto;
  padding: 10px 16px;
  background: #00A896;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  gap: 6px;
}
.btn-new-benefit:hover {
  background: #008B7A;
}

/* Modal */
.modal-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(11,35,64,0.4);
  z-index: 9000;
  align-items: center;
  justify-content: center;
}
.modal-overlay.open {
  display: flex;
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 28px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}
.modal-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #0B2340;
}
.modal-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #64748b;
  transition: color 0.15s;
}
.modal-close:hover {
  color: #0B2340;
}

.form-group {
  margin-bottom: 16px;
}
.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #0B2340;
  margin-bottom: 6px;
}
.form-input, .form-textarea, .form-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Poppins', sans-serif;
  color: #0B2340;
  transition: all 0.15s;
  box-sizing: border-box;
}
.form-input:focus, .form-textarea:focus, .form-select:focus {
  outline: none;
  border-color: #00A896;
  box-shadow: 0 0 0 3px rgba(0,168,150,0.1);
}
.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}
.btn-cancel {
  flex: 1;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Poppins', sans-serif;
  background: white;
  color: #0B2340;
  transition: all 0.15s;
}
.btn-cancel:hover {
  background: #F3F6F9;
}
.btn-save {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Poppins', sans-serif;
  background: #00A896;
  color: white;
  transition: all 0.15s;
}
.btn-save:hover {
  background: #008B7A;
}
```

#### Data de Ejemplo

```javascript
const beneficios = [
  {
    id: 1,
    titulo: "Descuento en Farmacias Del Dr. Ahorro",
    descripcion: "Hasta 30% de descuento en medicamentos y productos de parafarmacia en todas las sucursales de Bariloche.",
    categoria: "descuentos",
    estado: "disponible",
    logo: "partner-farmacia.png",
    link: "https://farmaciasdel.com.ar",
    desde: "2026-01-15",
    hasta: "2026-12-31"
  },
  {
    id: 2,
    titulo: "Cobertura Especial IOMA + Programa de Prevención",
    descripcion: "Acceso prioritario a estudios preventivos y cobertura extendida en cirugías de riesgo. Coordinación directa con auditoría médica.",
    categoria: "salud",
    estado: "disponible",
    logo: "partner-ioma.png",
    link: "https://ioma.gob.ar",
    desde: "2026-03-01",
    hasta: null
  },
  {
    id: 3,
    titulo: "Capacitación Acreditada — IFCM",
    descripcion: "Cursos de educación continua, talleres de actualización, congresos internacionales. Créditos para matrícula.",
    categoria: "educacion",
    estado: "proximo",
    logo: "partner-ifcm.png",
    link: "https://ifcm-bariloche.edu.ar",
    desde: "2026-04-15",
    hasta: null
  },
  {
    id: 4,
    titulo: "Descuento en Viajes — TravelMed",
    descripcion: "Paquetes vacacionales con descuentos, seguros de viaje médico, asistencia al viajero 24/7.",
    categoria: "viajes",
    estado: "disponible",
    logo: "partner-travelmed.png",
    link: "https://travelmed.com.ar",
    desde: "2025-06-01",
    hasta: "2026-12-31"
  },
  {
    id: 5,
    titulo: "Seguros Especiales — Seguros Médicos CMRB",
    descripcion: "Pólizas de responsabilidad civil, cobertura de incapacidad laboral, seguros de vida con primas reducidas.",
    categoria: "otros",
    estado: "disponible",
    logo: "partner-seguros.png",
    link: "https://segurosmedicos.com.ar",
    desde: "2025-08-01",
    hasta: "2027-07-31"
  },
  {
    id: 6,
    titulo: "Plataforma de Gestión Clínica — Vitacore",
    descripcion: "Software de gestión médica con IA, auditoría inteligente, integración con histórico del paciente.",
    categoria: "otros",
    estado: "proximo",
    logo: "partner-vitacore.png",
    link: "https://vitacore.com.ar",
    desde: "2026-05-01",
    hasta: null
  }
];
```

#### Interacciones & Comportamientos

- **Filtro Estado:** Dropdown que filtra cards (`display: none` para las que no coincidan)
- **Filtro Categoría:** Dropdown con multi-select opcional (checkbox)
- **Search input:** Busca en `titulo` y en el campo de partner del beneficio
- **Hover en card:** Cambia `border-color` a teal, aplica `box-shadow`
- **Click [+ Nuevo Beneficio]:** Abre modal vacío con form limpio
- **Click [Edit]:** Abre modal pre-poblado con datos del beneficio
- **Click [Delete]:** Muestra confirmación simple (`confirm()`) antes de remover
- **Click en overlay del modal:** Cierra modal sin guardar
- **Click [Guardar]:** Valida que título y descripción no estén vacíos; si pasa, cierra modal y actualiza la grid

#### Accesibilidad

- Todos los inputs con `<label>` asociado (`for="..."`)
- Focus visible en inputs con color teal `border-color: #00A896`
- Modal con `aria-modal="true"`, `role="dialog"`
- Botones con texto claro (no solo ícono)
- Ratios de contraste: navy #0B2340 sobre blanco > 4.5:1; teal #00A896 sobre blanco > 3:1

---

### 1.2 — MOBILE: `mobile-beneficios.html`

#### Propósito
Vista del socio médico viendo sus beneficios disponibles. Dos secciones: DISPONIBLES (teal) y PRÓXIMAMENTE (amber).

#### Layout — Estructura HTML

```
Phone frame (390px × 844px)
  ├─ Status bar (navy, 12:34, icons)
  ├─ App header (navy, logo CMRB, notif btn)
  ├─ Scroll area
  │   ├─ Page title "Beneficios"
  │   ├─ Section "DISPONIBLES AHORA" (teal accent)
  │   │   └─ Benefit cards (× 3-4)
  │   │       ├─ Partner logo (small, left)
  │   │       ├─ Title
  │   │       ├─ Category badge (teal)
  │   │       ├─ Short description
  │   │       └─ [Ver más] link (teal)
  │   ├─ Section "PRÓXIMAMENTE" (amber accent)
  │   │   └─ Benefit cards (× 2)
  │   │       └─ Similar layout + "Desde DD de mes YYYY" date
  │   └─ Empty state si no hay beneficios
  └─ Tab bar (Módulos | Foro | DMs | Perfil)
```

#### CSS Classes Necesarias

```css
.benefit-list {
  padding: 16px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 20px 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #00A896; /* DISPONIBLES */
}
.section-header.proximo {
  border-bottom-color: #F59E0B; /* PRÓXIMAMENTE */
}

.section-title {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #0B2340;
}

.section-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00A896; /* DISPONIBLES */
}
.section-dot.proximo {
  background: #F59E0B; /* PRÓXIMAMENTE */
}

.mobile-benefit-card {
  background: white;
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 10px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.mobile-benefit-logo {
  width: 56px;
  height: 56px;
  background: #F3F6F9;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 11px;
  color: #94a3b8;
  overflow: hidden;
}
.mobile-benefit-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mobile-benefit-content {
  flex: 1;
  min-width: 0;
}

.mobile-benefit-title {
  font-size: 14px;
  font-weight: 700;
  color: #0B2340;
  margin-bottom: 4px;
  line-height: 1.35;
}

.mobile-benefit-desc {
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.mobile-benefit-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.mobile-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 10px;
  font-weight: 600;
}
.mobile-badge-descuentos { background: #D6F5F1; color: #00A896; }
.mobile-badge-salud { background: #dbeafe; color: #0284c7; }
.mobile-badge-educacion { background: #fce7f3; color: #be185d; }
.mobile-badge-viajes { background: #fef3c7; color: #F0A500; }

.mobile-see-more {
  color: #00A896;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}

.mobile-date-start {
  color: #94a3b8;
  font-size: 11px;
  font-style: italic;
}

.empty-state {
  text-align: center;
  padding: 40px 24px;
  color: #94a3b8;
}
.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}
.empty-title {
  font-size: 15px;
  font-weight: 600;
  color: #0B2340;
  margin-bottom: 6px;
}
.empty-text {
  font-size: 13px;
  color: #94a3b8;
}
```

#### Data de Ejemplo (igual a admin)

Usar mismo JSON de beneficios pero filtrado por estado (`disponible` vs `proximo`).

#### Interacciones

- **Scroll:** Scroll within scroll-area, tab bar siempre visible abajo
- **[Ver más]:** Click abre modal con descripción completa del beneficio + botón "Visitar sitio" (link externo)
- **Tab bar:** Navegación entre Módulos, Foro, DMs, Perfil (dentro del mock, sin navegación real)

#### Accesibilidad

- Dos secciones con `<h2>` semántico (DISPONIBLES, PRÓXIMAMENTE)
- Links [Ver más] con `role="button"` si es JS, o `<a>` si es HTML puro
- Cards con `.mobile-benefit-card` con suficiente padding/touch target

---

## FEATURE 2: DIRECTORIO DE SOCIOS

### 2.1 — ADMIN PANEL: `admin-directorio.html`

#### Propósito
Buscador interno de socios para administrador. Buscar por nombre, especialidad, matrícula. Enviar mensajes directos.

#### Layout — Estructura HTML

```
Sidebar (240px fixed, navy)
Main content
  ├─ Topbar
  ├─ Content area
      ├─ Page header "Directorio de Socios"
      ├─ Search & filters row
      │   ├─ Search input (nombre/especialidad/matrícula)
      │   ├─ Filter select (Socio Activo / Miembro de Comisión)
      │   └─ Filter select (Especialidad)
      ├─ Results info ("X socios encontrados")
      └─ Socios grid (auto-fill, minmax 280px)
          └─ Socio cards (× 10+)
              ├─ Avatar (initials)
              ├─ Nombre
              ├─ Especialidad
              ├─ Matrícula
              ├─ Email (link)
              ├─ Teléfono
              ├─ Badge si es miembro de comisión
              └─ Actions ([Enviar mensaje], [Ver perfil])
```

#### CSS Classes Necesarias

```css
.socio-card {
  background: white;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  padding: 18px 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
}
.socio-card:hover {
  border-color: #00A896;
  box-shadow: 0 8px 16px rgba(0,168,150,0.12);
}

.socio-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.socio-avatar {
  width: 48px;
  height: 48px;
  background: #00A896;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.socio-header-info {
  flex: 1;
}

.socio-name {
  font-size: 15px;
  font-weight: 700;
  color: #0B2340;
  margin-bottom: 2px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.socio-specialty {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
}

.socio-matricula {
  font-size: 11px;
  color: #94a3b8;
  font-family: 'Courier New', monospace;
}

.badge-comision {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  background: #FEE2E2;
  color: #DC2626;
  border-radius: 10px;
  font-size: 10px;
  font-weight: 600;
  gap: 3px;
}

.socio-contact {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
  padding: 10px;
  background: #F9FAFB;
  border-radius: 8px;
  border-left: 2px solid #e2e8f0;
}

.contact-item {
  font-size: 12px;
  color: #0B2340;
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-label {
  color: #94a3b8;
  font-weight: 500;
  min-width: 60px;
}

.contact-value {
  color: #0B2340;
  flex: 1;
}

.contact-email-link {
  color: #00A896;
  text-decoration: none;
  cursor: pointer;
}
.contact-email-link:hover {
  text-decoration: underline;
}

.socio-actions {
  display: flex;
  gap: 8px;
}

.btn-msg-socio {
  flex: 1;
  padding: 8px 10px;
  background: #00A896;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-msg-socio:hover {
  background: #008B7A;
}

.btn-profile-socio {
  flex: 1;
  padding: 8px 10px;
  background: white;
  color: #0B2340;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-profile-socio:hover {
  background: #F3F6F9;
  border-color: #cbd5e1;
}

.search-row {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
  align-items: center;
}

.search-input-socio {
  flex: 1;
  min-width: 220px;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Poppins', sans-serif;
  color: #0B2340;
}
.search-input-socio:focus {
  outline: none;
  border-color: #00A896;
  box-shadow: 0 0 0 3px rgba(0,168,150,0.1);
}

.filter-select-socio {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Poppins', sans-serif;
  color: #0B2340;
  background: white;
  cursor: pointer;
}

.results-info {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 16px;
  padding: 12px;
  background: #F9FAFB;
  border-radius: 8px;
  border-left: 2px solid #e2e8f0;
}
.results-count {
  font-weight: 600;
  color: #0B2340;
}

.no-results {
  text-align: center;
  padding: 40px 24px;
}
.no-results-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.4;
}
.no-results-title {
  font-size: 15px;
  font-weight: 600;
  color: #0B2340;
  margin-bottom: 6px;
}
.no-results-text {
  font-size: 13px;
  color: #94a3b8;
}
```

#### Data de Ejemplo

```javascript
const socios = [
  {
    id: 1,
    nombre: "Dr. Federico Martínez",
    especialidad: "Traumatología",
    matricula: "T-8841-ARG",
    email: "f.martinez@cmrb.com.ar",
    telefono: "+54 294 4428334",
    esComision: true
  },
  {
    id: 2,
    nombre: "Dra. Gabriela Fernández",
    especialidad: "Cardiología",
    matricula: "C-7229-ARG",
    email: "g.fernandez@cmrb.com.ar",
    telefono: "+54 294 4456221",
    esComision: false
  },
  {
    id: 3,
    nombre: "Dr. Andrés López Ramirez",
    especialidad: "Pediatría",
    matricula: "P-4502-ARG",
    email: "a.lopez.ramirez@cmrb.com.ar",
    telefono: "+54 294 4612339",
    esComision: true
  },
  {
    id: 4,
    nombre: "Dra. Mariana Gómez",
    especialidad: "Oftalmología",
    matricula: "O-6891-ARG",
    email: "m.gomez@cmrb.com.ar",
    telefono: "+54 294 4734455",
    esComision: false
  },
  {
    id: 5,
    nombre: "Dr. Carlos Sánchez Ruiz",
    especialidad: "Neurología",
    matricula: "N-5567-ARG",
    email: "c.sanchez.ruiz@cmrb.com.ar",
    telefono: "+54 294 4821676",
    esComision: false
  },
  {
    id: 6,
    nombre: "Dra. María Paula Arrigoni",
    especialidad: "Dermatología",
    matricula: "D-3344-ARG",
    email: "m.arrigoni@cmrb.com.ar",
    telefono: "+54 294 4903442",
    esComision: false
  },
  {
    id: 7,
    nombre: "Dr. Juan Carlos Monteros",
    especialidad: "Urología",
    matricula: "U-7721-ARG",
    email: "j.monteros@cmrb.com.ar",
    telefono: "+54 294 4541998",
    esComision: true
  },
  {
    id: 8,
    nombre: "Dra. Susana Benítez",
    especialidad: "Oncología",
    matricula: "ON-2288-ARG",
    email: "s.benitez@cmrb.com.ar",
    telefono: "+54 294 4667833",
    esComision: false
  },
  {
    id: 9,
    nombre: "Dr. Roberto Díaz Martínez",
    especialidad: "Cirugía General",
    matricula: "CG-9004-ARG",
    email: "r.diaz.martinez@cmrb.com.ar",
    telefono: "+54 294 4789123",
    esComision: false
  },
  {
    id: 10,
    nombre: "Dra. Laura Vázquez García",
    especialidad: "Psiquiatría",
    matricula: "PS-5556-ARG",
    email: "l.vazquez.garcia@cmrb.com.ar",
    telefono: "+54 294 4850441",
    esComision: false
  },
  {
    id: 11,
    nombre: "Dr. Javier González",
    especialidad: "Otorrinolaringología",
    matricula: "ORL-3312-ARG",
    email: "j.gonzalez@cmrb.com.ar",
    telefono: "+54 294 4925514",
    esComision: true
  },
  {
    id: 12,
    nombre: "Dra. Constanza Vega",
    especialidad: "Gastroenterología",
    matricula: "G-8876-ARG",
    email: "c.vega@cmrb.com.ar",
    telefono: "+54 294 4612277",
    esComision: false
  }
];
```

#### Interacciones

- **Search input:** Busca en `nombre`, `especialidad`, `matricula` (case-insensitive, parcial)
- **Filter tipo socio:** "Todos", "Socios Activos", "Miembros de Comisión"
- **Filter especialidad:** Dropdown con todas las especialidades únicas + "Todas"
- **[Enviar mensaje]:** Abre modal DM igual al de `admin-contactos.html` (reusar estructura CSS)
- **[Ver perfil]:** En mock, simplemente mostrar un alert con el perfil (sin navegación real)
- **Results info:** Actualiza dinámicamente ("12 socios encontrados")
- **No results:** Muestra empty state si la búsqueda/filtros no retornan nada

#### Accesibilidad

- Inputs con `<label>` asociado
- Focus visible teal
- Page title con `<h1>`
- Datos de contacto con `<dl>` semántico opcional

---

### 2.2 — MOBILE: `mobile-directorio.html`

#### Propósito
Explorador de contactos mobile. Socio busca colegas, ve especialidad, inicia chat.

#### Layout — Estructura HTML

```
Phone frame (390px × 844px)
  ├─ Status bar
  ├─ App header
  ├─ Scroll area
  │   ├─ Search bar (nombre/especialidad)
  │   ├─ Filter pills (Todos / Comisión)
  │   ├─ Socio list
  │   │   └─ Socio items (× 10+)
  │   │       ├─ Avatar (initials, teal bg)
  │   │       ├─ Name
  │   │       ├─ Specialty (secondary text)
  │   │       ├─ Badge si es comisión
  │   │       └─ Tap area (accesible)
  │   └─ Contact detail sheet (expandible? O modal?)
  │       ├─ Full name + especialidad
  │       ├─ Email + teléfono
  │       ├─ [Chat] button
  │       └─ [Cerrar]
  └─ Tab bar
```

#### CSS Classes Necesarias

```css
.mobile-directory-search {
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

.mobile-search-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Poppins', sans-serif;
  color: #0B2340;
  background: #F9FAFB;
}
.mobile-search-input:focus {
  outline: none;
  border-color: #00A896;
  background: white;
}

.mobile-filter-pills {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.mobile-filter-pills::-webkit-scrollbar {
  display: none;
}

.filter-pill {
  padding: 8px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  background: white;
  color: #0B2340;
  font-size: 12px;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.15s;
}
.filter-pill.active {
  background: #00A896;
  color: white;
  border-color: #00A896;
}

.mobile-socio-list {
  padding: 0;
}

.mobile-socio-item {
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  gap: 12px;
  align-items: center;
  cursor: pointer;
  transition: background 0.15s;
}
.mobile-socio-item:active {
  background: #F3F6F9;
}

.mobile-socio-avatar {
  width: 48px;
  height: 48px;
  background: #00A896;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.mobile-socio-info {
  flex: 1;
  min-width: 0;
}

.mobile-socio-name {
  font-size: 14px;
  font-weight: 700;
  color: #0B2340;
  margin-bottom: 2px;
}

.mobile-socio-specialty-badge {
  display: flex;
  align-items: center;
  gap: 6px;
}

.mobile-specialty {
  font-size: 12px;
  color: #64748b;
}

.mobile-comision-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 6px;
  background: #FEE2E2;
  color: #DC2626;
  border-radius: 8px;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

/* Contact Detail Sheet / Modal */
.mobile-contact-sheet {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-radius: 20px 20px 0 0;
  padding: 20px 16px 40px;
  z-index: 1000;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.12);
  animation: slideUp 0.3s ease-out;
}
.mobile-contact-sheet.open {
  display: block;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.sheet-handle {
  width: 40px;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  margin: 0 auto 16px;
}

.sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.sheet-title {
  font-size: 17px;
  font-weight: 700;
  color: #0B2340;
}

.sheet-close {
  background: none;
  border: none;
  font-size: 20px;
  color: #94a3b8;
  cursor: pointer;
}

.sheet-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.sheet-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sheet-label {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.sheet-value {
  font-size: 14px;
  color: #0B2340;
}

.sheet-value-email {
  color: #00A896;
  text-decoration: none;
}

.sheet-actions {
  display: flex;
  gap: 10px;
}

.btn-chat-sheet {
  flex: 1;
  padding: 12px;
  background: #00A896;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-chat-sheet:active {
  background: #008B7A;
}

.btn-close-sheet {
  flex: 1;
  padding: 12px;
  background: #F3F6F9;
  color: #0B2340;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-close-sheet:active {
  background: #E8EFF8;
}
```

#### Data de Ejemplo

Igual al directorio admin (mismo JSON de socios).

#### Interacciones

- **Search bar:** Filtra lista por nombre/especialidad en tiempo real
- **Filter pills (Todos / Comisión):** Filtra lista (`display: none` para items que no coincidan)
- **Tap en socio:** Abre sheet bottom con detalles (nombre, especialidad, email, teléfono)
- **[Chat]:** Click en sheet abre DM modal (ídem a admin-contactos.html)
- **[Cerrar] en sheet O tap fuera:** Cierra sheet
- **Sheet draggable:** Si queda capacidad, permitir arrastrar para cerrar (no crítico en mock)

#### Accesibilidad

- Items con `.mobile-socio-item` con `role="button"` implícito o explícito
- Touch targets ≥ 48px altura (cumple con 12px padding × 2 + 14px text = 48px)
- Search input focusable con outline teal
- Sheet con `aria-modal="true"` si es accesible

---

## RESUMEN DE ARCHIVOS Y CONVENCIONES

### Archivos a crear/modificar
1. `/mocks-colmedplatform/admin-beneficios.html` — Admin: gestión de beneficios
2. `/mocks-colmedplatform/mobile-beneficios.html` — Mobile: vista socio beneficios
3. `/mocks-colmedplatform/admin-directorio.html` — Admin: búsqueda de socios
4. `/mocks-colmedplatform/mobile-directorio.html` — Mobile: explorador de contactos

### Colores ya definidos (respetar exactamente)
- Navy primary: `#0B2340`
- Teal accent: `#00A896`
- Light bg: `#F3F6F9`
- Orange alert: `#E8735A`
- Amber (próximamente): `#F59E0B`
- Error red: `#DC2626` (para comisión directiva badge)

### Fuentes
- Serif (títulos): `'Lora', serif`
- Sans-serif (body): `'Poppins', system-ui, sans-serif`

### Iconografía
- SVG-only, CERO emojis
- Inline SVG o assets SVG (no emojis como fallback)

### Especificidades de interacción

**Admin Beneficios:**
- Modal de creación/edición con form validation
- Filtros dropdown + search
- Cards con hover teal + shadow
- Delete con confirmación simple

**Mobile Beneficios:**
- Dos secciones con color accent (teal/amber)
- Cards compactas con 2 líneas de descripción max
- Click [Ver más] abre modal con descripción completa

**Admin Directorio:**
- Search + dos filtros (tipo socio, especialidad)
- Cards con info de contacto visible
- DM modal reutilizado de admin-contactos.html
- Badge "Comisión" en rojo (#DC2626)

**Mobile Directorio:**
- Search bar + filter pills
- List de items tap-able
- Bottom sheet con contacto detail
- Chat button en sheet

---

## TESTING CHECKLIST

- [ ] Todos los inputs con `<label>` asociado (`for="..."`)
- [ ] Focus visible (teal border) en todos los inputs
- [ ] Contraste WCAG AA (navy sobre blanco, teal sobre blanco, rojo para comisión)
- [ ] SVG icons sin emojis fallback
- [ ] Mobile responsivity: phone frame 390×844px, no overflow horizontal
- [ ] Modales cerrables con Esc o click en overlay
- [ ] Tab bar siempre visible en mobile (72px bottom offset)
- [ ] Sidebar fijo 240px en admin, sin horizontal scroll
- [ ] Cards con hover states coherentes
- [ ] Empty states cuando no hay resultados
- [ ] Data example realista (nombres médicos argentinos, especialidades reales)

---

## NOTAS PARA LEIA

Este document es tu fuente de verdad. Todos los estilos, clases, estructuras y comportamientos están especificados aquí. Si hay ambigüedad, preguntame antes de implementar. Los datos de ejemplo son para mock — en producción vendrán de una API.

Cada página tiene su propia estructura HTML, pero reusan componentes base (sidebar, topbar, modal DM, tab bar). No copies CSS innecesariamente — crea estilos generales en `<style>` de cada página.

Las interacciones JavaScript son vanilla JS puro (sin frameworks). Usa `classList.add/remove/toggle` para estados, `display: none` para filtros, y `document.getElementById()` para referencias.

Accesibilidad es non-negotiable: todos los elementos interactivos deben ser teclado-accesibles y tener focus visible.

