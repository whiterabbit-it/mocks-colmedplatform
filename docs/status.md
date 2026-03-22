# Status — mocks-colmedplatform
_Última actualización: 2026-03-22_

## Estado general
**Sprint 1 v0.2 — CERRADO** ✅
Todos los mocks de la fase de diseño están completos y publicados en GitHub Pages.

---

## Páginas creadas

### Admin (webapp)
| Archivo | Descripción | Estado |
|---|---|---|
| `admin-dashboard.html` | Dashboard principal | ✅ |
| `admin-communications.html` | Comunicaciones oficiales + lecturas | ✅ |
| `admin-foro.html` | Foro (ex Mensajería) — threads | ✅ |
| `admin-dms.html` | Mensajes directos — vista two-panel | ✅ |
| `admin-members.html` | Listado de miembros | ✅ |
| `admin-board.html` | Comisión Directiva con datos reales | ✅ |
| `admin-obras-sociales.html` | Hub OS: Convenios, Conflictos, Aranceles, Calendario, Recursos | ✅ |
| `admin-agenda.html` | Agenda de reuniones — calendario + lista | ✅ |
| `admin-contactos.html` | Contactos institucionales con DM | ✅ |
| `admin-facturacion.html` | Facturación — Próximamente banner | ✅ |
| `admin-reminders.html` | Reminders automáticos | ✅ |
| `admin-documentos.html` | Repositorio de documentos | ✅ |
| `admin-perfil.html` | Perfil de usuario — 8 secciones | ✅ |

### Mobile
| Archivo | Descripción | Estado |
|---|---|---|
| `mobile-modules.html` | Hub de módulos — 2-col grid, SVG icons | ✅ |
| `mobile-home.html` | Home | ✅ |
| `mobile-foro.html` | Foro (ex Mensajes) | ✅ |
| `mobile-dms.html` | DMs individual | ✅ |
| `mobile-ai.html` | IA assistant | ✅ |
| `mobile-credencial.html` | Credencial digital | ✅ |
| `mobile-board.html` | Comisión Directiva mobile | ✅ |
| `mobile-obras-sociales.html` | Obras Sociales mobile — 5 tabs | ✅ |
| `mobile-agenda.html` | Agenda mobile | ✅ |
| `mobile-perfil.html` | Perfil mobile — 8 secciones | ✅ |

### Público
| Archivo | Descripción | Estado |
|---|---|---|
| `public-directorio.html` | Directorio público sin login | ✅ |

### Herramientas del equipo
| Archivo | Descripción | Estado |
|---|---|---|
| `feedback-panel.html` | Panel admin de feedback — auth gate propio | ✅ |

---

## Toolbox de feedback (`assets/feedback.js`)
- Botón `💬` flotante en todas las páginas
- Drawer lateral con form de comentarios
- Login: nombre + email (no-admins); nombre + email + password (admins)
- ADMIN_EMAILS: `lucas@`, `hernan@`, `damian@whiterabbit.com.ar`
- ADMIN_PASSWORD: `followtherabbit!`
- Admins ven todos los comentarios; no-admins solo los propios
- Supabase: proyecto `mocks-feedback` (ref: `efuglxlxgbvhsaiecffs`)
- Tabla: `feedback_comments` — RLS habilitado (anon INSERT + SELECT)
- Free tier: ~500 MB storage, ~2GB bandwidth/mes — suficiente para la fase de review

## index.html — hub
- Card "Panel de Feedback" visible solo si `localStorage.feedback_user` tiene email admin WR
- Resto del hub público (sin login)

---

## Deploy
- GitHub Pages: `https://whiterabbit-it.github.io/mocks-colmedplatform/`
- Auto-deploy desde branch `main`

---

## Decisiones tomadas
- No OAuth — login simple con localStorage para mocks estáticos
- SVG-only iconography — sin emojis en ninguna pantalla
- Tab bar mobile: Módulos | Foro | DMs | Perfil
- DMs accesibles desde Contactos (no ítem nav separado en admin sidebar)
- Feedback panel excluido del hub público — visible solo a admins WR
