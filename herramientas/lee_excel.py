# -*- coding: utf-8 -*-
"""Lee el Excel de Carla y lo deja normalizado en fichas.json. No toca ninguna tienda."""
import openpyxl, json, os, re, unicodedata, zipfile, glob, difflib, collections, datetime

RAIZ = r"C:\Users\desca\OneDrive\Desktop\loveanimalsbcn"
XLSX = os.path.join(RAIZ, "docs", "Love Animals BCN - fichas de los animales.xlsx")
IMGS = os.path.join(RAIZ, "docs", "img_loveanimalsbcn")
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fichas.json")

# titulo, subtitulo, urgente, anio
ALBUMES = [
    ("NECESITAMOS CASA DE ACOGIDA", "los que no pueden esperar más", True,  None),
    ("ABUELOS",                     "sabiduría y siestas",           False, None),
    ("LOS MÁS VETERANOS",           "los que más llevan esperando",  False, None),
    ("PPP JÓVENES",                 "energía con etiqueta injusta",  False, None),
    ("PPP ADULTOS",                 "caballeros con corazón grande", False, None),
    ("MESTIZOS",                    "únicos e irrepetibles",         False, None),
    ("GATOS",                       "ronroneos buscando sofá",       False, None),
    ("DESDE 2021 ESPERANDO FAMILIA", "los que más años acumulan",    False, 2021),
    ("DESDE 2022 ESPERANDO FAMILIA", "aún sin su oportunidad",       False, 2022),
    ("DESDE 2023 ESPERANDO FAMILIA", "siguen contando los días",     False, 2023),
    ("DESDE 2024 ESPERANDO FAMILIA", "y los que vayan llegando…",    False, 2024),
]
# El zip «GATO EXTREME FILA 147.zip» dice a quien pertenece en su propio nombre:
# fila 147 del Excel es Extreme, y su celda de Fotos vino vacia.
FOTOS_A_MANO = {149: ["IMG_1414", "IMG_1415", "IMG_1416"]}

# Lo que Carla corrigio por WhatsApp el 03-09-2026, ya con el Excel entregado.
# Su fichero no se toca: las decisiones viven aqui, cada una con su motivo. La
# clave es la fila del Excel, que es lo unico que no se mueve cuando ella edita.
BAJAS = {
    5:   "adoptado esta semana",
    58:  "adoptado esta semana",
    99:  "adoptada esta semana",
    161: "adoptado esta semana",
    169: "adoptado esta semana",
    170: "adoptado esta semana",
    179: "adoptado esta semana",
    180: "adoptado esta semana",
    196: "adoptado esta semana",
    206: "adoptada esta semana",
    178: "falleció de panleucopenia (Muso)",
}
# Sakura resulto ser la misma gata que «Nina (abuelita)», con dos nombres
DUPLICADOS = {219: "es la misma que Nina (abuelita)"}
# y aqui al reves: el «NO PONERLO» se quedo de cuando la ficha era solo Bibi
DENTRO = {218: "Bibi & Sepi, adopcion conjunta: Carla la quiere publicada"}

# Tres nombres se repiten en el Excel, y son animales distintos de verdad: un
# perro PPP y un gato que se llaman Balder, otro perro y otra gata que se llaman
# Peque, y dos Zeus PPP de distinta edad. El «-2» se lo llevaba el que apareciera
# despues en la hoja, asi que bastaba con que Carla moviera una fila para que se
# intercambiaran las URLs — y, como el alta va por handle, para que uno pisara
# los datos del otro. Aqui va clavado por fecha de entrada, que es del animal y
# no del sitio que ocupe en el Excel.
HANDLES = {
    ("balder", "2020-02-13"): "balder-2",   # el gato
    ("peque", "2020-05-31"): "peque-2",     # la gata
    ("zeus", "2025-09-10"): "zeus-2",       # el PPP joven
}

# Casillas que el Excel trae mal y Carla ha confirmado por WhatsApp. Se corrigen
# aqui, sobre la fila, sin tocar su fichero.
CORRIGE = {
    64: {"ppp": "Sí"},   # Papaya: la movio a «PPP ADULTOS» y la casilla PPP se quedo en No
}

TAMANOS = {"pequeno": "Pequeño", "mediano": "Mediano", "grande": "Grande"}
ESTADOS = {"en adopcion": "en_adopcion", "en acogida": "en_acogida", "adoptado": "adoptado"}
SINO    = {"si": "si", "no": "no", "consultar": "consultar"}


def sin_tildes(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()


def clave(s):
    """Para comparar textos sin que estorben tildes, mayusculas ni espacios de mas."""
    return re.sub(r"\s+", " ", sin_tildes(s)).strip().lower()


def nfc(s):
    """Los zips vienen de un Mac: las tildes llegan descompuestas (NFD)."""
    return unicodedata.normalize("NFC", str(s)).strip().lower()


def handle(nombre, entrada, vistos, avisos):
    h = re.sub(r"[^a-z0-9]+", "-", sin_tildes(nombre).lower()).strip("-") or "animal"
    fijo = HANDLES.get((h, entrada))
    if fijo:
        h = fijo
    elif h in vistos:
        # choque nuevo: que se entere alguien antes de que dos fichas se pisen
        base, n = h, 2
        while h in vistos:
            h = "%s-%d" % (base, n)
            n += 1
        avisos.append("%s: el nombre ya estaba cogido, queda como «%s». Fijalo en HANDLES"
                      % (nombre, h))
    vistos.add(h)
    return h


# ---------------------------------------------------------------- fotos en disco
def indice_de_fotos():
    """basename sin extension (NFC, minusculas) -> [(zip, ruta dentro del zip)]"""
    idx = collections.defaultdict(list)
    for z in sorted(glob.glob(os.path.join(IMGS, "*.zip"))):
        with zipfile.ZipFile(z) as f:
            for i in f.infolist():
                b = os.path.basename(i.filename)
                if i.is_dir() or b.startswith("._") or "__MACOSX" in i.filename:
                    continue
                idx[nfc(os.path.splitext(b)[0])].append((os.path.basename(z), i.filename))
    for p in glob.glob(os.path.join(IMGS, "*.*")):
        if os.path.splitext(p)[1].lower() in (".png", ".jpg", ".jpeg"):
            idx[nfc(os.path.splitext(os.path.basename(p))[0])].append(("(suelto)", os.path.basename(p)))
    return idx


def laxa(k):
    """Carla copio los UUID a mano: la O y el 0 se confunden, y algun caracter se cae."""
    return k.replace("-", "").replace("o", "0").replace("i", "1").replace("l", "1").replace("s", "5")


def fotos_de(celda, idx, lax, avisos, nombre):
    trozos = [t.strip() for t in str(celda or "").replace("\n", ",").replace(";", ",").split(",")]
    juntos, i = [], 0
    while i < len(trozos):
        t = trozos[i]
        if not t:
            i += 1
            continue
        if nfc(os.path.splitext(t)[0]) in idx:
            juntos.append(t)
            i += 1
            continue
        # hay nombres de fichero con coma dentro (un «Sin titulo (1080 x 1440 px)» y similares)
        if i + 1 < len(trozos) and nfc(os.path.splitext(", ".join([t, trozos[i + 1]]))[0]) in idx:
            juntos.append(", ".join([t, trozos[i + 1]]))
            i += 2
            continue
        juntos.append(t)
        i += 1

    encontradas, perdidas = [], []
    for t in juntos:
        k = nfc(os.path.splitext(t)[0])
        # y a alguno se le ha caido el punto de la extension: «IMG_6522jpeg»
        if k not in idx:
            k = re.sub(r"(jpe?g|png|heic)$", "", k).strip() or k
        if k in idx:
            if k not in encontradas:
                encontradas.append(k)
            continue
        cand = lax.get(laxa(k))
        if not cand:
            cerca = difflib.get_close_matches(laxa(k), list(lax), n=1, cutoff=0.90)
            cand = lax[cerca[0]] if cerca else None
        if cand:
            avisos.append("%s: «%s» no existe, uso %s" % (nombre, t, idx[cand[0]][0][1]))
            if cand[0] not in encontradas:
                encontradas.append(cand[0])
        else:
            perdidas.append(t)
    return encontradas, perdidas


# ---------------------------------------------------------------- albumes
def albumes_de(celda, avisos, nombre):
    titulos, indice = [], {clave(t): t for t, _, _, _ in ALBUMES}
    for trozo in str(celda or "").split(";"):
        t = trozo.strip()
        if not t:
            continue
        bueno = indice.get(clave(t))
        if bueno is None:                                  # «DESDE 2021 ESPERANDO» sin el «FAMILIA»
            m = re.search(r"(\d{4})", clave(t))
            if m and "esperando" in clave(t):
                bueno = indice.get("desde %s esperando familia" % m.group(1))
        if bueno is None:
            cerca = difflib.get_close_matches(clave(t), list(indice), n=1, cutoff=0.75)
            bueno = indice[cerca[0]] if cerca else None
        if bueno is None:
            avisos.append("%s: álbum desconocido «%s»" % (nombre, t))
            continue
        if clave(bueno) != clave(t):
            avisos.append("%s: álbum «%s» -> «%s»" % (nombre, t, bueno))
        if bueno not in titulos:
            titulos.append(bueno)
    return titulos


def texto(v):
    return re.sub(r"\s+", " ", str(v)).strip() if v not in (None, "") else ""


def fecha(v):
    if isinstance(v, datetime.datetime):
        return v.date().isoformat()
    if isinstance(v, datetime.date):
        return v.isoformat()
    if v in (None, ""):
        return ""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", str(v))
    return m.group(0) if m else ""


def main():
    idx = indice_de_fotos()
    lax = collections.defaultdict(list)
    for k in idx:
        lax[laxa(k)].append(k)

    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb["Animales"]
    COLS = ["n", "nombre", "album", "estado", "entrada", "adopcion", "sexo", "edad", "tamano",
            "ppp", "ninos", "perros", "gatos", "caracter", "frase", "historia", "fotos", "notas", "cod"]

    avisos, fuera, animales, vistos = [], [], [], set()
    for r in range(3, ws.max_row + 1):
        v = {k: ws.cell(r, i + 1).value for i, k in enumerate(COLS)}
        v.update(CORRIGE.get(r, {}))
        nombre = texto(v["nombre"])
        if not nombre:
            continue
        if r in BAJAS or r in DUPLICADOS:
            fuera.append({"fila": r, "nombre": nombre, "baja": r in BAJAS,
                          "nota": BAJAS.get(r) or DUPLICADOS[r]})
            continue
        # Carla marca en «Notas» los que no quiere en la web
        if r not in DENTRO and re.search(r"\bno\s+pon(er|erlo|erla|gais|ga)\b", clave(v["notas"] or "")):
            fuera.append({"fila": r, "nombre": nombre, "nota": texto(v["notas"])[:150]})
            continue
        # la fecha de entrada es obligatoria en la definicion y la web cuenta los dias
        # que llevan esperando: sin ella la ficha no se puede crear ni inventar
        if not fecha(v["entrada"]):
            fuera.append({"fila": r, "nombre": nombre, "nota": "sin fecha de entrada"})
            continue

        celda = v["fotos"] or ", ".join(FOTOS_A_MANO.get(r, []))
        enc, perdidas = fotos_de(celda, idx, lax, avisos, nombre)
        car = [c.strip() for c in re.split(r"[,;]", texto(v["caracter"])) if c.strip()]
        animales.append({
            "fila": r,
            "nombre": nombre,
            "handle": handle(nombre, fecha(v["entrada"]), vistos, avisos),
            "albumes": albumes_de(v["album"], avisos, nombre),
            "estado": ESTADOS.get(clave(v["estado"]), ""),
            "fecha_entrada": fecha(v["entrada"]),
            "fecha_adopcion": fecha(v["adopcion"]),
            "sexo": clave(v["sexo"]) if clave(v["sexo"]) in ("macho", "hembra") else "",
            "edad": texto(v["edad"]),
            "tamano": TAMANOS.get(clave(v["tamano"]), ""),
            "ppp": {"si": True, "no": False}.get(clave(v["ppp"])),
            "convive_ninos": SINO.get(clave(v["ninos"]), ""),
            "convive_perros": SINO.get(clave(v["perros"]), ""),
            "convive_gatos": SINO.get(clave(v["gatos"]), ""),
            "caracter": car,
            "frase": texto(v["frase"]),
            "historia": texto(v["historia"]),
            "fotos": enc,
            "fotos_perdidas": perdidas,
            "instagram": re.findall(r"https?://www\.instagram\.com/[^\s)]+", str(v["notas"] or "")),
        })

    usadas = set()
    for a in animales:
        usadas.update(a["fotos"])
    datos = {
        "animales": animales,
        "albumes": [{"titulo": t, "subtitulo": s, "es_urgente": u, "anio_espera": y} for t, s, u, y in ALBUMES],
        "fotos_en_disco": {k: idx[k][0] for k in idx},
        "fuera": fuera,
        "avisos": avisos,
    }
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)

    print("animales:", len(animales), "| excluidos por «NO PONERLO»:", len(fuera))
    print("handles unicos:", len(set(a["handle"] for a in animales)))
    print("fotos en disco:", len(idx), "| referenciadas:", len(usadas), "| huerfanas:", len(set(idx) - usadas))
    print("animales sin ninguna foto:", sum(1 for a in animales if not a["fotos"]))
    print("referencias rotas:", sum(len(a["fotos_perdidas"]) for a in animales))
    print("avisos:", len(avisos))
    print("->", SALIDA)


if __name__ == "__main__":
    main()
