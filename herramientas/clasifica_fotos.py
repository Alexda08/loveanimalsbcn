# -*- coding: utf-8 -*-
# OJO (22-10-2026): reconstruido del historial de trabajo, pero le faltan los últimos
# retoques de la parte que reparte las fotos en las subcarpetas de _sin_dueno: la versión final exacta no quedó registrada. Funciona como
# referencia del método; antes de relanzarlo, léelo entero y compáralo con docs/../herramientas/README.md.
"""Pone nombre a las fotos que no usa nadie, hasta donde se pueda saber.

Una foto sin dueño puede ser cuatro cosas, y conviene no mezclarlas:

  1. de un animal que SÍ está en el Excel pero se ha quedado fuera (adoptado,
     fallecido o marcado «NO PONERLO»): esas ya tienen nombre, no hay que
     preguntar nada
  2. una toma de más de un animal que sí está publicado: el Excel solo nombraba
     algunas de sus fotos
  3. de la tienda solidaria: gente con la ropa, prendas tendidas, mockups
  4. sin pista ninguna: las candidatas para los cuatro gatos que faltan

Solo las del grupo 4 hay que preguntárselas a Carla.
"""
import os, re, sys, json, glob, zipfile, unicodedata, collections
import openpyxl

RAIZ = r"C:\Users\desca\OneDrive\Desktop\loveanimalsbcn"
XLSX = os.path.join(RAIZ, "docs", "Love Animals BCN - fichas de los animales.xlsx")
IMGS = os.path.join(RAIZ, "docs", "img_loveanimalsbcn")
AQUI = os.path.dirname(os.path.abspath(__file__))

# zips que no son de animales, son el material de la tienda
DE_TIENDA = ("Fotos de productos", "PRODUCTOS LAB")


def nfc(s):
    return unicodedata.normalize("NFC", str(s)).strip().lower()


def laxa(k):
    return k.replace("-", "").replace("o", "0").replace("i", "1").replace("l", "1").replace("s", "5")


def del_excel():
    """clave de foto -> [(fila, nombre, se_publica)] mirando TODAS las filas."""
    ws = openpyxl.load_workbook(XLSX, data_only=True)["Animales"]
    fichas = json.load(open(os.path.join(AQUI, "fichas.json"), encoding="utf-8"))
    publicados = {a["fila"] for a in fichas["animales"]}
    motivo = {f["fila"]: f["nota"] for f in fichas["fuera"]}
    de = collections.defaultdict(list)
    for r in range(3, ws.max_row + 1):
        nombre = ws.cell(r, 2).value
        celda = ws.cell(r, 17).value
        if not nombre or not celda:
            continue
        for t in re.split(r"[,;\n]", str(celda)):
            t = t.strip()
            if not t:
                continue
            k = nfc(os.path.splitext(t)[0])
            k = re.sub(r"(jpe?g|png|heic)$", "", k) or k
            de[k].append((r, str(nombre).strip(), r in publicados, motivo.get(r, "")))
            de[laxa(k)].append((r, str(nombre).strip(), r in publicados, motivo.get(r, "")))
    return de


def huerfanas():
    """[(zip, ruta, basename)] de todo lo que no reclama ningun animal publicado."""
    asig = json.load(open(os.path.join(AQUI, "asignacion.json"), encoding="utf-8"))
    usadas = set()
    for fs in asig.values():
        usadas.update(fs)
    # las portadas van por otro camino (sube_portadas.py), no por la asignacion
    port = os.path.join(AQUI, "portadas.json")
    puestas = set()
    if os.path.exists(port):
        import sube_portadas
        hechas = json.load(open(port, encoding="utf-8"))
        puestas = {nfc(f) for h, (f, _) in sube_portadas.PORTADAS.items() if h in hechas}
    out = []
    for z in sorted(glob.glob(os.path.join(IMGS, "*.zip"))):
        zn = os.path.basename(z)
        with zipfile.ZipFile(z) as f:
            for i in f.infolist():
                b = os.path.basename(i.filename)
                if i.is_dir() or b.startswith("._") or "__MACOSX" in i.filename:
                    continue
                if "%s|%s" % (zn, i.filename) in usadas:
                    continue
                if zn == "PORTADAS.zip" and nfc(os.path.splitext(b)[0]) in puestas:
                    continue
                out.append((zn, i.filename, unicodedata.normalize("NFC", b)))
    return out


def firmas():
    """nombre de fichero -> {zips donde aparece}, mirando TODOS los zips.

    No vale el md5: la misma foto sale del zip de gatos y del de «que faltan»
    con 322 bytes de diferencia, que son los metadatos de la reexportacion.
    """
    donde = collections.defaultdict(set)
    for z in sorted(glob.glob(os.path.join(IMGS, "*.zip"))):
        zn = os.path.basename(z)
        with zipfile.ZipFile(z) as f:
            for i in f.infolist():
                b = os.path.basename(i.filename)
                if i.is_dir() or b.startswith("._") or "__MACOSX" in i.filename:
                    continue
                donde[nfc(b)].add(zn)
    return donde


def main():
    de = del_excel()
    fuera = huerfanas()
    donde_esta = firmas()
    grupos = collections.defaultdict(list)
    vistas = set()
    for zn, ruta, base in fuera:
        k = nfc(os.path.splitext(base)[0])
        if k in vistas:            # la misma foto sale en dos zips
            continue
        vistas.add(k)
        if zn.startswith(DE_TIENDA):
            grupos["3. material de la tienda (zip de productos)"].append((zn, base, ""))
            continue
        if os.path.splitext(base)[1].lower() not in (".jpg", ".jpeg", ".png", ".heic"):
            grupos["5. no son fotos (vídeos)"].append((zn, base, ""))
            continue
        duenos = de.get(k) or de.get(laxa(k)) or []
        if not duenos:
            # el zip «que faltan» trae mezcladas las fotos de los gatos que
            # quedaban y el material de la tienda. Las de gato estan tambien en
            # el zip de gatos, byte a byte: eso las separa sin tener que mirarlas
            donde = donde_esta.get(nfc(base), set())
            de_animales = {z for z in donde
                           if not z.startswith(DE_TIENDA)
                           and z not in ("FOTOS WEB QUE FALTAN.zip", "PORTADAS.zip", zn)}
            if zn == "FOTOS WEB QUE FALTAN.zip" and not de_animales:
                grupos["3. material de la tienda (venia mezclado en «que faltan»)"].append((zn, base, ""))
            else:
                otros = " · tambien en %s" % ", ".join(sorted(de_animales)) if de_animales else ""
                grupos["4. sin pista: hay que preguntar"].append((zn, base, otros))
        elif any(pub for _, _, pub, _ in duenos):
            quien = ", ".join(sorted({n for _, n, pub, _ in duenos if pub}))
            grupos["2. toma de más de un animal ya publicado"].append((zn, base, quien))
        else:
            quien = ", ".join("%s (%s)" % (n, m or "fuera") for _, n, _, m in duenos)
            grupos["1. de un animal que se quedó fuera"].append((zn, base, quien))

    for g in sorted(grupos):
        print("\n== %s == %d" % (g, len(grupos[g])))
        for zn, base, quien in sorted(grupos[g], key=lambda x: (x[0], x[1])):
            print("   %-30s %-46s %s" % (zn[:30], base[:46], quien[:44]))
    print("\ntotal sin dueño:", len(fuera))

    if len(sys.argv) > 1 and sys.argv[1] == "reparte":
        reparte(grupos)


CARPETA = {
    "1.": "3-ya-tienen-nombre",
    "2.": "3-ya-tienen-nombre",
    "3.": "2-para-la-tienda",
    "4.": "1-de-quien-es",
    "5.": "4-videos",
}

LEEME = """Fotos que no usa ninguna ficha de la web, ordenadas por lo que hay que hacer
con cada una. Sale de clasifica_fotos.py y se puede volver a generar.

1-de-quien-es/      lo unico que hay que mirar. Son fotos de animales que el
                    Excel no reclama: cuatro gatos se quedaron sin subir porque
                    su casilla «Fotos» vino vacia. Con escribir el nombre del
                    fichero en el Excel, entran solas.
2-para-la-tienda/   gente con la ropa, prendas tendidas y fotos de producto.
                    Nada que ver con las fichas: son para la tienda solidaria.
3-ya-tienen-nombre/ sabemos de quien son: o el animal se ha ido (adoptado,
                    fallecido, sin publicar) o es una toma de mas de uno que ya
                    esta en la web. El nombre del fichero lo dice.
4-videos/           no son fotos; la galeria solo admite imagenes.
"""


def corto(zn):
    s = re.sub(r"(?i)\.zip$", "", zn)
    s = re.sub(r"(?i)^fotos?\s+", "", s).strip()
    s = re.sub(r"(?i)\s*web\s*$", "", s).strip()
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").upper() or "SUELTAS"


def reparte(grupos):
    """Deja cada foto en la carpeta de lo que hay que hacer con ella."""
    import shutil
    destino = os.path.join(IMGS, "_sin_dueno")
    if os.path.isdir(destino):
        shutil.rmtree(destino)
    abiertos, cuenta = {}, collections.Counter()
    for g, filas in grupos.items():
        sub = os.path.join(destino, CARPETA[g[:2]])
        os.makedirs(sub, exist_ok=True)
        for zn, base, quien in filas:
            if zn not in abiertos:
                abiertos[zn] = zipfile.ZipFile(os.path.join(IMGS, zn))
            ruta = next(i.filename for i in abiertos[zn].infolist()
                        if nfc(os.path.basename(i.filename)) == nfc(base))
            etiqueta = re.sub(r"[^\w.() -]+", "_", quien)[:40] + "__" if quien else ""
            nombre = "%s%s__%s" % (etiqueta, corto(zn), base)
            with abiertos[zn].open(ruta) as o, open(os.path.join(sub, nombre), "wb") as f:
                shutil.copyfileobj(o, f)
            cuenta[CARPETA[g[:2]]] += 1
    with open(os.path.join(destino, "LEEME.txt"), "w", encoding="utf-8") as f:
        f.write(LEEME)
    print()
    for k, n in sorted(cuenta.items()):
        print("   %-22s %3d fotos" % (k, n))
    print("   ->", destino)

    if len(sys.argv) > 1 and sys.argv[1] == "reparte":
        reparte(grupos)


CARPETA = {
    "1.": "3-ya-tienen-nombre",
    "2.": "3-ya-tienen-nombre",
    "3.": "2-para-la-tienda",
    "4.": "1-de-quien-es",
    "5.": "4-videos",
}

LEEME = """Fotos que no usa ninguna ficha de la web, ordenadas por lo que hay que hacer
con cada una. Generado por clasifica_fotos.py: se puede volver a generar.

1-de-quien-es/      lo unico que hay que mirar. Son fotos de animales que el
                    Excel no reclama: cuatro gatos se quedaron sin subir porque
                    su casilla «Fotos» vino vacia. Con poner el nombre del
                    fichero en el Excel, entran solas.
2-para-la-tienda/   gente con la ropa, prendas y fotos de producto. Nada que ver
                    con las fichas; son para la parte de tienda solidaria.
3-ya-tienen-nombre/ sabemos de quien son: o el animal se ha ido (adoptado,
                    fallecido, sin publicar) o es una toma de mas de uno que ya
                    esta en la web. El nombre del fichero lo dice.
4-videos/           no son fotos, la galeria solo admite imagenes.
"""


def reparte(grupos):
    """Deja las fotos en carpetas segun lo que haya que hacer con cada una."""
    import shutil
    destino = os.path.join(IMGS, "_sin_dueno")
    if os.path.isdir(destino):
        shutil.rmtree(destino)
    abiertos = {}
    cuenta = collections.Counter()
    for g, filas in grupos.items():
        sub = os.path.join(destino, CARPETA[g[:2]])
        os.makedirs(sub, exist_ok=True)
        for zn, base, quien in filas:
            if zn not in abiertos:
                abiertos[zn] = zipfile.ZipFile(os.path.join(IMGS, zn))
            ruta = next(i.filename for i in abiertos[zn].infolist()
                        if os.path.basename(i.filename) == base
                        or nfc(os.path.basename(i.filename)) == nfc(base))
            etiqueta = re.sub(r"[^\w.() -]+", "_", quien)[:40] + "__" if quien else ""
            nombre = "%s%s__%s" % (etiqueta, corto(zn), base)
            with abiertos[zn].open(ruta) as o, open(os.path.join(sub, nombre), "wb") as f:
                shutil.copyfileobj(o, f)
            cuenta[CARPETA[g[:2]]] += 1
    with open(os.path.join(destino, "LEEME.txt"), "w", encoding="utf-8") as f:
        f.write(LEEME)
    print()
    for k, n in sorted(cuenta.items()):
        print("   %-22s %3d fotos" % (k, n))
    print("   ->", destino)


def corto(zn):
    s = re.sub(r"(?i)\.zip$", "", zn)
    s = re.sub(r"(?i)^fotos?\s+", "", s).strip()
    s = re.sub(r"(?i)\s*web\s*$", "", s).strip()
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").upper() or "SUELTAS"

if __name__ == "__main__":
    main()
