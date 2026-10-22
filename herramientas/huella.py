# -*- coding: utf-8 -*-
"""Huella visual de una foto (dHash de 64 bits) para encontrar repetidas aunque
cambie el nombre, el tamaño o la compresión."""
from PIL import Image, ImageOps

def dhash(im, tam=8):
    im = ImageOps.exif_transpose(im).convert("L").resize((tam + 1, tam), Image.LANCZOS)
    px = list(im.getdata())
    bits = 0
    for f in range(tam):
        for c in range(tam):
            i = f * (tam + 1) + c
            bits = (bits << 1) | (1 if px[i] > px[i + 1] else 0)
    return "%016x" % bits

def abre_rapido(fp):
    im = Image.open(fp)
    try:
        im.draft("L", (320, 320))
    except Exception:
        pass
    return im

def distancia(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count("1")
