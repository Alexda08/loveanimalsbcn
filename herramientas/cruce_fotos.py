# -*- coding: utf-8 -*-
"""El cruce: Excel <-> fichas de la tienda <-> fotos de los zips <-> galerías
<-> biblioteca de Archivos. Todo local. Deja cruce_fotos.txt y cruce_fotos.json."""
import json, io, re, unicodedata, collections
from huella import distancia


def carga(n):
    return json.load(io.open(n, encoding="utf-8"))


def nfc(s):
    return unicodedata.normalize("NFC", s or "").strip()


def plano(s):
    return re.sub(r"\s+", " ", nfc(s)).strip().lower()


fichas = carga("fichas.json")
zips = carga("inventario_zips.json")
tienda = carga("inventario_tienda.json")
huellas = carga("huellas_tienda.json")
prods = carga("dump/productos.json")
albs = carga("dump/album.json")
anim_dump = carga("dump/animal.json")
id2handle = {a["id"]: a["handle"] for a in anim_dump}

excel = {a["handle"]: a for a in fichas["animales"]}
store = {a["handle"]: a for a in tienda["animales"]}
R = collections.OrderedDict()
L = []


def sec(t):
    L.append("")
    L.append("=" * 78)
    L.append(t)
    L.append("=" * 78)


# ---------------------------------------------------------------- A. Excel <-> tienda
sec("A. EXCEL <-> FICHAS DE LA TIENDA")
solo_excel = sorted(set(excel) - set(store))
solo_tienda = sorted(set(store) - set(excel))
L.append("animales en el Excel (sin los 17 NO PONERLO): %d   en la tienda: %d" % (len(excel), len(store)))
L.append("en el Excel y no en la tienda: %s" % (solo_excel or "ninguno"))
L.append("en la tienda y no en el Excel: %s" % (", ".join(
    "%s(%s,%s)" % (h, store[h]["publicado"], store[h]["estado"]) for h in solo_tienda) or "ninguno"))
R["solo_excel"], R["solo_tienda"] = solo_excel, solo_tienda

campos_dump = {a["handle"]: {f["key"]: f.get("value") for f in a["fields"]} for a in anim_dump}


def rich_a_texto(v):
    try:
        d = json.loads(v)
    except Exception:
        return plano(v)
    out = []

    def anda(n):
        if isinstance(n, dict):
            if n.get("type") == "text":
                out.append(n.get("value", ""))
            for c in n.get("children", []) or []:
                anda(c)
            if n.get("type") == "paragraph":
                out.append("\n")
    anda(d)
    return plano("".join(out))


difs = []
for h, e in excel.items():
    t = campos_dump.get(h)
    if not t:
        continue
    for k in ("nombre", "estado", "fecha_entrada", "fecha_adopcion", "sexo", "edad", "tamano",
              "convive_ninos", "convive_perros", "convive_gatos", "frase"):
        ev, tv = plano(str(e.get(k) or "")), plano(str(t.get(k) or ""))
        if ev != tv:
            difs.append((h, k, ev[:60], tv[:60]))
    if bool(e.get("ppp")) != (str(t.get("ppp")).lower() == "true"):
        difs.append((h, "ppp", str(e.get("ppp")), str(t.get("ppp"))))
    ec = [plano(x) for x in (e.get("caracter") or [])]
    try:
        tc = [plano(x) for x in json.loads(t.get("caracter") or "[]")]
    except Exception:
        tc = [plano(t.get("caracter") or "")]
    if ec != tc:
        difs.append((h, "caracter", ", ".join(ec)[:60], ", ".join(tc)[:60]))
    eh, th = plano(e.get("historia") or ""), rich_a_texto(t.get("historia") or "")
    if eh != th:
        i = next((i for i in range(min(len(eh), len(th))) if eh[i] != th[i]), min(len(eh), len(th)))
        difs.append((h, "historia", "…" + eh[max(0, i - 25):i + 35], "…" + th[max(0, i - 25):i + 35]))
L.append("")
L.append("diferencias de campo Excel -> tienda: %d" % len(difs))
por_campo = collections.Counter(k for _, k, _, _ in difs)
L.append("  por campo: " + ", ".join("%s=%d" % kv for kv in por_campo.most_common()))
for h, k, ev, tv in difs:
    L.append("  %-18s %-14s excel=[%s]  tienda=[%s]" % (h, k, ev, tv))
R["difs_campos"] = difs

memb = collections.defaultdict(set)
for a in albs:
    c = {f["key"]: f.get("value") for f in a["fields"]}
    ids = (json.loads(c["animales"]) if c.get("animales") else []) + \
          (json.loads(c["animales_mas"]) if c.get("animales_mas") else [])
    for gid in ids:
        memb[id2handle.get(gid, gid)].add(c.get("titulo"))
dif_alb = []
for h, e in excel.items():
    ex = set(plano(x) for x in e.get("albumes") or [])
    ti = set(plano(x) for x in memb.get(h, set()))
    if ex != ti:
        dif_alb.append((h, sorted(ex - ti), sorted(ti - ex)))
L.append("")
L.append("álbumes: animales cuyo reparto no coincide con el Excel: %d" % len(dif_alb))
for h, falta, sobra in dif_alb:
    L.append("  %-18s excel dice y no está: %s | está y el excel no dice: %s" % (h, falta, sobra))
R["dif_albumes"] = dif_alb

# ---------------------------------------------------------------- B. fotos: excel vs galeria
sec("B. FOTOS: LO QUE DICE EL EXCEL vs LA GALERÍA DE LA TIENDA")
dif_n = []
sin_foto = []
for h, e in excel.items():
    t = store.get(h)
    if not t:
        continue
    n_excel = len(e.get("fotos") or [])
    n_tienda = len(t["fotos"])
    perdidas = e.get("fotos_perdidas") or []
    if n_tienda == 0:
        sin_foto.append(h)
    if n_excel != n_tienda:
        dif_n.append((h, n_excel, n_tienda, perdidas))
L.append("animales sin ninguna foto en la tienda: %d %s" % (len(sin_foto), sin_foto))
L.append("animales con distinto nº de fotos Excel/tienda: %d" % len(dif_n))
for h, a, b, p in dif_n:
    L.append("  %-18s excel=%d tienda=%d %s" % (h, a, b, ("perdidas en el excel: %s" % p) if p else ""))
perd = [(h, e["fotos_perdidas"]) for h, e in excel.items() if e.get("fotos_perdidas")]
L.append("fotos que el Excel nombra y no existen en ningún zip: %d animales" % len(perd))
for h, p in perd:
    L.append("  %-18s %s" % (h, p))
R["sin_foto"], R["dif_n"], R["perdidas"] = sin_foto, dif_n, perd

# ---------------------------------------------------------------- C. huellas
sec("C. HUELLAS: CADA FOTO DE LA TIENDA, ¿DE QUÉ FOTO DEL ZIP VIENE? ¿SE REPITE?")
zh = [z for z in zips if z.get("huella")]
vistas = collections.OrderedDict()
for z in zh:
    for hh, lst in vistas.items():
        if distancia(z["huella"], hh) <= 4:
            lst.append(z)
            break
    else:
        vistas[z["huella"]] = [z]
grupos_zip = [g for g in vistas.values() if len(g) > 1]
L.append("fotos en los zips: %d   grupos de fotos repetidas entre ficheros (huella casi igual): %d" % (len(zh), len(grupos_zip)))
for g in grupos_zip:
    L.append("  " + "  ==  ".join("%s/%s" % (x["zip"][:22], x["ruta"].split("/")[-1][:30]) for x in g))
R["repetidas_zip"] = [[x["zip"] + "|" + x["ruta"] for x in g] for g in grupos_zip]

gal = []
for a in tienda["animales"]:
    for i, f in enumerate(a["fotos"], 1):
        gal.append((a["handle"], i, f["id"], f["url"] or "", f["alt"] or "", (huellas.get(f["id"]) or {}).get("huella")))
origen = {}
sin_origen = []
for h, i, gid, url, alt, hu in gal:
    if not hu:
        sin_origen.append((h, i, "sin huella"))
        continue
    mejor, dmin = None, 99
    for z in zh:
        d = distancia(hu, z["huella"])
        if d < dmin:
            mejor, dmin = z, d
    if dmin <= 6:
        origen[gid] = (mejor, dmin)
    else:
        sin_origen.append((h, i, "la más parecida, a %d bits: %s/%s" % (dmin, mejor["zip"][:20], mejor["ruta"].split("/")[-1])))
L.append("")
L.append("fotos en galerías: %d   con origen claro en un zip: %d   sin origen en los zips: %d" % (len(gal), len(origen), len(sin_origen)))
for h, i, m in sin_origen:
    L.append("  %-18s foto %d  %s" % (h, i, m))
R["sin_origen"] = sin_origen

# origen que no cuadra con lo que el Excel asigna a ese animal
excel_fotos = {h: set(plano(x) for x in (e.get("fotos") or [])) for h, e in excel.items()}
mal_origen = []
for h, i, gid, url, alt, hu in gal:
    if gid not in origen or h not in excel_fotos:
        continue
    z, d = origen[gid]
    base = plano(re.sub(r"\.[a-z0-9]+$", "", z["fichero"], flags=re.I))
    if excel_fotos[h] and base not in excel_fotos[h] and not any(base.replace(" ", "") == x.replace(" ", "") for x in excel_fotos[h]):
        mal_origen.append((h, i, z["zip"][:24], z["fichero"], sorted(excel_fotos[h])[:4]))
L.append("")
L.append("fotos cuyo fichero de origen NO es uno de los que el Excel da a ese animal: %d" % len(mal_origen))
for x in mal_origen:
    L.append("  %-18s #%d %s/%s   excel: %s" % x)
R["mal_origen"] = mal_origen

por_hu = collections.defaultdict(list)
for h, i, gid, url, alt, hu in gal:
    if hu:
        por_hu[hu].append((h, i, gid, url.split("/")[-1].split("?")[0]))
claves = list(por_hu)
usado = set()
grupos = []
for a_ in claves:
    if a_ in usado:
        continue
    g = list(por_hu[a_])
    usado.add(a_)
    for b_ in claves:
        if b_ in usado:
            continue
        if distancia(a_, b_) <= 4:
            g += por_hu[b_]
            usado.add(b_)
    if len(g) > 1:
        grupos.append(g)
mismo_animal = [g for g in grupos if len({x[0] for x in g}) == 1]
entre_animales = [g for g in grupos if len({x[0] for x in g}) > 1]
L.append("")
L.append("la MISMA foto dos veces en la galería de un animal: %d" % len(mismo_animal))
for g in mismo_animal:
    L.append("  " + " | ".join("%s #%d %s" % (x[0], x[1], x[3]) for x in g))
L.append("la MISMA foto en galerías de animales DISTINTOS: %d" % len(entre_animales))
for g in entre_animales:
    L.append("  " + " | ".join("%s #%d %s" % (x[0], x[1], x[3]) for x in g))
R["mismo_animal"], R["entre_animales"] = mismo_animal, entre_animales

raros = []
nombres = {h: plano(store[h]["nombre"] or h) for h in store}
for h, i, gid, url, alt, hu in gal:
    fich = url.split("/")[-1].split("?")[0].lower()
    pref = re.sub(r"-\d+\.[a-z0-9]+$", "", fich)
    if pref != h:
        raros.append((h, i, fich, alt[:60], "fichero de otro animal"))
        continue
    for h2, n2 in nombres.items():
        if h2 != h and n2 and len(n2) > 3 and re.search(r"\b" + re.escape(n2) + r"\b", plano(alt)):
            if not re.search(r"\b" + re.escape(nombres[h]) + r"\b", plano(alt)):
                raros.append((h, i, fich, alt[:60], "el alt nombra a %s" % h2))
                break
L.append("")
L.append("fotos cuyo fichero o alt no cuadra con el animal: %d" % len(raros))
for x in raros:
    L.append("  %-18s #%d %-28s alt=[%s]  %s" % x)
R["raros"] = raros

# ---------------------------------------------------------------- D. zips no usadas
sec("D. FOTOS DE LOS ZIPS DE ANIMALES QUE NO ESTÁN EN NINGUNA GALERÍA")
huellas_tienda = {hu for _, _, _, _, _, hu in gal if hu}
zips_animales = [z for z in zh if re.search(r"FOTOS (GATOS|LOS|PERR|WEB)|Bimba|Cacahuete|EXTREME|LEWANDOWSKI", z["zip"])]
no_usadas = [z for z in zips_animales if not any(distancia(z["huella"], hu) <= 6 for hu in huellas_tienda)]
por_zip = collections.Counter(z["zip"] for z in no_usadas)
L.append("fotos en zips de animales: %d   sin usar en ninguna galería: %d" % (len(zips_animales), len(no_usadas)))
for z, n in sorted(por_zip.items()):
    L.append("  %-42s %d" % (z, n))
sueltas = [z for z in zips if not z["zip"] and z.get("huella")]
no_clas = [z for z in no_usadas if not any(distancia(z["huella"], s_["huella"]) <= 4 for s_ in sueltas)]
L.append("de esas, ya copiadas y clasificadas en _sin_dueno: %d   NO clasificadas: %d" % (len(no_usadas) - len(no_clas), len(no_clas)))
for z in no_clas:
    L.append("  %-40s %s" % (z["zip"][:40], z["ruta"]))
R["no_usadas"] = [z["zip"] + "|" + z["ruta"] for z in no_usadas]
R["no_clasificadas"] = [z["zip"] + "|" + z["ruta"] for z in no_clas]

# ---------------------------------------------------------------- E. biblioteca
sec("E. BIBLIOTECA DE ARCHIVOS: ¿QUIÉN USA CADA FICHERO?")
usados = collections.defaultdict(set)
for h, i, gid, url, alt, hu in gal:
    usados[gid].add("galería " + h)
for a in albs:
    c = {f["key"]: f.get("value") for f in a["fields"]}
    if c.get("portada"):
        usados[c["portada"]].add("portada " + a["handle"])
for p in prods:
    for m in p["media"]["nodes"]:
        if m and m.get("id"):
            usados[m["id"]].add("producto " + p["handle"])
arch = tienda["archivos"]


def nombre_arch(f):
    u = (f.get("image") or {}).get("url") or f.get("url") or f.get("filename") or ""
    return u.split("/")[-1].split("?")[0]


sin_uso = [f for f in arch if f["id"] not in usados]
fallidos = [f for f in arch if f.get("fileStatus") not in ("READY", None)]
L.append("archivos en la biblioteca: %d   usados por galerías/portadas/productos: %d   sin uso conocido: %d   con estado raro: %d" % (
    len(arch), len([f for f in arch if f["id"] in usados]), len(sin_uso), len(fallidos)))
grupos_su = collections.Counter()
for f in sin_uso:
    n = nombre_arch(f)
    clave = ("foto de animal" if re.match(r"^[a-z0-9-]+-\d+\.(jpe?g|png)$", n) else
             "portada de album" if n.startswith("album-") else
             "tienda/producto" if re.search(r"loveanimals|camiseta|sudadera|totebag|lab|catalogo|mockup|adoptaresvida|taza|funda", n, re.I) else
             "logo/tema" if re.search(r"logo|favicon|\.svg$", n, re.I) else "otro")
    grupos_su[clave] += 1
L.append("  sin uso, por tipo: " + ", ".join("%s=%d" % kv for kv in grupos_su.most_common()))
for f in sin_uso:
    n = nombre_arch(f)
    if re.match(r"^[a-z0-9-]+-\d+\.(jpe?g|png)$", n) or n.startswith("album-"):
        L.append("  SIN USO %-45s %s %s" % (n, f["createdAt"][:10], f["id"].split("/")[-1]))
otros = [nombre_arch(f) for f in sin_uso if not (re.match(r"^[a-z0-9-]+-\d+\.(jpe?g|png)$", nombre_arch(f)) or nombre_arch(f).startswith("album-"))]
L.append("  el resto sin uso (%d), muestra: %s" % (len(otros), otros[:25]))
R["sin_uso"] = [(nombre_arch(f), f["id"], f["createdAt"][:10]) for f in sin_uso]
for f in fallidos:
    L.append("  ESTADO %s %s" % (f.get("fileStatus"), nombre_arch(f)))

# ---------------------------------------------------------------- F. productos
sec("F. PRODUCTOS: FOTOS")
activos = [p for p in prods if p["status"] == "ACTIVE"]
sin_img = [p["handle"] for p in activos if not p["media"]["nodes"]]
L.append("productos activos: %d   sin ninguna foto: %d %s" % (len(activos), len(sin_img), sin_img))
por_media = collections.defaultdict(list)
for p in activos:
    for m in p["media"]["nodes"]:
        if m and m.get("id"):
            por_media[m["id"]].append(p["handle"])
comp = {k: v for k, v in por_media.items() if len(v) > 1}
L.append("fotos compartidas entre productos (mismo fichero): %d" % len(comp))
for k, v in comp.items():
    L.append("  %s -> %s" % (k.split("/")[-1], v))
sin_alt = [p["handle"] for p in activos if p["media"]["nodes"] and not any((m.get("alt") or "").strip() for m in p["media"]["nodes"] if m)]
L.append("productos activos con todas las fotos sin alt: %d" % len(sin_alt))

io.open("cruce_fotos.txt", "w", encoding="utf-8").write("\n".join(L))
json.dump(R, io.open("cruce_fotos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("lineas:", len(L))
