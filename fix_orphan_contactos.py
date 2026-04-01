#!/usr/bin/env python3
"""
Fix orphan lines left by the nav-contactos deletion.
After the first script ran, the <a href="admin-contactos.html"> line was removed
but the inner lines (<span...> Contactos\n    </a>) were left orphaned.
This script removes those orphan fragments from all admin files.
"""

import os
import re

BASE = "/Users/lucas/projects/mocks-colmedplatform"

ADMIN_FILES = [
    "admin-agenda.html",
    "admin-beneficios.html",
    "admin-board.html",
    "admin-communications.html",
    # "admin-contactos.html",  # skipped — keep its own nav item
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


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# The orphan pattern: a <span class="nav-icon">...SVG... Contactos</span>\n    </a>
# that appears without a preceding <a href="admin-contactos.html">
# Pattern: line with <span class="nav-icon">...line x1="19"...Contactos
# followed by line with just "    </a>"
ORPHAN_PATTERN = re.compile(
    r'\n\s+<span class="nav-icon"><svg[^<]*(?:<[^/][^>]*>[^<]*</[^>]+>|<[^>]+/>)*[^<]*</svg></span> Contactos\n\s+</a>',
    re.DOTALL
)

# More targeted: match the exact SVG for the contacts icon (line x1="19"...)
# followed by " Contactos\n    </a>"
ORPHAN_CONTACTS_NAV = re.compile(
    r'\n[ \t]*<span class="nav-icon"><svg[^>]*>(?:<[^>]*>)*?<line x1="19" y1="8"[^>]*/><line x1="19" y1="11"[^>]*/><line x1="19" y1="14"[^>]*/></svg></span> Contactos\n[ \t]*</a>',
    re.DOTALL
)

for filename in ADMIN_FILES:
    path = os.path.join(BASE, filename)
    content = read(path)
    original = content

    # Remove orphan fragment
    new_content = ORPHAN_CONTACTS_NAV.sub('', content)

    if new_content != original:
        write(path, new_content)
        print(f"  [FIXED] {filename}")
    else:
        # Try broader pattern
        new_content2 = ORPHAN_PATTERN.sub('', content)
        if new_content2 != original:
            write(path, new_content2)
            print(f"  [FIXED-broad] {filename}")
        else:
            print(f"  [--] {filename} — no orphan found (may already be clean)")

print("\nDone.")
