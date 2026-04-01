#!/usr/bin/env python3
"""
Brand color update script — CMRB #1A4EA8
Cambios:
  1a. Admin sidebar background #0B2340 → #1A4EA8
  1b. Admin sidebar-logo: nuevo logo circular + texto
  1c. Admin topbar: quitar logocmrb.jpg inline
  2a. Admin nav: renombrar "Directorio" → "Contactos" (link admin-directorio.html)
  2b. Admin nav: eliminar línea con href="admin-contactos.html"
  3a. Mobile status-bar y app-header background #0B2340 → #1A4EA8 (solo en CSS)
  3b. Mobile logo: 30px → 44px, 28px → 42px
  4a. mobile-directorio: arreglar app-header roto
  4b. mobile-directorio: renombrar "Directorio" → "Contactos" en contenido visible
  4c. Mobile tab bar: "Directorio" → "Contactos" en todos los mobile
  5.  mobile-dms: agregar header con logo en view-list
"""

import os
import re

BASE = "/Users/lucas/projects/mocks-colmedplatform"

ADMIN_FILES = [
    "admin-agenda.html",
    "admin-beneficios.html",
    "admin-board.html",
    "admin-communications.html",
    "admin-contactos.html",
    "admin-dashboard.html",
    "admin-directorio.html",
    "admin-dms.html",
    "admin-documentos.html",
    "admin-facturacion.html",
    "admin-foro.html",
    "admin-members.html",
    "admin-obras-sociales.html",
    "admin-perfil.html",
    "admin-reminders.html",
]

MOBILE_FILES = [
    "mobile-agenda.html",
    "mobile-ai.html",
    "mobile-beneficios.html",
    "mobile-board.html",
    "mobile-credencial.html",
    "mobile-directorio.html",
    "mobile-dms.html",
    "mobile-foro.html",
    "mobile-home.html",
    "mobile-modules.html",
    "mobile-obras-sociales.html",
    "mobile-perfil.html",
]

NEW_SIDEBAR_LOGO = """<div class="sidebar-logo">
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="background:white;border-radius:50%;width:44px;height:44px;display:flex;align-items:center;justify-content:center;overflow:hidden;flex-shrink:0;box-shadow:0 2px 8px rgba(0,0,0,0.2);">
      <img src="assets/logocmrb.jpg" alt="CMRB" style="width:42px;height:42px;border-radius:50%;object-fit:cover;">
    </div>
    <div>
      <div style="font-family:'Lora',serif;font-weight:700;font-size:18px;color:#fff;letter-spacing:1px;line-height:1.1;">CMRB</div>
      <div style="font-size:10px;color:#93c5fd;letter-spacing:0.3px;margin-top:1px;">CMRB | WRHMS</div>
    </div>
  </div>
</div>"""

TOPBAR_LOGO_TO_REMOVE = '<img src="assets/logocmrb.jpg" alt="CMRB" style="height:36px;width:36px;border-radius:50%;object-fit:cover;border:1px solid #e2e8f0;">'

DMS_HEADER = """<div style="background:#1A4EA8;padding:8px 20px 12px;display:flex;align-items:center;gap:8px;flex-shrink:0;">
  <div style="background:white;border-radius:50%;width:44px;height:44px;display:flex;align-items:center;justify-content:center;overflow:hidden;flex-shrink:0;box-shadow:0 2px 6px rgba(0,0,0,0.15);">
    <img src="assets/logocmrb.jpg" alt="CMRB" style="width:42px;height:42px;border-radius:50%;object-fit:cover;">
  </div>
  <span style="font-family:'Lora',serif;font-weight:700;font-size:17px;color:#fff;letter-spacing:2px;">CMRB</span>
</div>"""

FIXED_MOBILE_DIRECTORIO_HEADER = """  <div class="app-header">
    <div style="display:flex;align-items:center;gap:8px;">
      <div style="background:white;border-radius:50%;width:44px;height:44px;display:flex;align-items:center;justify-content:center;overflow:hidden;flex-shrink:0;box-shadow:0 2px 6px rgba(0,0,0,0.15);">
        <img src="assets/logocmrb.jpg" alt="CMRB" style="width:42px;height:42px;border-radius:50%;object-fit:cover;">
      </div>
      <span style="font-family:'Lora',serif;font-weight:700;font-size:17px;color:#fff;letter-spacing:2px;">CMRB</span>
    </div>
  </div>"""


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def process_admin(filename):
    path = os.path.join(BASE, filename)
    content = read(path)
    original = content

    # 1a. Sidebar background
    content = content.replace(
        "width: 240px; min-height: 100vh; background: #0B2340;",
        "width: 240px; min-height: 100vh; background: #1A4EA8;"
    )

    # 1b. Reemplazar sidebar-logo completo con regex (re.DOTALL para multilinea)
    content = re.sub(
        r'<div class="sidebar-logo">.*?</div>',
        NEW_SIDEBAR_LOGO,
        content,
        count=1,
        flags=re.DOTALL
    )

    # 1c. Quitar logo del topbar
    content = content.replace(TOPBAR_LOGO_TO_REMOVE, "")

    # 2a. Renombrar "Directorio" → "Contactos" en el nav item de admin-directorio.html
    content = content.replace("></span> Directorio</a>", "></span> Contactos</a>")

    # 2b. Eliminar bloque completo del nav item de admin-contactos.html
    #     El bloque puede ser multilínea: <a href="admin-contactos.html" ...>...</a>
    #     (excepto en admin-contactos.html donde el item activo puede quedarse)
    if filename != "admin-contactos.html":
        # Eliminar el bloque completo <a href="admin-contactos.html"...>...</a>
        content = re.sub(
            r'\s*<a href="admin-contactos\.html"[^>]*>[\s\S]*?</a>',
            '',
            content,
            count=1
        )

    if content != original:
        write(path, content)
        print(f"  [OK] {filename}")
    else:
        print(f"  [--] {filename} — sin cambios")


def process_mobile(filename):
    path = os.path.join(BASE, filename)
    content = read(path)
    original = content

    # 3a. Status-bar background en CSS — multilinea y en-línea
    # Patrón multilinea (mobile-home style)
    content = re.sub(
        r'(/\* Status bar \*/\s*\.status-bar \{[^}]*?)background: #0B2340;',
        r'\1background: #1A4EA8;',
        content,
        flags=re.DOTALL
    )
    # Patrón en-línea: .status-bar { background: #0B2340; padding: ...
    content = re.sub(
        r'(\.status-bar \{[^}]*?)background: #0B2340;',
        r'\1background: #1A4EA8;',
        content,
        flags=re.DOTALL
    )

    # 3a. App-header background en CSS
    content = re.sub(
        r'(\.app-header \{[^}]*?)background: #0B2340;',
        r'\1background: #1A4EA8;',
        content,
        flags=re.DOTALL
    )

    # 3b. Logo mobile: 30px → 44px, 28px → 42px (solo en contexto del logo circular del header)
    content = content.replace(
        "background:white;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center;overflow:hidden;flex-shrink:0;",
        "background:white;border-radius:50%;width:44px;height:44px;display:flex;align-items:center;justify-content:center;overflow:hidden;flex-shrink:0;box-shadow:0 2px 6px rgba(0,0,0,0.15);"
    )
    content = content.replace(
        'style="width:28px;height:28px;border-radius:50%;object-fit:cover;"',
        'style="width:42px;height:42px;border-radius:50%;object-fit:cover;"'
    )

    # 4c. Tab bar: "Directorio" → "Contactos" en todos los mobile
    # El patrón es el texto "Directorio" en el tab bar (dentro de .tab-item)
    # Hay variantes con salto de línea:
    #   >Directorio\n    </a>
    #   >      Directorio\n    </a>
    content = re.sub(
        r'(href="mobile-directorio\.html"[^>]*>[\s\S]*?<span[^>]*>[\s\S]*?</span>\s*)Directorio(\s*</a>)',
        r'\1Contactos\2',
        content
    )

    if content != original:
        write(path, content)
        print(f"  [OK] {filename}")
    else:
        print(f"  [--] {filename} — sin cambios")


def fix_mobile_directorio():
    filename = "mobile-directorio.html"
    path = os.path.join(BASE, filename)
    content = read(path)
    original = content

    # 4a. Arreglar el app-header roto
    # El problema: hay 3 closing </div> en lugar de 2 (lineas 383-391)
    # Buscar el bloque roto con regex y reemplazarlo limpio
    broken_pattern = re.compile(
        r'<div class="app-header">\s*<div[^>]*>\s*<div[^>]*>\s*<img[^>]*logocmrb[^>]*>\s*</div>\s*<span[^>]*>CMRB</span>\s*</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    content = broken_pattern.sub(FIXED_MOBILE_DIRECTORIO_HEADER, content, count=1)

    # 4b. Renombrar "Buscar colegas" → "Buscar contactos"
    content = content.replace('placeholder="Buscar colegas..."', 'placeholder="Buscar contactos..."')

    # El title de la página en tab bar ya se maneja en process_mobile (4c)
    # El tab item activo en mobile-directorio.html:
    content = re.sub(
        r'(<a href="mobile-directorio\.html" class="tab-item active"[^>]*>[\s\S]*?</span>\s*)Directorio(\s*</a>)',
        r'\1Contactos\2',
        content
    )

    if content != original:
        write(path, content)
        print(f"  [OK] {filename} — header arreglado + Contactos")
    else:
        print(f"  [--] {filename} — sin cambios (revisar regex)")


def fix_mobile_dms():
    filename = "mobile-dms.html"
    path = os.path.join(BASE, filename)
    content = read(path)
    original = content

    # 3a. Status bar background (formato en-línea en dms)
    # Ya manejado en process_mobile, pero verificar
    # El formato en dms es: background: #0B2340; padding: 12px 24px 8px; (en línea)
    content = content.replace(
        "background: #0B2340; padding: 12px 24px 8px;",
        "background: #1A4EA8; padding: 12px 24px 8px;"
    )

    # 5. Agregar header con logo dentro de #view-list, antes del primer elemento
    # Buscar <div id="view-list" ...> y agregar el header inmediatamente después
    view_list_pattern = re.compile(
        r'(<div id="view-list"[^>]*>)',
        re.DOTALL
    )
    replacement = r'\1\n' + DMS_HEADER
    content = view_list_pattern.sub(replacement, content, count=1)

    if content != original:
        write(path, content)
        print(f"  [OK] {filename} — header agregado + color actualizado")
    else:
        print(f"  [--] {filename} — sin cambios (revisar regex)")


# ── MAIN ──────────────────────────────────────────────────

print("\n=== ADMIN FILES ===")
for f in ADMIN_FILES:
    process_admin(f)

print("\n=== MOBILE FILES ===")
for f in MOBILE_FILES:
    process_mobile(f)

print("\n=== MOBILE DIRECTORIO (fix especial) ===")
fix_mobile_directorio()

print("\n=== MOBILE DMS (fix especial) ===")
fix_mobile_dms()

print("\nDone.")
