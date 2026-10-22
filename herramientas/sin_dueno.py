# -*- coding: utf-8 -*-
"""Saca a una carpeta las fotos que no reclama ningun animal del Excel.

Es para mandarselas a Carla y que diga de quien son. El nombre del fichero
lleva delante el zip del que sale, para que ella se situe.
"""
import os, re, json, zipfile, shutil, unicodedata

RAIZ = r"C:\Users\desca\OneDrive\Desktop\loveanimalsbcn"
IMGS = os.path.join(RAIZ, "docs", "img_loveanimalsbcn")
DESTINO = os.path.join(IMGS, "_sin_dueno")
AQUI = os.path.dirname(os.path.abspath(__file__))

# zips que no son de animales: son las fotos de producto para la tienda
NO_SON_ANIMALES = ("Fotos de productos", "PRODUCTOS LAB")


def corto(zn):
    """El nombre del zip, limpio, para que Carla sepa de que tanda sale cada foto."""
    s = re.sub(r"(?i)\.zip$", "", zn)
    s = re.sub(r"(?i)^fotos?\s+", "", s).strip()
    s = re.sub(r"(?i)\s*web\s*$", "", s).strip()
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").upper() or "SUELTAS"


def main():
    asig = json.load(open(os.path.join(AQUI, "asignacion.json"), encoding="utf-8"))
    usadas = set()
    for fs in asig.values():
        usadas.update(fs)

    if os.path.isdir(DESTINO):
        shutil.rmtree(DESTINO)
    os.makedirs(DESTINO)

    n = 0
    for z in sorted(os.listdir(IMGS)):
        if not z.lower().endswith(".zip") or z.startswith(NO_SON_ANIMALES):
            continue
        with zipfile.ZipFile(os.path.join(IMGS, z)) as f:
            for i in f.infolist():
                base = os.path.basename(i.filename)
                if i.is_dir() or base.startswith("._") or "__MACOSX" in i.filename:
                    continue
                if "%s|%s" % (z, i.filename) in usadas:
                    continue
                nombre = "%s__%s" % (corto(z), unicodedata.normalize("NFC", base))
                with f.open(i) as origen, open(os.path.join(DESTINO, nombre), "wb") as salida:
                    shutil.copyfileobj(origen, salida)
                n += 1
    print("%d fotos sin dueño -> %s" % (n, DESTINO))
    por_zip = {}
    for x in sorted(os.listdir(DESTINO)):
        por_zip.setdefault(x.split("__")[0], []).append(x)
    for k, v in sorted(por_zip.items()):
        print("   %-28s %3d" % (k, len(v)))


if __name__ == "__main__":
    main()
