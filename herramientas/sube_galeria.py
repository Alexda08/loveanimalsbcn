# -*- coding: utf-8 -*-
"""Sube a la tienda las fotos de la franja de la tienda solidaria.

Carla pidió «fotos chulas de gente con la ropa o productos, que vayan
cambiando». Vienen de dos zips suyos: el catálogo cuidado (PRODUCTOS LAB) y las
de gente real que ha comprado, que venían mezcladas en FOTOS WEB QUE FALTAN.

Se suben con nombre `tienda-NN` para poder referenciarlas desde la plantilla
como `shopify://shop_images/tienda-NN.ext`, y con texto alternativo escrito a
mano: son fotos con personas y animales, no vale un alt genérico.

Ojo al escribir la plantilla: **Shopify renombra `.jpeg` a `.jpg`** al guardar
el fichero, así que la referencia hay que sacarla de los nombres que devuelve la
tienda, no de los que se subieron. Si no coincide, el bloque se queda en blanco
y la foto no sale, sin ningún error.

    python sube_galeria.py mirar
    python sube_galeria.py subir     (se puede relanzar: no duplica)
"""
import os, sys, json, time, zipfile, mimetypes, unicodedata
import requests

RAIZ = r"C:\Users\desca\OneDrive\Desktop\loveanimalsbcn"
IMGS = os.path.join(RAIZ, "docs", "img_loveanimalsbcn")
AQUI = os.path.dirname(os.path.abspath(__file__))
HECHAS = os.path.join(AQUI, "galeria.json")

API = "https://loveanimalsbcn.myshopify.com/admin/api/2026-01/graphql.json"
TOKEN = os.environ.get("LA_TOKEN_REAL", "")

CATALOGO = "PRODUCTOS LAB CATÁLOGO BONITO.zip"
GENTE = "FOTOS WEB QUE FALTAN.zip"

# (zip, fichero sin extensión, texto alternativo). El orden es el de la cinta:
# se alterna catálogo y gente para que no salgan seguidas todas las de estudio.
FOTOS = [
    (CATALOGO, "032FA66A-2B5B-4785-AD43-0DCA92185842", "Taza «Si tú me dices miau lo dejo todo» junto a un gato atigrado"),
    (GENTE, "055ba628-ab0a-4dac-a619-551cffb28565", "Una chica con la camiseta «El amor no se compra» sentada con su perro en un mirador"),
    (CATALOGO, "0BA818EB-EFBC-466A-B048-04531AF9D7CC", "Tres bodis de bebé de la tienda solidaria tendidos en una cuerda"),
    (GENTE, "21656db7-2583-4c7c-bd85-beeefdeeac24", "Un chico de espaldas con la camiseta «Stop Ley PPP» y un gato blanco a su lado"),
    (CATALOGO, "12A7DD94-69B6-4D97-B16E-9C088DA4125B", "Tres fundas de móvil de la asociación, con un perro y un gato detrás"),
    (GENTE, "29DC6F1C-F3B1-4673-97E4-0FAD32F5933C", "Una chica con la sudadera «Stop Ley PPP» y su perro, al atardecer"),
    (CATALOGO, "AA809BE8-8EF2-4F20-83E4-BC00F7BC2C19", "Totebag negra «El amor no se compra» colgada junto a unas plantas"),
    (GENTE, "503E5AEE-F3CF-48BB-9C17-A622E968641E", "Una chica de espaldas con la camiseta «Stop Ley PPP» abrazando a su perro en el campo"),
    (CATALOGO, "C764A91E-5731-4C34-9344-DB2805C3619F", "Taza «El amor no se compra» apoyada junto a un perro tumbado"),
    (GENTE, "554e6baa-3b85-4a45-b87c-3437d3247f4b", "Una mujer con la camiseta «Si tú me dices miau» sujetando a sus dos gatos"),
    (CATALOGO, "A249AF04-9670-4953-A089-9F00D2BCF0D0", "Llaveros redondos con el logo de la asociación"),
    (GENTE, "9DFFDFD4-4F08-49B8-9B0B-00C7775EC3CA", "Una chica en la playa con su perro blanco, los dos con ropa de la tienda"),
    (CATALOGO, "77A56AC5-5837-40F9-AC76-E7C295B55DD2", "Dos mochilas de cuerdas con el logo, tendidas al sol"),
    (GENTE, "IMG_6578", "Una mujer con la sudadera «El amor no se compra» agachada junto a su perro"),
    (CATALOGO, "BC8B0795-B673-44B8-A52E-5B0923A86D3B", "Lámina de adopción enmarcada, con un gato naranja al lado"),
    (GENTE, "a23a1df8-91fd-4bcd-8ff3-8dbdc1082e74", "Una chica con camiseta de la asociación y su perro blanco"),
    (CATALOGO, "8130FCA9-2D3F-4906-8FAA-98D08EE48B74", "Punto de libro con las fotos de dos perros, sobre un libro abierto"),
    (GENTE, "image0", "Una chica de espaldas en la playa, con la camiseta «Stop Ley PPP» y su perro"),
    (CATALOGO, "E85D6BB2-3A55-48D6-86D7-7FDCB0F2D44B", "Dos tazas, «Yo no soy peligroso» y «Stop Ley PPP», con un perro detrás"),
    (GENTE, "image1", "Una chica agachada en el campo con su perro, con sudadera de la asociación"),
    (CATALOGO, "A89BA88C-E7E1-4988-AA30-B9A2B2901053", "Sudadera blanca «Adoptar es vida» colgada de una escalera de madera"),
    (GENTE, "InShot_20200520_203238749", "Una chica de espaldas en un balcón, con sudadera de la asociación y su perro"),
    (CATALOGO, "CF04D578-96C1-4A1A-B089-7D23B160D9A4", "Bolígrafo con huellas, sobre un cuaderno"),
    (GENTE, "IMG_3120", "Camisetas y sudaderas de la tienda solidaria tendidas al sol"),
    (CATALOGO, "B9626DE7-BFBD-4C79-BE00-F4CAB061A2AB", "Jabón artesanal de la asociación en el lavabo"),
    (CATALOGO, "F4A525F2-0FDB-4698-A017-0702217BD958", "Jabones de colores envueltos, listos para regalar"),
    (CATALOGO, "005afbc2-6cdc-4de4-95b1-fe8c05c7bd06", "Jabón de detalle de boda, con la ficha de un animal en adopción"),
    (CATALOGO, "F2604C46-42BB-4DDF-9638-A7CC78C46E7C", "Camiseta negra del día de la madre, tendida en una cuerda"),
]

M_STAGED = """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
  stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }"""
M_FILE = """mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){
  files{ id fileStatus } userErrors{ field message } } }"""
Q_ESTADO = """query($ids:[ID!]!){ nodes(ids:$ids){ ... on MediaImage { id fileStatus } } }"""


def gql(consulta, variables=None, intentos=5):
    for n in range(intentos):
        r = requests.post(API, json={"query": consulta, "variables": variables or {}},
                          headers={"X-Shopify-Access-Token": TOKEN}, timeout=180)
        if r.status_code in (429, 500, 502, 503):
            time.sleep(2 * (n + 1)); continue
        d = r.json()
        if any(e.get("extensions", {}).get("code") == "THROTTLED" for e in d.get("errors", []) or []):
            time.sleep(3); continue
        if d.get("errors"):
            raise SystemExit("GraphQL: %s" % json.dumps(d["errors"], ensure_ascii=False)[:600])
        return d["data"]
    raise SystemExit("la API no responde")


def dentro(zn):
    """clave en minusculas -> (ruta dentro del zip, bytes)"""
    out = {}
    with zipfile.ZipFile(os.path.join(IMGS, zn)) as f:
        for i in f.infolist():
            b = os.path.basename(i.filename)
            if i.is_dir() or b.startswith("._") or "__MACOSX" in i.filename:
                continue
            out[unicodedata.normalize("NFC", os.path.splitext(b)[0]).lower()] = (i.filename, i.file_size)
    return out


def plan():
    indices, pendientes = {}, []
    for n, (zn, fichero, alt) in enumerate(FOTOS, 1):
        if zn not in indices:
            indices[zn] = dentro(zn)
        clave = unicodedata.normalize("NFC", fichero).lower()
        if clave not in indices[zn]:
            print("   !! no esta  %-40s en %s" % (fichero[:40], zn))
            continue
        ruta, peso = indices[zn][clave]
        nombre = "tienda-%02d%s" % (n, os.path.splitext(ruta)[1].lower())
        pendientes.append((nombre, zn, ruta, alt, peso))
    return pendientes


def main():
    if not TOKEN:
        raise SystemExit("falta LA_TOKEN_REAL en el entorno")
    hazlo = len(sys.argv) > 1 and sys.argv[1] == "subir"
    hechas = json.load(open(HECHAS, encoding="utf-8")) if os.path.exists(HECHAS) else {}
    todas = plan()
    quedan = [p for p in todas if p[0] not in hechas]

    print("   %d en la cinta | ya subidas: %d | quedan: %d (%.0f MB)"
          % (len(todas), len(hechas), len(quedan), sum(p[4] for p in quedan) / 1e6))
    if not hazlo:
        for nombre, zn, ruta, alt, _ in todas:
            print("      %-16s %s" % (nombre, alt[:74]))
        return
    if not quedan:
        print("   nada que subir"); return

    for i in range(0, len(quedan), 8):
        lote = quedan[i:i + 8]
        entrada, contenido = [], {}
        for nombre, zn, ruta, alt, _ in lote:
            with zipfile.ZipFile(os.path.join(IMGS, zn)) as f:
                datos = f.read(ruta)
            contenido[nombre] = datos
            entrada.append({"filename": nombre,
                            "mimeType": mimetypes.guess_type(nombre)[0] or "image/jpeg",
                            "resource": "IMAGE", "httpMethod": "POST",
                            "fileSize": str(len(datos))})
        d = gql(M_STAGED, {"input": entrada})["stagedUploadsCreate"]
        if d["userErrors"]:
            raise SystemExit("stagedUploads: %s" % d["userErrors"])
        ficheros = []
        for (nombre, zn, ruta, alt, _), destino in zip(lote, d["stagedTargets"]):
            campos = [(p["name"], p["value"]) for p in destino["parameters"]]
            r = requests.post(destino["url"], data=campos,
                              files={"file": (nombre, contenido[nombre])}, timeout=300)
            if r.status_code not in (200, 201, 204):
                raise SystemExit("subida de %s: %s" % (nombre, r.status_code))
            ficheros.append({"originalSource": destino["resourceUrl"],
                             "contentType": "IMAGE", "alt": alt})
        d = gql(M_FILE, {"files": ficheros})["fileCreate"]
        if d["userErrors"]:
            raise SystemExit("fileCreate: %s" % d["userErrors"])
        gids = [f["id"] for f in d["files"]]
        pend = list(gids)
        for _ in range(40):
            nodos = gql(Q_ESTADO, {"ids": pend})["nodes"]
            if any(n and n["fileStatus"] == "FAILED" for n in nodos):
                raise SystemExit("alguna fallo: %s" % nodos)
            pend = [n["id"] for n in nodos if n and n["fileStatus"] != "READY"]
            if not pend:
                break
            time.sleep(3)
        for (nombre, *_), gid in zip(lote, gids):
            hechas[nombre] = gid
            print("   subida      %s" % nombre)
        with open(HECHAS, "w", encoding="utf-8") as f:
            json.dump(hechas, f, ensure_ascii=False, indent=1)
    print("   %d fotos en la tienda -> %s" % (len(hechas), HECHAS))


if __name__ == "__main__":
    main()
