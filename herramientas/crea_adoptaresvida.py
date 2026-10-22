# -*- coding: utf-8 -*-
"""Da de alta la camiseta y la sudadera «Adoptar es vida» que mandó Carla.

El diseño ya existe en el catálogo de Pris: es ADOPTARESVIDA en los SKU, y no
hay que confundirlo con SILUETAADOPTAR, que es el de 2022 (frase *y* silueta) y
que se ha retirado. Los mockups que mandó son todos blancos, así que van sólo
en blanco; el resto de la estructura es la misma que la de sus hermanos.

Las colecciones de esta tienda son todas automáticas por etiqueta, así que
`camiseta`/`sudadera` + `novedades` ya los mete donde tienen que ir.

    python crea_adoptaresvida.py crear      los crea EN BORRADOR
    python crea_adoptaresvida.py publicar   los pasa a la venta
"""
import os, sys, json, time, requests

API = "https://loveanimalsbcn.myshopify.com/admin/api/2026-01/graphql.json"
TOKEN = os.environ.get("LA_TOKEN_REAL", "")
AQUI = os.path.dirname(os.path.abspath(__file__))
MOCK = os.path.join(AQUI, "mockups")
HECHO = os.path.join(AQUI, "adoptaresvida.json")

PIE = (u"<p>Los pedidos se hacen por Instagram: escribe a <strong>El Armario de Pris</strong> "
       u"diciéndole el diseño y la talla. Parte de los beneficios se donan a la asociación "
       u"<strong>De la jaula a la vida</strong>.</p>"
       u"<p>Todos los pedidos pueden personalizarse: puedes pedir la prenda en otro color, "
       u"aunque en las fotos salga sólo la blanca.</p>"
       u"<p>Revisa bien las medidas antes de pedir: estos productos no admiten devolución.</p>")


def sku_camiseta(modelo, talla):
    return "LOVEANIMALSBCN-ADOPTARESVIDA_LIGHT-%s-WH-%s" % (
        "US002" if modelo == u"Unisex" else "WS002", talla)


def sku_sudadera(modelo, talla):
    return "LOVEANIMALSBCN-ADOPTARESVIDA_LIGHT-SWH02-WH-%s" % talla


PRODUCTOS = [
    {
        "handle": "camiseta-adoptar-es-vida",
        "title": u"Camiseta | Adoptar es vida",
        "productType": "Camiseta",
        "tags": ["adoptaresvida", "camiseta", "novedades"],
        "descriptionHtml": u"<p>El diseño de «Adoptar es vida», escrito a mano, en camiseta.</p>" + PIE,
        "opciones": [(u"Modelo", [u"Unisex", u"Mujer"]),
                     (u"Talla", [u"S", u"M", u"L", u"XL", u"2XL"]),
                     (u"Color", [u"Blanco"])],
        "precio": "15.00",
        "sku": sku_camiseta,
        "fotos": [("21.png", u"Camiseta blanca con la frase «Adoptar es vida» escrita a mano en negro"),
                  ("22.png", u"Camiseta blanca unisex con la frase «Adoptar es vida» en el pecho")],
    },
    {
        "handle": "sudadera-adoptar-es-vida",
        "title": u"Sudadera | Adoptar es vida",
        "productType": "Sudadera",
        "tags": ["adoptaresvida", "sudadera", "novedades"],
        "descriptionHtml": u"<p>El diseño de «Adoptar es vida», escrito a mano, en sudadera con capucha.</p>" + PIE,
        "opciones": [(u"Modelo", [u"Unisex"]),
                     (u"Talla", [u"XS", u"S", u"M", u"L", u"XL", u"2XL"]),
                     (u"Color", [u"Blanco"])],
        "precio": "25.00",
        "sku": sku_sudadera,
        "fotos": [("23.png", u"Sudadera blanca con capucha y la frase «Adoptar es vida» escrita a mano en negro"),
                  ("24.png", u"La sudadera blanca «Adoptar es vida» colgada de una escalera de madera")],
    },
]

CANALES = ["gid://shopify/Publication/66308472983",    # Online Store
           "gid://shopify/Publication/77882523799",    # Buy Button
           "gid://shopify/Publication/123177795735"]   # Shop


def gql(q, v=None):
    for n in range(6):
        r = requests.post(API, json={"query": q, "variables": v or {}},
                          headers={"X-Shopify-Access-Token": TOKEN}, timeout=120)
        if r.status_code in (429, 500, 502, 503):
            time.sleep(2 * (n + 1))
            continue
        d = r.json()
        if any(e.get("extensions", {}).get("code") == "THROTTLED" for e in d.get("errors") or []):
            time.sleep(3)
            continue
        if d.get("errors"):
            raise SystemExit("GraphQL: " + json.dumps(d["errors"], ensure_ascii=False)[:800])
        return d["data"]
    raise SystemExit("la API no responde")


def sube_fotos(fotos, prefijo):
    """staged upload -> POST -> lo que espera productCreate(media:)"""
    entrada, datos = [], []
    for i, (fichero, alt) in enumerate(fotos, 1):
        b = open(os.path.join(MOCK, fichero), "rb").read()
        nombre = "%s-%02d.png" % (prefijo, i)
        datos.append((nombre, b, alt))
        entrada.append({"filename": nombre, "mimeType": "image/png", "resource": "IMAGE",
                        "httpMethod": "POST", "fileSize": str(len(b))})
    d = gql("""mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
                 stagedTargets{ url resourceUrl parameters{name value} } userErrors{field message} } }""",
            {"input": entrada})["stagedUploadsCreate"]
    if d["userErrors"]:
        raise SystemExit("stagedUploads: %s" % d["userErrors"])
    media = []
    for (nombre, b, alt), destino in zip(datos, d["stagedTargets"]):
        campos = [(p["name"], p["value"]) for p in destino["parameters"]]
        r = requests.post(destino["url"], data=campos, files={"file": (nombre, b)}, timeout=600)
        if r.status_code not in (200, 201, 204):
            raise SystemExit("subida %s: %s %s" % (nombre, r.status_code, r.text[:200]))
        media.append({"originalSource": destino["resourceUrl"], "contentType": "IMAGE", "alt": alt})
    return media


def crear():
    hecho = json.load(open(HECHO)) if os.path.exists(HECHO) else {}
    for p in PRODUCTOS:
        if p["handle"] in hecho:
            print("ya estaba:", p["handle"])
            continue
        y = gql("""query($q:String!){ products(first:1, query:$q){ nodes{ id handle } } }""",
                {"q": "handle:" + p["handle"]})["products"]["nodes"]
        if y:
            print("!! ya existe en la tienda:", y[0]["handle"], y[0]["id"])
            continue

        media = sube_fotos(p["fotos"], p["handle"])
        d = gql("""mutation($product:ProductCreateInput!,$media:[CreateMediaInput!]){
                     productCreate(product:$product, media:$media){
                       product{ id handle title status } userErrors{ field message } } }""",
                {"product": {"handle": p["handle"], "title": p["title"],
                             "descriptionHtml": p["descriptionHtml"],
                             "productType": p["productType"], "vendor": "BCN",
                             "tags": p["tags"], "status": "DRAFT",
                             "productOptions": [{"name": n, "values": [{"name": v} for v in vs]}
                                                for n, vs in p["opciones"]]},
                 "media": media})["productCreate"]
        if d["userErrors"]:
            raise SystemExit("productCreate: %s" % json.dumps(d["userErrors"], ensure_ascii=False))
        pid = d["product"]["id"]
        print("creado (borrador):", d["product"]["handle"], pid)

        opciones = dict(p["opciones"])
        variantes = []
        for modelo in opciones[u"Modelo"]:
            for talla in opciones[u"Talla"]:
                variantes.append({
                    "optionValues": [{"optionName": u"Modelo", "name": modelo},
                                     {"optionName": u"Talla", "name": talla},
                                     {"optionName": u"Color", "name": u"Blanco"}],
                    "price": p["precio"],
                    "inventoryPolicy": "CONTINUE",
                    "inventoryItem": {"sku": p["sku"](modelo, talla), "tracked": True},
                })
        d = gql("""mutation($id:ID!,$v:[ProductVariantsBulkInput!]!,$s:ProductVariantsBulkCreateStrategy){
                     productVariantsBulkCreate(productId:$id, variants:$v, strategy:$s){
                       productVariants{ id title sku price } userErrors{ field message } } }""",
                {"id": pid, "v": variantes, "s": "REMOVE_STANDALONE_VARIANT"})["productVariantsBulkCreate"]
        if d["userErrors"]:
            raise SystemExit("variantes: %s" % json.dumps(d["userErrors"], ensure_ascii=False))
        print("   %d variantes" % len(d["productVariants"]))
        hecho[p["handle"]] = pid
        json.dump(hecho, open(HECHO, "w"), indent=1)


def publicar():
    hecho = json.load(open(HECHO))
    for h, pid in sorted(hecho.items()):
        d = gql("""mutation($p:ProductUpdateInput!){ productUpdate(product:$p){
                     product{ handle status } userErrors{ field message } } }""",
                {"p": {"id": pid, "status": "ACTIVE"}})["productUpdate"]
        if d["userErrors"]:
            raise SystemExit("status: %s" % d["userErrors"])
        d = gql("""mutation($id:ID!,$input:[PublicationInput!]!){ publishablePublish(id:$id, input:$input){
                     userErrors{ field message } } }""",
                {"id": pid, "input": [{"publicationId": c} for c in CANALES]})["publishablePublish"]
        if d["userErrors"]:
            raise SystemExit("publicar: %s" % d["userErrors"])
        print("publicado:", h)


if __name__ == "__main__":
    {"crear": crear, "publicar": publicar}[sys.argv[1]]()
