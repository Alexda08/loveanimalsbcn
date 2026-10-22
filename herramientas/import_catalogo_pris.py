# -*- coding: utf-8 -*-
"""Crea en la tienda los productos del catálogo actual de El Armario de Pris
(tazas, mochilas y fundas), con sus fotos recortadas del Canva.

Idempotente por handle. Los precios son los del catálogo (agosto 2026), aunque
la web los tenga ocultos en modo escaparate.
"""
import io
import json
import mimetypes
import os
import sys
import urllib.request
import uuid

from shop import gql, user_errors

sys.stdout.reconfigure(encoding="utf-8")

ENVIO = "Envío a toda España (6 € aparte)"

FICHA_TAZA = [
    "Cerámica resistente al microondas y al lavavajillas",
    "Aguanta 3.000 lavados sin que el estampado pierda color",
    ENVIO,
]
FICHA_TAZA_FOTO = [
    "Cerámica resistente al microondas y al lavavajillas",
    "Se personaliza con la foto que tú quieras junto a la frase",
    "Aguanta 3.000 lavados sin que el estampado pierda color",
    ENVIO,
]
FICHA_MOCHILA = [
    "Tejido non-woven, ligera y resistente",
    "Cierre de cordón para llevarla a la espalda",
    ENVIO,
]
FICHA_FUNDA = [
    "Escríbenos para saber las marcas y modelos disponibles",
    "Estampado a todo color sobre funda rígida",
    ENVIO,
]

# handle, título, tipo, precio, familia (para claim/historia), etiqueta, tipo_prenda, ficha, hermano textil
CATALOGO = [
    ("taza-de-la-jaula-a-la-vida", "Taza · De la jaula a la vida", "Taza", "10.00", "jaula",
     "Taza", "Taza de cerámica", FICHA_TAZA, "camiseta-de-la-jaula-a-la-vida"),
    ("taza-si-tu-me-dices-miau", "Taza · Si tú me dices MIAU lo dejo TODO", "Taza", "10.00", "gatos",
     "Taza", "Taza de cerámica", FICHA_TAZA, "camiseta-si-tu-me-dices-miau"),
    ("taza-mestizos", "Taza · Yo también soy de raza(s)", "Taza", "10.00", "mestizos",
     "Taza", "Taza de cerámica", FICHA_TAZA, "camiseta-mestizos"),
    ("taza-stop-ley-ppp", "Taza · Stop Ley PPP", "Taza", "10.00", "ppp",
     "Causa", "Taza de cerámica · personalizable", FICHA_TAZA_FOTO, "camiseta-stop-ley-ppp"),
    ("taza-foto-si-tu-me-dices-miau", "Taza personalizable · Si tú me dices MIAU", "Taza", "11.00", "gatos",
     "Personalizable", "Taza con tu foto", FICHA_TAZA_FOTO, "camiseta-si-tu-me-dices-miau"),
    ("taza-foto-el-amor-no-se-compra", "Taza personalizable · El amor no se compra", "Taza", "11.00", "amor",
     "Personalizable", "Taza con tu foto", FICHA_TAZA_FOTO, "camiseta-el-amor-no-se-compra"),
    ("mochila-love-animals-bcn", "Mochila-saco · Love Animals BCN", "Mochila", "10.00", "logo",
     "Mochila", "Mochila de cuerdas", FICHA_MOCHILA, "camiseta-love-animals-bcn"),
    ("mochila-stop-ley-ppp", "Mochila-saco · Stop Ley PPP", "Mochila", "10.00", "ppp",
     "Causa", "Mochila de cuerdas", FICHA_MOCHILA, "camiseta-stop-ley-ppp"),
    ("funda-movil-love-animals-bcn", "Funda de móvil · Love Animals BCN", "Funda de móvil", "14.95", "logo",
     "Funda", "Funda rígida", FICHA_FUNDA, "camiseta-love-animals-bcn"),
    ("funda-movil-stop-ley-ppp", "Funda de móvil · Stop Ley PPP", "Funda de móvil", "14.95", "ppp",
     "Causa", "Funda rígida", FICHA_FUNDA, "camiseta-stop-ley-ppp"),
]

CLAIM = {
    "ppp": "yo no soy peligroso",
    "gatos": "en esta casa mandan ellos",
    "mestizos": "todos pertenecen a una raza única: perro",
    "jaula": "cada jaula esconde una historia que merece cambiar",
    "amor": "el amor no se compra, se adopta",
    "logo": "por todos los que hacéis familia",
}

BANDA = {
    "Taza": "la pinta a mano El Armario de Pris",
    "Mochila": "la prepara El Armario de Pris",
    "Funda de móvil": "la prepara El Armario de Pris",
}

# --------------------------------------------------------------- subida de fotos ---
M_STAGED = """
mutation($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}
"""


def sube(ruta):
    """Sube un fichero local y devuelve la resourceUrl para usarla como originalSource."""
    nombre = os.path.basename(ruta)
    tipo = mimetypes.guess_type(nombre)[0] or "image/png"
    datos = open(ruta, "rb").read()
    res = gql(M_STAGED, {"input": [{
        "resource": "IMAGE", "filename": nombre, "mimeType": tipo,
        "httpMethod": "POST", "fileSize": str(len(datos)),
    }]})["stagedUploadsCreate"]
    if user_errors(res, nombre):
        return None
    destino = res["stagedTargets"][0]

    frontera = "----lab" + uuid.uuid4().hex
    cuerpo = b""
    for p in destino["parameters"]:
        cuerpo += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
                   % (frontera, p["name"], p["value"])).encode("utf-8")
    cuerpo += ("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"%s\"\r\n"
               "Content-Type: %s\r\n\r\n" % (frontera, nombre, tipo)).encode("utf-8")
    cuerpo += datos + ("\r\n--%s--\r\n" % frontera).encode("utf-8")

    req = urllib.request.Request(destino["url"], data=cuerpo, method="POST",
                                 headers={"Content-Type": "multipart/form-data; boundary=" + frontera})
    with urllib.request.urlopen(req, timeout=120) as r:
        r.read()
    return destino["resourceUrl"]


# ------------------------------------------------------------------- productos ---
Q_HERMANO = """
query($handle: String!) {
  productByHandle(handle: $handle) {
    metafields(first: 20, namespace: "custom") { nodes { key value type } }
  }
}
"""

M_SET = """
mutation($input: ProductSetInput!) {
  productSet(synchronous: true, input: $input) {
    product { id handle title }
    userErrors { field message code }
  }
}
"""

M_PUBLISH = """
mutation($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) { userErrors { field message } }
}
"""

online = next(p["id"] for p in gql("{ publications(first: 10) { nodes { id name } } }")["publications"]["nodes"]
              if "Online Store" in p["name"])

creados = {}
for handle, titulo, tipo, precio, fam, etiqueta, tipo_prenda, ficha, hermano in CATALOGO:
    # la historia del diseño se hereda de la prenda con el mismo estampado
    historia = {}
    h = gql(Q_HERMANO, {"handle": hermano})["productByHandle"]
    if h:
        for mf in h["metafields"]["nodes"]:
            if mf["key"].startswith("historia"):
                historia[mf["key"]] = (mf["value"], mf["type"])

    metafields = [
        {"namespace": "custom", "key": "etiqueta", "type": "single_line_text_field", "value": etiqueta},
        {"namespace": "custom", "key": "etiqueta_eco", "type": "boolean", "value": "false"},
        {"namespace": "custom", "key": "tipo_prenda", "type": "single_line_text_field", "value": tipo_prenda},
        {"namespace": "custom", "key": "claim", "type": "single_line_text_field", "value": CLAIM[fam]},
        {"namespace": "custom", "key": "impacto_corto", "type": "single_line_text_field",
         "value": BANDA[tipo]},
        {"namespace": "custom", "key": "ficha", "type": "list.single_line_text_field",
         "value": json.dumps(ficha, ensure_ascii=False)},
    ]
    for clave, (valor, mtipo) in historia.items():
        metafields.append({"namespace": "custom", "key": clave, "type": mtipo, "value": valor})

    foto = "canva/productos/%s.png" % handle
    recurso = sube(foto)

    descripcion = "".join("<p>%s</p>" % x for x in ficha)
    inp = {
        "handle": handle,
        "title": titulo,
        "descriptionHtml": descripcion,
        "productType": tipo,
        "vendor": "Love Animals BCN",
        "tags": sorted({fam, tipo.lower(), "catalogo-pris"}),
        "status": "ACTIVE",
        "metafields": metafields,
        "productOptions": [{"name": "Title", "values": [{"name": "Default Title"}]}],
        "variants": [{
            "optionValues": [{"optionName": "Title", "name": "Default Title"}],
            "price": precio,
            "inventoryPolicy": "CONTINUE",
            "inventoryItem": {"tracked": False},
            "taxable": True,
        }],
    }
    if recurso:
        inp["files"] = [{"originalSource": recurso, "contentType": "IMAGE", "alt": titulo}]

    res = gql(M_SET, {"input": inp})["productSet"]
    if user_errors(res, handle):
        continue
    pid = res["product"]["id"]
    gql(M_PUBLISH, {"id": pid, "input": [{"publicationId": online}]})
    creados[handle] = {"id": pid, "tipo": tipo, "familia": fam, "titulo": titulo}
    print("  +", handle, "·", titulo, "·", precio, "€")

json.dump(creados, open("catalogo_pris_creado.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("total:", len(creados))
