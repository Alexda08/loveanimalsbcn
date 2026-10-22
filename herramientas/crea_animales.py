# -*- coding: utf-8 -*-
# OJO (22-10-2026): reconstruido del historial de trabajo, pero le faltan los últimos
# retoques de la parte que genera docs/INDICE-ANIMALES.md: la versión final exacta no quedó registrada. Funciona como
# referencia del método; antes de relanzarlo, léelo entero y compáralo con docs/METAOBJETOS.md.
"""Da de alta álbumes y fichas de animal en la tienda REAL, en borrador.

Todo va por `handle`: relanzarlo actualiza lo que ya está y crea lo que falta,
nunca duplica. El token entra por LA_TOKEN_REAL y no se escribe en disco.

    python crea_animales.py albumes    los 11 álbumes (crea GATOS)
    python crea_animales.py animales   las 208 fichas, con su galería
    python crea_animales.py enlaza     mete cada animal en sus álbumes
    python crea_animales.py sobran     lista lo que hay en la tienda y ya no toca
    python crea_animales.py limpia     borra eso (pide confirmación)
    python crea_animales.py indice     regenera docs/INDICE-ANIMALES.md
    python crea_animales.py publica    pasa todo de borrador a publicado
"""
import os, sys, json, time, re, unicodedata
import requests

RAIZ = r"C:\Users\desca\OneDrive\Desktop\loveanimalsbcn"
AQUI = os.path.dirname(os.path.abspath(__file__))
FICHAS = os.path.join(AQUI, "fichas.json")
FOTOS = os.path.join(AQUI, "fotos.json")
ASIGNA = os.path.join(AQUI, "asignacion.json")
INDICE = os.path.join(AQUI, "indice.json")
MD = os.path.join(RAIZ, "docs", "INDICE-ANIMALES.md")

TIENDA = "loveanimalsbcn.myshopify.com"
API = "https://%s/admin/api/2026-01/graphql.json" % TIENDA
TOKEN = os.environ.get("LA_TOKEN_REAL", "")
ADMIN = "https://admin.shopify.com/store/loveanimalsbcn/content/entries/%s/%s"


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


M_UPSERT = """
mutation($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
  metaobjectUpsert(handle: $handle, metaobject: $metaobject) {
    metaobject { id handle type }
    userErrors { field message code }
  }
}
"""

M_UPDATE = """
mutation($id: ID!, $metaobject: MetaobjectUpdateInput!) {
  metaobjectUpdate(id: $id, metaobject: $metaobject) {
    metaobject { id handle }
    userErrors { field message code }
  }
}
"""

M_BORRA = """
mutation($id: ID!) { metaobjectDelete(id: $id) { deletedId userErrors { field message } } }
"""

Q_TODOS = """
query($t:String!,$c:String){
  metaobjects(type:$t, first:100, after:$c){
    pageInfo{ hasNextPage endCursor }
    nodes{ id handle capabilities{ publishable{ status } } fields{ key value } }
  }
}
"""


# Nacen publicadas: la tienda de verdad ya lleva las 200 fichas en marcha y
# relanzar esto no puede devolverlas a borrador por el camino.
def upsert(tipo, handle, campos, borrador=False):
    v = {
        "handle": {"type": tipo, "handle": handle},
        "metaobject": {
            "fields": [{"key": k, "value": val} for k, val in campos.items() if val not in (None, "")],
            "capabilities": {"publishable": {"status": "DRAFT" if borrador else "ACTIVE"}},
        },
    }
    d = gql(M_UPSERT, v)["metaobjectUpsert"]
    if d["userErrors"]:
        raise SystemExit("%s/%s: %s" % (tipo, handle, d["userErrors"]))
    return d["metaobject"]["id"]


def todos(tipo):
    out, cur = [], None
    while True:
        m = gql(Q_TODOS, {"t": tipo, "c": cur})["metaobjects"]
        out += m["nodes"]
        if not m["pageInfo"]["hasNextPage"]:
            break
        cur = m["pageInfo"]["endCursor"]
    return out


# El titulo que se ve en la web no tiene por que ser el del Excel: Carla pidio
# que «MESTIZOS» dijera tambien que ahi hay perros de raza. El handle no se toca,
# que es lo que cuelga de /album/ y a donde apunta la 301 del blog viejo.
TITULOS_WEB = {"mestizos": "MESTIZOS Y NO PPP"}


def handle_de(titulo):
    s = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def rico(texto):
    """El campo `historia` es rich_text: Shopify lo quiere como árbol JSON."""
    parrafos = [p.strip() for p in re.split(r"\n{2,}", texto) if p.strip()] or [texto]
    return json.dumps({"type": "root", "children": [
        {"type": "paragraph", "children": [{"type": "text", "value": p}]} for p in parrafos]},
        ensure_ascii=False)


def carga(ruta, defecto):
    return json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else defecto


def guarda(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ acciones
def haz_albumes(datos, indice):
    for al in datos["albumes"]:
        h = handle_de(al["titulo"])
        campos = {
            "titulo": TITULOS_WEB.get(h, al["titulo"]),
            "subtitulo": al["subtitulo"],
            "es_urgente": "true" if al["es_urgente"] else "false",
        }
        if al["anio_espera"]:
            campos["anio_espera"] = str(al["anio_espera"])
        gid = upsert("album", h, campos)
        indice.setdefault("albumes", {})[h] = gid
        print("   álbum", h, gid.rsplit("/", 1)[1])
    guarda(INDICE, indice)


def haz_animales(datos, indice, solo=None):
    fotos = carga(FOTOS, {})
    asigna = carga(ASIGNA, {})
    if not fotos:
        print("   aviso: no hay fotos.json, las fichas se crean sin galería")
    hechos = indice.setdefault("animales", {})

    # solo suben los que están completos: sin foto, la ficha se queda esperando
    lista = [a for a in datos["animales"] if a["fotos"]]
    if solo:
        lista = [a for a in lista if a["handle"] == solo] or [a for a in datos["animales"] if a["handle"] == solo]
    else:
        print("   fuera por no tener foto: %s" % ", ".join(
            a["nombre"] for a in datos["animales"] if not a["fotos"]))

    for n, a in enumerate(lista, 1):
        galeria = [fotos[i] for i in asigna.get(a["handle"], []) if i in fotos]
        campos = {
            "nombre": a["nombre"],
            "frase": a["frase"],
            "fecha_entrada": a["fecha_entrada"],
            "fecha_adopcion": a["fecha_adopcion"],
            "edad": a["edad"],
            "tamano": a["tamano"],
            "sexo": a["sexo"],
            "convive_ninos": a["convive_ninos"],
            "convive_perros": a["convive_perros"],
            "convive_gatos": a["convive_gatos"],
            "estado": a["estado"],
            "caracter": json.dumps(a["caracter"], ensure_ascii=False) if a["caracter"] else "",
            "historia": rico(a["historia"]) if a["historia"] else "",
            "galeria": json.dumps(galeria) if galeria else "",
        }
        if a["ppp"] is not None:
            campos["ppp"] = "true" if a["ppp"] else "false"
        hechos[a["handle"]] = upsert("animal", a["handle"], campos)
        if n % 10 == 0:
            guarda(INDICE, indice)
            print("   %d/%d  %s" % (n, len(lista), a["handle"]))
    guarda(INDICE, indice)
    print("   %d fichas" % len(hechos))


def haz_enlaces(datos, indice):
    albumes = indice.get("albumes", {})
    animales = indice.get("animales", {})
    dentro = {h: [] for h in albumes}
    for a in datos["animales"]:
        for titulo in a["albumes"]:
            h = handle_de(titulo)
            if h in dentro and a["handle"] in animales:
                dentro[h].append(animales[a["handle"]])
    for h, gids in dentro.items():
        d = gql(M_UPDATE, {"id": albumes[h], "metaobject": {
            "fields": [{"key": "animales", "value": json.dumps(gids)}]}})["metaobjectUpdate"]
        if d["userErrors"]:
            raise SystemExit("%s: %s" % (h, d["userErrors"]))
        print("   %-30s %d animales" % (h, len(gids)))


def sobran(datos):
    quiero = {a["handle"] for a in datos["animales"]}
    fuera = {}
    for f in datos["fuera"]:
        fuera[handle_de(f["nombre"])] = f["nota"]
    resto = []
    for m in todos("animal"):
        if m["handle"] not in quiero:
            resto.append((m["handle"], m["id"], fuera.get(m["handle"], "ya no está en el Excel")))
    return resto


def baja(datos):
    """Los adoptados no se borran: pasan a borrador y esperan al rincon feliz."""
    resto = sobran(datos)
    if not resto:
        print("   no sobra ninguna"); return
    for h, gid, porque in resto:
        d = gql(M_UPDATE, {"id": gid, "metaobject": {
            "capabilities": {"publishable": {"status": "DRAFT"}}}})["metaobjectUpdate"]
        if d["userErrors"]:
            print("   error en", h, d["userErrors"])
        else:
            print("   a borrador  %-22s %s" % (h, porque[:60]))


def limpia(datos):
    resto = sobran(datos)
    if not resto:
        print("   nada que borrar"); return
    for h, gid, porque in resto:
        print("   %-24s %s" % (h, porque[:70]))
    if input("\n   ¿borro estas %d fichas? (escribe SI) " % len(resto)) != "SI":
        print("   cancelado"); return
    for h, gid, _ in resto:
        d = gql(M_BORRA, {"id": gid})["metaobjectDelete"]
        if d["userErrors"]:
            print("   error en", h, d["userErrors"])
        else:
            print("   borrada", h)


def publica(indice):
    ids = list(indice.get("albumes", {}).values()) + list(indice.get("animales", {}).values())
    for n, gid in enumerate(ids, 1):
        d = gql(M_UPDATE, {"id": gid, "metaobject": {
            "capabilities": {"publishable": {"status": "ACTIVE"}}}})["metaobjectUpdate"]
        if d["userErrors"]:
            print("   error", gid, d["userErrors"])
        if n % 25 == 0:
            print("   %d/%d" % (n, len(ids)))
    print("   %d entradas publicadas" % len(ids))


# ------------------------------------------------------------------ índice md
def escribe_md(datos, indice):
    animales = datos["animales"]
    albumes = datos["albumes"]
    an = indice.get("animales", {})
    al = indice.get("albumes", {})
    dentro = {handle_de(x["titulo"]): 0 for x in albumes}
    for a in animales:
        for t in a["albumes"]:
            dentro[handle_de(t)] = dentro.get(handle_de(t), 0) + 1

    L = []
    L.append("# Índice de animales y álbumes\n")
    L.append("> ### Contenido de verdad, pero todavía vivo\n>")
    L.append("> Estas **%d fichas** y **%d álbumes** salen del Excel que rellenó Carla." % (len(animales), len(albumes)))
    L.append("> Están **en borrador**: existen en la tienda, se pueden ver y editar desde el")
    L.append("> admin, pero no las pinta nadie hasta que se publiquen a mano.\n>")
    L.append("> Como el alta va por `handle`, esto se puede relanzar las veces que haga falta:")
    L.append("> las fichas que ya están se actualizan y las nuevas se crean. No hay que")
    L.append("> rehacer nada ni borrar para volver a subir.\n")

    L.append("\n## Álbumes\n")
    L.append("| Álbum | handle | Animales | ID | Editar |")
    L.append("|---|---|---:|---|---|")
    for x in albumes:
        h = handle_de(x["titulo"])
        gid = al.get(h, "")
        num = gid.rsplit("/", 1)[1] if gid else "—"
        enlace = "[abrir](%s)" % (ADMIN % ("album", num)) if gid else "—"
        L.append("| %s | `%s` | %d | `%s` | %s |" % (x["titulo"], h, dentro.get(h, 0), num, enlace))

    sin_foto = [a for a in animales if not a["fotos"]]
    L.append("\n\n## Animales\n")
    L.append("%d fichas. La columna **Foto** dice si la ficha lleva galería;" % len(animales))
    L.append("las %d que van con «—» son las que se quedaron sin imagen." % len(sin_foto))
    L.append("")
    L.append("| # | Nombre | handle | ID | Foto | Álbumes | Editar |")
    L.append("|---:|---|---|---|:-:|---|---|")
    for i, a in enumerate(animales, 1):
        gid = an.get(a["handle"], "")
        num = gid.rsplit("/", 1)[1] if gid else "—"
        enlace = "[abrir](%s)" % (ADMIN % ("animal", num)) if gid else "—"
        L.append("| %d | %s | `%s` | `%s` | %s | %s | %s |" % (
            i, a["nombre"], a["handle"], num,
            "✅" if a["fotos"] else "—",
            ", ".join(a["albumes"]), enlace))

    if datos["fuera"]:
        L.append("\n\n## Fuera de la web\n")
        L.append("Carla marcó estas %d en «Notas» y no se han subido:\n" % len(datos["fuera"]))
        L.append("| Fila | Nombre | Nota |")
        L.append("|---:|---|---|")
        for f in datos["fuera"]:
            L.append("| %d | %s | %s |" % (f["fila"], f["nombre"], f["nota"].replace("|", "/")[:90]))

    if sin_foto:
        L.append("\n\n## Fichas sin foto\n")
        L.append("| Fila | Nombre | Qué pasa |")
        L.append("|---:|---|---|")
        for a in sin_foto:
            que = ("las fotos que pone el Excel no están en los zips: %s" % ", ".join(a["fotos_perdidas"])
                   if a["fotos_perdidas"] else "el Excel no dice qué fotos son")
            L.append("| %d | %s | %s |" % (a["fila"], a["nombre"], que))

    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("->", MD)


def main():
    accion = sys.argv[1] if len(sys.argv) > 1 else "estado"
    if accion != "indice" and not TOKEN:
        raise SystemExit("falta LA_TOKEN_REAL en el entorno")
    datos = json.load(open(FICHAS, encoding="utf-8"))
    indice = carga(INDICE, {})

    solo = sys.argv[2] if len(sys.argv) > 2 else None
    if accion == "albumes":
        haz_albumes(datos, indice)
    elif accion == "animales":
        haz_animales(datos, indice, solo)
    elif accion == "enlaza":
        haz_enlaces(datos, indice)
    elif accion == "sobran":
        for h, gid, porque in sobran(datos):
            print("   %-24s %s" % (h, porque[:80]))
    elif accion == "baja":
        baja(datos)
    elif accion == "limpia":
        limpia(datos)
    elif accion == "publica":
        publica(indice)
    elif accion == "indice":
        escribe_md(datos, indice)
    else:
        print("acciones: albumes | animales | enlaza | sobran | baja | limpia | indice | publica")


if __name__ == "__main__":
    main()
