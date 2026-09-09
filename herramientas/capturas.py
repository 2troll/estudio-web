#!/usr/bin/env python3
"""Capturas de los sitios de muestra, para la página del estudio.

Un portfolio que enseña una foto de archivo de un portátil no enseña nada. Lo
honesto es enseñar el trabajo: esto abre cada sitio en un Chrome sin ventana y
guarda la pantalla, en su idioma y a su ancho.

    python3 herramientas/capturas.py            # todas
    python3 herramientas/capturas.py nahar      # las que empiecen por «nahar»

Se captura la **copia local** del repositorio hermano, no la versión publicada.
Se ve igual y permite dos cosas que desde la red no se pueden hacer: forzar el
idioma sin depender de `localStorage`, y ocultar el aviso de cookies, que si no
tapa el tercio inferior de todas las capturas.

Sin dependencias: el Chrome instalado y el `sips` de macOS.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = Path(__file__).resolve().parent.parent
SITIOS = BASE.parent
SALIDA = BASE / "img"

# (archivo, repo, ruta, idioma, ancho, alto)
TOMAS = [
    ("nahar-es.jpg",    "nahar-solar", "inicio",       "es", 1440, 900),
    ("nahar-ar.jpg",    "nahar-solar", "numeros",      "ar", 1440, 900),
    ("nahar-movil.jpg", "nahar-solar", "servicios",    "es",  414, 820),
    ("bunn-es.jpg",     "bunn-cafe",   "cafes",        "es", 1440, 900),
    ("bunn-ar.jpg",     "bunn-cafe",   "preparar",     "ar", 1440, 900),
    ("bunn-movil.jpg",  "bunn-cafe",   "comprar",      "es",  414, 820),
    ("atlas-es.jpg",    "atlas-fisio", "tratamientos", "es", 1440, 900),
    ("atlas-ar.jpg",    "atlas-fisio", "recuperacion", "ar", 1440, 900),
    ("atlas-movil.jpg", "atlas-fisio", "contacto",     "es",  414, 820),
]


def preparar(repo: str, idioma: str, destino: Path) -> None:
    """Copia el sitio y lo deja arrancando en el idioma pedido, sin aviso de cookies."""
    origen = SITIOS / repo
    shutil.copytree(origen, destino, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git", "*.md"))
    html = (destino / "index.html").read_text(encoding="utf-8")

    # El arranque no se escribe igual en los tres sitios: unos ponen «var g = null;»
    # y otros «var g=null;». Si la sustitución falla hay que enterarse, no seguir
    # capturando en español y creer que se ha probado el árabe.
    html, n1 = re.subn(r"var g\s*=\s*null;", 'var g = "%s";' % idioma, html)
    html, n2 = re.subn(r'try\{\s*g\s*=\s*localStorage\.getItem\("[a-z]+_lang"\);\s*\}catch\(e\)\{\}',
                       "", html)
    if not (n1 and n2):
        raise SystemExit(f"{repo}: no se pudo forzar el idioma ({n1}, {n2})")

    # El aviso de cookies tapa el tercio inferior. En una captura sobra.
    html = html.replace("</head>", "<style>#ck{display:none!important}</style></head>", 1)
    (destino / "index.html").write_text(html, encoding="utf-8")


def capturar(archivo: str, repo: str, ruta: str, idioma: str, ancho: int, alto: int) -> None:
    tmp = Path(tempfile.mkdtemp())
    try:
        preparar(repo, idioma, tmp)
        SALIDA.mkdir(exist_ok=True)
        destino = SALIDA / archivo
        subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
             "--force-color-profile=srgb", f"--window-size={ancho},{alto}",
             "--virtual-time-budget=9000", f"--screenshot={destino}",
             f"file://{tmp}/index.html#/{ruta}"],
            capture_output=True, timeout=120)
        if not destino.exists():
            print(f"  FALLÓ {archivo}", file=sys.stderr)
            return
        if shutil.which("sips"):
            calidad = 68
            subprocess.run(["sips", "-s", "format", "jpeg",
                            "-s", "formatOptions", str(calidad), str(destino),
                            "--out", str(destino)], capture_output=True)
            while destino.stat().st_size > 200 * 1024 and calidad > 35:
                calidad -= 12
                subprocess.run(["sips", "-s", "formatOptions", str(calidad),
                                str(destino), "--out", str(destino)], capture_output=True)
        print(f"  {archivo}  {destino.stat().st_size // 1024} kB  ({repo}/{ruta}, {idioma})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    tomas = [t for t in TOMAS if not filtro or t[0].startswith(filtro)]
    if not tomas:
        sys.exit(f"nada que capturar con «{filtro}»")
    print(f"capturando {len(tomas)}:")
    for t in tomas:
        capturar(*t)


if __name__ == "__main__":
    main()
