# -*- coding: utf-8 -*-
"""Saca las fotos de los zips y las sube a los Ficheros de la tienda real.

Guarda el resultado en fotos.json (clave de foto -> GID) para poder cortar y
seguir por donde iba. El token entra por la variable de entorno LA_TOKEN_REAL:
nunca se escribe en disco.

    python sube_fotos.py prueba     una sola foto, para ver que el circuito va
    python sube_fotos.py subir      las 445 (se puede relanzar sin duplicar)
    python sube_fotos.py estado     cuántas quedan
"""
import os, sys, json, time, zipfile, glob, unicodedata, collections, mimetypes
import requests

RAIZ = r"C:\Users\desca\OneDrive\Desktop\loveanimalsbcn"
IMGS = os.path.join(RAIZ, "docs", "img_loveanimalsbcn")
AQUI = os.path.dirname(os.path.abspath(__file__))
FICHAS = os.path.join(AQUI, "fichas.json")
FOTOS = os.path.join(AQUI, "fotos.json")

TIENDA = "loveanimalsbcn.myshopify.com"
API = "https://%s/admin/api/2026-01/graphql.json" % TIENDA
TOKEN = os.environ.get("LA_TOKEN_REAL", "")

# cada álbum se rellenó desde un zip concreto; sirve para deshacer los empates
# cuando dos animales distintos tienen una foto con el mismo nombre
ZIP_DE_ALBUM = {
    "GATOS": "FOTOS GATOS WEB.zip",
    "ABUELOS": "FOTOS PERROS ABUELOS WEB.zip",
    "LOS MÁS VETERANOS": "FOTOS LOS + VETERANOS WEB .zip",
    "DESDE 2021 ESPERANDO FAMILIA": "FOTOS PERROS 2021 WEB.zip",
    "DESDE 2022 ESPERANDO FAMILIA": "FOTOS PERRROS 2022.zip",
    "DESDE 2023 ESPERANDO FAMILIA": "FOTOS PERROS 2023.zip",
    "DESDE 2024 ESPERANDO FAMILIA": "FOTOS PERROS 2024 Y NUEVOS.zip",
}


def nfc(s):
    return unicodedata.normalize("NFC", str(s)).strip().lower()


def gql(consulta, variables=None, intentos=5):
    for n in range(intentos):
        r = requests.post(API, json={"query": consulta, "variables": variables or {}},
                          headers={"X-Shopify-Access-Token": TOKEN}, timeout=120)
        if r.status_code in (429, 500, 502, 503):
            time.sleep(2 * (n + 1)); continue
        d = r.json()
        if any(e.get("extensions", {}).get("code") == "THROTTLED" for e in d.get("errors", []) or []):
            time.sleep(3); continue
        if d.get("errors"):
            raise SystemExit("GraphQL: %s" % json.dumps(d["errors"], ensure_ascii=False)[:600])
        coste = d.get("extensions", {}).get("cost", {}).get("throttleStatus", {})
        if coste.get("currentlyAvailable", 999) < 250:
            time.sleep(1)
        return d["data"]
    raise SystemExit("la API no responde tras %d intentos" % intentos)


# ------------------------------------------------------------------ inventario
def inventario():
    """clave -> [(zip, ruta dentro del zip, bytes)]  (los sueltos van con zip=None)"""
    idx = collections.defaultdict(list)
    for z in sorted(glob.glob(os.path.join(IMGS, "*.zip"))):
        with zipfile.ZipFile(z) as f:
            for i in f.infolist():
                b = os.path.basename(i.filename)
                if i.is_dir() or b.startswith("._") or "__MACOSX" in i.filename:
                    continue
                idx[nfc(os.path.splitext(b)[0])].append((os.path.basename(z), i.filename, i.file_size))
    for p in glob.glob(os.path.join(IMGS, "*.*")):
        if os.path.splitext(p)[1].lower() in (".png", ".jpg", ".jpeg"):
            idx[nfc(os.path.splitext(os.path.basename(p))[0])].append((None, os.path.basename(p), os.path.getsize(p)))
    return idx


def reparte(animales, idx):
    """Decide qué fichero concreto le toca a cada animal y con qué nombre se sube.

    Un mismo nombre de foto puede existir en dos zips y ser dos fotos distintas de
    dos animales distintos (Cay y Hedy Lamarr comparten «IMG_1352»), así que la
    identidad de una foto es el par zip+ruta, no el nombre.

    Devuelve (plan, asignacion):
      plan        [(id, zip, ruta, nombre_final, alt)] — una entrada por fichero
      asignacion  {handle: [id, ...]} en el orden en que van en la ficha
    """
    reclaman = collections.defaultdict(list)      # quién pide cada nombre
    for a in animales:
        for k in a["fotos"]:
            reclaman[k].append(a)

    def elige(a, k):
        copias = idx.get(k, [])
        if len(copias) <= 1:
            return copias[0] if copias else None
        # 1) el zip del álbum del animal
        prefer = [ZIP_DE_ALBUM[t] for t in a["albumes"] if t in ZIP_DE_ALBUM]
        cual = next((c for c in copias if c[0] in prefer), None)
        if cual:
            return cual
        # 2) si no, el zip que ningún otro que pida esa foto reclama por álbum
        otros = set()
        for b in reclaman[k]:
            if b is not a:
                otros.update(ZIP_DE_ALBUM[t] for t in b["albumes"] if t in ZIP_DE_ALBUM)
        return next((c for c in copias if c[0] not in otros), copias[0])

    vistos, plan, asignacion = {}, [], {}
    for a in animales:
        especie = "gato" if "GATOS" in a["albumes"] else "perro"
        suyas = []
        for n, k in enumerate(a["fotos"], 1):
            cual = elige(a, k)
            if cual is None:
                continue
            ident = "%s|%s" % (cual[0], cual[1])
            suyas.append(ident)
            if ident in vistos:                    # foto de verdad compartida (Bonnie y Clyde)
                continue
            ext = os.path.splitext(cual[1])[1].lower() or ".jpg"
            vistos[ident] = True
            plan.append((ident, cual[0], cual[1], "%s-%d%s" % (a["handle"], n, ext),
                         "%s, %s en adopción en Love Animals BCN" % (a["nombre"], especie)))
        asignacion[a["handle"]] = suyas
    return plan, asignacion


def bytes_de(znombre, ruta):
    if znombre is None:
        with open(os.path.join(IMGS, ruta), "rb") as f:
            return f.read()
    with zipfile.ZipFile(os.path.join(IMGS, znombre)) as f:
        return f.read(ruta)


# ------------------------------------------------------------------ subida
M_STAGED = """
mutation($input:[StagedUploadInput!]!){
  stagedUploadsCreate(input:$input){
    stagedTargets{ url resourceUrl parameters{ name value } }
    userErrors{ field message }
  }
}
"""

M_FILE = """
mutation($files:[FileCreateInput!]!){
  fileCreate(files:$files){
    files{ id fileStatus alt ... on MediaImage { image { url } } }
    userErrors{ field message code }
  }
}
"""

Q_ESTADO = """
query($ids:[ID!]!){ nodes(ids:$ids){ ... on MediaImage { id fileStatus fileErrors{ code details message } image{ url } } } }
"""


def sube_lote(lote):
    """lote = [(clave, zip, ruta, nombre, alt)] -> {clave: gid}"""
    entrada = []
    contenido = {}
    for k, zn, ruta, nombre, alt in lote:
        datos = bytes_de(zn, ruta)
        contenido[nombre] = datos
        entrada.append({
            "filename": nombre,
            "mimeType": mimetypes.guess_type(nombre)[0] or "image/jpeg",
            "resource": "IMAGE",
            "httpMethod": "POST",
            "fileSize": str(len(datos)),
        })
    d = gql(M_STAGED, {"input": entrada})["stagedUploadsCreate"]
    if d["userErrors"]:
        raise SystemExit("stagedUploads: %s" % d["userErrors"])

    ficheros = []
    for (k, zn, ruta, nombre, alt), destino in zip(lote, d["stagedTargets"]):
        campos = [(p["name"], p["value"]) for p in destino["parameters"]]
        r = requests.post(destino["url"], data=campos,
                          files={"file": (nombre, contenido[nombre])}, timeout=300)
        if r.status_code not in (200, 201, 204):
            raise SystemExit("subida de %s: %s %s" % (nombre, r.status_code, r.text[:300]))
        ficheros.append({"originalSource": destino["resourceUrl"], "contentType": "IMAGE", "alt": alt})

    d = gql(M_FILE, {"files": ficheros})["fileCreate"]
    if d["userErrors"]:
        raise SystemExit("fileCreate: %s" % d["userErrors"])
    return {lote[i][0]: f["id"] for i, f in enumerate(d["files"])}


def espera(gids):
    """Shopify procesa las imágenes en diferido; hasta READY no se pueden referenciar."""
    pendientes = list(gids)
    for vuelta in range(40):
        nodos = gql(Q_ESTADO, {"ids": pendientes})["nodes"]
        malos = [n for n in nodos if n and n["fileStatus"] == "FAILED"]
        if malos:
            raise SystemExit("fallaron: %s" % json.dumps(malos, ensure_ascii=False)[:500])
        pendientes = [n["id"] for n in nodos if n and n["fileStatus"] != "READY"]
        if not pendientes:
            return
        time.sleep(3)
    print("   aviso: %d fotos siguen procesándose" % len(pendientes))


def main():
    if not TOKEN:
        raise SystemExit("falta LA_TOKEN_REAL en el entorno")
    accion = sys.argv[1] if len(sys.argv) > 1 else "estado"

    fichas = json.load(open(FICHAS, encoding="utf-8"))
    idx = inventario()
    plan = reparte(fichas["animales"], idx)
    hechas = json.load(open(FOTOS, encoding="utf-8")) if os.path.exists(FOTOS) else {}
    quedan = [p for p in plan if p[0] not in hechas]

    peso = sum(t[2] for p in quedan for t in [next(c for c in idx[p[1] and nfc(os.path.splitext(os.path.basename(p[2]))[0]) or ''] if 0)] ) if False else sum(tam(p) for p in quedan)
    print("fotos del plan: %d | ya subidas: %d | quedan: %d (%.0f MB)"
          % (len(plan), len(hechas), len(quedan), peso / 1e6))

    if accion == "estado":
        return
    if accion == "prueba":
        quedan = quedan[:1]
    if not quedan:
        print("nada que hacer"); return

    TAM = 10
    subidas = 0
    for i in range(0, len(quedan), TAM):
        lote = quedan[i:i + TAM]
        nuevas = sube_lote(lote)
        espera(list(nuevas.values()))
        hechas.update(nuevas)
        subidas += len(nuevas)
        with open(FOTOS, "w", encoding="utf-8") as f:
            json.dump(hechas, f, ensure_ascii=False, indent=1)
        print("   %d/%d  %s" % (subidas, len(quedan), lote[-1][3]))
    print("listo:", len(hechas), "fotos en la tienda ->", FOTOS)


if __name__ == "__main__":
    main()
