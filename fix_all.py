#!/usr/bin/env python3
"""
Script de correcciones masivas para mocks-colmedplatform.
Correcciones 1, 2, 3, 5 y 6 (la 4 se hace aparte).
"""

import os
import re

BASE = '/Users/lucas/projects/mocks-colmedplatform'

# ─────────────────────────────────────────────
# CORRECCIÓN 1 — Orden sidebar: Beneficios ANTES de Contactos
# ─────────────────────────────────────────────

C1_FILES = [
    'admin-agenda.html', 'admin-board.html', 'admin-communications.html',
    'admin-contactos.html', 'admin-dashboard.html', 'admin-dms.html',
    'admin-documentos.html', 'admin-facturacion.html', 'admin-foro.html',
    'admin-members.html', 'admin-obras-sociales.html', 'admin-perfil.html',
    'admin-reminders.html',
]

def swap_beneficios_contactos(html):
    """
    Encuentra las líneas de nav-item de Contactos y Beneficios y las intercambia
    para que Beneficios quede primero. Trabaja buscando el href en la línea.
    """
    pat_c = re.compile(r'(<a\s[^>]*admin-contactos\.html[^>]*>.*?</a>[^\n]*\n)', re.DOTALL)
    pat_b = re.compile(r'(<a\s[^>]*admin-beneficios\.html[^>]*>.*?</a>[^\n]*\n)', re.DOTALL)

    m_c = pat_c.search(html)
    m_b = pat_b.search(html)

    if not m_c or not m_b:
        return html, False

    line_c = m_c.group(1)
    line_b = m_b.group(1)

    # Si Contactos viene ANTES que Beneficios → swap necesario
    if m_c.start() < m_b.start():
        # Quitar beneficios primero (está después), para no desplazar índice de contactos
        html_tmp = html[:m_b.start()] + html[m_b.end():]
        # Buscar contactos de nuevo en el texto reducido
        m_c2 = pat_c.search(html_tmp)
        if m_c2:
            # Insertar beneficios justo antes de contactos
            html_tmp = html_tmp[:m_c2.start()] + line_b + html_tmp[m_c2.start():]
        return html_tmp, True

    return html, False


print("=== CORRECCIÓN 1: Orden sidebar ===")
for fname in C1_FILES:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content, changed = swap_beneficios_contactos(content)
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  OK: {fname}")
    else:
        print(f"  SKIP (ya ok o no encontrado): {fname}")


# ─────────────────────────────────────────────
# CORRECCIÓN 2 — Ícono de Beneficios: smiley → gift box
# ─────────────────────────────────────────────

SMILEY_PATH = 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2'
GIFT_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 12V22H4V12"/><path d="M22 7H2v5h20V7z"/><path d="M12 22V7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>'

def fix_beneficios_icon(html):
    """Reemplaza el SVG del nav-item de Beneficios (smiley) por el gift box."""
    pat = re.compile(
        r'(<a\s[^>]*admin-beneficios\.html[^>]*>.*?<span class="nav-icon">)(<svg[^>]*>.*?</svg>)(</span>)',
        re.DOTALL
    )
    def replacer(m):
        return m.group(1) + GIFT_SVG + m.group(3)
    new_html, n = pat.subn(replacer, html)
    return new_html, n > 0

print("\n=== CORRECCIÓN 2: Ícono Beneficios (gift box) ===")
admin_files = sorted([f for f in os.listdir(BASE) if f.startswith('admin-') and f.endswith('.html')])

for fname in admin_files:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if SMILEY_PATH not in content:
        print(f"  SKIP (no smiley): {fname}")
        continue
    new_content, changed = fix_beneficios_icon(content)
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  OK: {fname}")
    else:
        print(f"  WARN (smiley pero patrón no matcheó): {fname}")


# ─────────────────────────────────────────────
# CORRECCIÓN 5 — Ícono Comunicaciones: agregar segundo path
# ─────────────────────────────────────────────

COMM_INCOMPLETE = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 11 18-5v12L3 13v-2z"/></svg>'
COMM_COMPLETE   = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 11 18-5v12L3 13v-2z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/></svg>'

print("\n=== CORRECCIÓN 5: Ícono Comunicaciones (agregar 2do path) ===")
for fname in admin_files:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if COMM_INCOMPLETE not in content:
        print(f"  SKIP: {fname}")
        continue
    new_content = content.replace(COMM_INCOMPLETE, COMM_COMPLETE)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  OK: {fname}")


# ─────────────────────────────────────────────
# CORRECCIÓN 3 — Tab bar mobile: nueva tab bar consistente
# ─────────────────────────────────────────────

def make_tab_bar(active):
    """Genera el bloque completo de tab-bar con el tab activo marcado."""
    a = {
        'inicio': ' active' if active == 'inicio' else '',
        'comm':   ' active' if active == 'comm' else '',
        'chat':   ' active' if active == 'chat' else '',
        'dir':    ' active' if active == 'dir' else '',
        'perfil': ' active' if active == 'perfil' else '',
    }

    tab_inicio = f'''    <a href="mobile-modules.html" class="tab-item{a['inicio']}">
      <span class="tab-icon"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></span>
      Inicio
    </a>'''

    tab_comm = f'''    <a href="mobile-home.html" class="tab-item{a['comm']}">
      <span class="tab-icon"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 11 18-5v12L3 13v-2z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/></svg></span>
      Comunicaciones
    </a>'''

    tab_chat = f'''    <a href="mobile-dms.html" class="tab-item{a['chat']}" style="position:relative;">
      <span class="tab-icon" style="position:relative;display:inline-block;">
        <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        <span style="position:absolute;top:-4px;right:-6px;background:#E8735A;color:white;border-radius:50%;width:14px;height:14px;font-size:8px;font-weight:700;display:flex;align-items:center;justify-content:center;border:1.5px solid white;">3</span>
      </span>
      Chat
    </a>'''

    tab_dir = f'''    <a href="mobile-directorio.html" class="tab-item{a['dir']}">
      <span class="tab-icon"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>
      Directorio
    </a>'''

    tab_perfil = f'''    <a href="mobile-perfil.html" class="tab-item{a['perfil']}">
      <span class="tab-icon"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
      Perfil
    </a>'''

    return (
        '  <div class="tab-bar">\n' +
        tab_inicio + '\n' +
        tab_comm + '\n' +
        tab_chat + '\n' +
        tab_dir + '\n' +
        tab_perfil + '\n' +
        '  </div>'
    )

# Mapeo página → tab activo
ACTIVE_MAP = {
    'mobile-modules.html':       'inicio',
    'mobile-home.html':          'comm',
    'mobile-dms.html':           'chat',
    'mobile-directorio.html':    'dir',
    'mobile-perfil.html':        'perfil',
    'mobile-agenda.html':        'inicio',
    'mobile-ai.html':            'inicio',
    'mobile-beneficios.html':    'inicio',
    'mobile-board.html':         'inicio',
    'mobile-credencial.html':    'inicio',
    'mobile-foro.html':          'comm',
    'mobile-obras-sociales.html': 'inicio',
}

TAB_BAR_PAT = re.compile(r'(<div class="tab-bar">)(.*?)(</div>)', re.DOTALL)

print("\n=== CORRECCIÓN 3: Tab bar mobile ===")
for fname, active_tab in ACTIVE_MAP.items():
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f"  SKIP (no existe): {fname}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_tab_bar = make_tab_bar(active_tab)
    m = TAB_BAR_PAT.search(content)
    if m:
        new_content = content[:m.start()] + new_tab_bar + content[m.end():]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  OK ({active_tab}): {fname}")
    else:
        print(f"  WARN (no tab-bar encontrado): {fname}")


# ─────────────────────────────────────────────
# CORRECCIÓN 6 — Logo CMRB
# ─────────────────────────────────────────────

LOGO_IMG = '<img src="assets/logocmrb.jpg" alt="CMRB" style="height:36px;width:36px;border-radius:50%;object-fit:cover;border:1px solid #e2e8f0;">'

# Mobile: reemplazar solo páginas con app-header real
# Hay dos sub-estructuras:
#   A) <div style="display:flex;align-items:center;gap:7px;"><span ...>CMRB</span></div>
#      → mobile-home, mobile-modules, mobile-perfil
#   B) <div class="header-logo"><div class="logo-badge">CR</div><div>...CMRB...</div></div>
#      → mobile-directorio, mobile-beneficios
#   mobile-ai.html tiene status-bar con CMRB (no app-header) → tratar aparte
#   mobile-credencial.html tiene status-bar con CMRB como texto de tarjeta → no tocar

LOGO_MOBILE_REPLACEMENT = '''<div style="display:flex;align-items:center;gap:8px;">
  <div style="background:white;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center;overflow:hidden;flex-shrink:0;">
    <img src="assets/logocmrb.jpg" alt="CMRB" style="width:28px;height:28px;border-radius:50%;object-fit:cover;">
  </div>
  <span style="font-family:'Lora',serif;font-weight:700;font-size:17px;color:#fff;letter-spacing:2px;">CMRB</span>
</div>'''

# Patrón A: wrapper div con span CMRB
PAT_A = re.compile(
    r'<div style="display:flex;align-items:center;gap:\d+px;">\s*'
    r"<span style=\"font-family:'Lora'[^\"]*\">CMRB</span>\s*"
    r'</div>',
    re.DOTALL
)

# Patrón B: header-logo con logo-badge y logo-text-main CMRB
PAT_B = re.compile(
    r'<div class="header-logo">.*?</div>\s*</div>',
    re.DOTALL
)
# Más preciso para B:
PAT_B2 = re.compile(
    r'<div class="header-logo">\s*<div class="logo-badge">.*?</div>\s*<div>.*?</div>\s*</div>',
    re.DOTALL
)

print("\n=== CORRECCIÓN 6a: Logo en topbar admin ===")
for fname in admin_files:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    target = '<span class="topbar-title">'
    if LOGO_IMG in content:
        print(f"  SKIP (ya tiene logo): {fname}")
        continue
    if target not in content:
        print(f"  SKIP (no topbar-title): {fname}")
        continue

    new_content = content.replace(target, LOGO_IMG + '\n      ' + target, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  OK: {fname}")

print("\n=== CORRECCIÓN 6b: Logo en app-header mobile ===")

# Sub-grupo A: páginas con estructura simple (gap:7px / gap:8px + span CMRB)
GROUP_A = ['mobile-home.html', 'mobile-modules.html', 'mobile-perfil.html']
# Sub-grupo B: páginas con header-logo / logo-badge
GROUP_B = ['mobile-directorio.html', 'mobile-beneficios.html']
# mobile-ai.html: tiene status-bar con CMRB dentro de un span — buscar ese span
GROUP_AI = ['mobile-ai.html']

for fname in GROUP_A:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'logocmrb.jpg' in content:
        print(f"  SKIP (ya tiene logo): {fname}")
        continue
    new_content, n = PAT_A.subn(LOGO_MOBILE_REPLACEMENT, content)
    if n > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  OK (A): {fname}")
    else:
        print(f"  WARN (patrón A no matcheó): {fname}")

for fname in GROUP_B:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'logocmrb.jpg' in content:
        print(f"  SKIP (ya tiene logo): {fname}")
        continue
    new_content, n = PAT_B2.subn(LOGO_MOBILE_REPLACEMENT, content)
    if n > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  OK (B): {fname}")
    else:
        print(f"  WARN (patrón B no matcheó): {fname}")

# mobile-ai.html: el CMRB está en el status-bar en un span dentro de un div
# Estructura: <div style="display:flex;align-items:center;gap:8px;">
#               <span style="font-family:'Lora',...">CMRB</span>
#             </div>
for fname in GROUP_AI:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'logocmrb.jpg' in content:
        print(f"  SKIP (ya tiene logo): {fname}")
        continue
    new_content, n = PAT_A.subn(LOGO_MOBILE_REPLACEMENT, content)
    if n > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  OK (AI): {fname}")
    else:
        # Fallback: buscar el span solo
        pat_span = re.compile(r"<span style=\"font-family:'Lora'[^\"]*\">CMRB</span>")
        new_content, n2 = pat_span.subn(LOGO_MOBILE_REPLACEMENT, content, count=1)
        if n2 > 0:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  OK (AI fallback): {fname}")
        else:
            print(f"  WARN (no patrón para): {fname}")

print("\n=== TODAS LAS CORRECCIONES COMPLETADAS ===")
