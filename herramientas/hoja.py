# -*- coding: utf-8 -*-
"""Monta hojas de contactos de las fotos sin dueño, para poder mirarlas de golpe."""
import os, sys, glob, math
from PIL import Image, ImageDraw

ORIGEN = r"C:\Users\desca\OneDrive\Desktop\loveanimalsbcn\docs\img_loveanimalsbcn\_sin_dueno\2-para-la-tienda"


def hoja(ficheros, salida, cols=7, ancho=300, alto=300, etiqueta=lambda p, n: str(n)):
    filas = math.ceil(len(ficheros) / cols)
    h = Image.new("RGB", (cols * ancho, filas * (alto + 22)), "white")
    d = ImageDraw.Draw(h)
    for n, p in enumerate(ficheros):
        im = Image.open(p).convert("RGB")
        im.thumbnail((ancho - 6, alto - 6))
        x = (n % cols) * ancho + (ancho - im.width) // 2
        y = (n // cols) * (alto + 22) + 20
        h.paste(im, (x, y))
        d.text(((n % cols) * ancho + 4, (n // cols) * (alto + 22) + 5), etiqueta(p, n + 1), fill="black")
    h.save(salida, quality=80)
    return salida, h.size


if __name__ == "__main__":
    pref = sys.argv[1]
    fs = sorted(glob.glob(os.path.join(ORIGEN, pref + "*")))
    trozo = int(sys.argv[2]) if len(sys.argv) > 2 else 28
    for i in range(0, len(fs), trozo):
        s, tam = hoja(fs[i:i + trozo], "hoja_%s_%d.jpg" % (pref.strip("_").lower(), i // trozo + 1),
                      etiqueta=lambda p, n, off=i: "%d %s" % (n + off, os.path.basename(p).split("__")[1][:16]))
        print(s, tam, os.path.getsize(s) // 1024, "KB")
