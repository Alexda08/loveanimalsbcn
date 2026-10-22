# -*- coding: utf-8 -*-
"""Ejemplo real (22-10-2026): alta de dos fichas sueltas, Chiquitita y Katsuki.

Sirve de plantilla para dar de alta a mano uno o dos animales sin pasar por
todo el circuito del Excel: sube las fotos (stagedUploadsCreate + fileCreate),
crea el metaobjeto publicado con todos sus campos y lo añade al final de
`animales_mas` del álbum Gatos (la primera lista, `animales`, ya tenía 50).

Antes de relanzarlo, cambia la lista ANIMALES y el álbum; las fotos se leen de
la carpeta D. Crear dos veces el mismo handle falla (no duplica).
"""
import json, os, time, urllib.request, uuid
from gql import gql
D = "gatos/"
ANIMALES = [
 dict(handle="chiquitita", nombre="Chiquitita", frase="La más pequeñita del refugio", fecha="2025-07-02",
      edad="2 años", sexo="hembra", ninos="consultar", perros="consultar", gatos="si",
      caracter=["tierna","adorable","tímida"],
      historia="Chiquitita es una gatita muy pequeñita de tamaño pese a que ya no es cachorra, de ahí su nombre. Llegó procedente de un decomiso por vivir en malas condiciones junto con otras gatas que ya fueron adoptadas. Ella quedó atrás porque era la más miedosa. Pero nosotras vimos algo más: también era la más tierna, la que más ayuda necesitaba, la más sensible, la más resiliente. A pesar de ser miedosa, tiene buen carácter y no hace un mal gesto. No se adapta a vivir en la gatera por lo que tiene que estar en jaulita y, aunque parezca peor, ella está más tranquila. Se lleva bien con otros gatos pero el estrés de la gatera fue demasiado para ella. Busca un hogar tranquilo, lleno de paz y amor.",
      posts=["https://www.instagram.com/p/DQxASBViKH0/"],
      fotos=["gato-2-atigrado-dorado__GATOS__IMG_0494.jpeg","gato-2-atigrado-dorado__GATOS__IMG_0500.jpeg","gato-2-atigrado-dorado__GATOS__IMG_0502.jpeg","gato-2-atigrado-dorado__GATOS__IMG_0511.jpeg"]),
 dict(handle="katsuki", nombre="Katsuki", frase="La ninja de los premios", fecha="2022-09-09",
      edad="6 años", sexo="hembra", ninos="consultar", perros="consultar", gatos="si",
      caracter=["menudita","juguetona","glotona"],
      historia="Katsuki llegó súper asustada y se escondía mucho, le llevó un tiempo empezar a dejarse ver pero cuando lo hizo descubrimos a un encanto de gatita, adorable. Empezó a interactuar con nosotras mediante el juego y los premios que LE ENCANTAN. Estamos seguras de que si en la gatera ha avanzado en un hogar lo hará mucho más pero, obviamente, necesita paciencia y empatía. Ya ha sido adoptada y devuelta una vez. No merece más decepciones pero tú que lees esto seguro que eres una familia súper guay. Le iría genial tener otros hermanos gatos.",
      posts=["https://www.instagram.com/p/CoeZt85ILVB/"],
      fotos=["gato-5-blanco-manchita__GATOS__IMG_3080.jpeg"]),
]

def sube(path, nombre, alt):
    data = open(path, "rb").read()
    t = gql("""mutation($i:[StagedUploadInput!]!){stagedUploadsCreate(input:$i){stagedTargets{url resourceUrl parameters{name value}} userErrors{message}}}""",
            {"i":[{"filename":nombre,"mimeType":"image/jpeg","resource":"IMAGE","httpMethod":"POST","fileSize":str(len(data))}]})["stagedUploadsCreate"]["stagedTargets"][0]
    b = uuid.uuid4().hex; body = b""
    for p in t["parameters"]:
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n".encode()
    body += f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{nombre}\"\r\nContent-Type: image/jpeg\r\n\r\n".encode() + data + f"\r\n--{b}--\r\n".encode()
    urllib.request.urlopen(urllib.request.Request(t["url"], data=body, headers={"Content-Type": f"multipart/form-data; boundary={b}"}))
    f = gql("""mutation($f:[FileCreateInput!]!){fileCreate(files:$f){files{id} userErrors{message}}}""",
            {"f":[{"originalSource":t["resourceUrl"],"contentType":"IMAGE","alt":alt,"filename":nombre}]})["fileCreate"]
    assert not f["userErrors"], f
    return f["files"][0]["id"]

ids = []
for a in ANIMALES:
    alt = f"{a['nombre']}, gato en adopción en Love Animals BCN"
    media = [sube(D+f, f"{a['handle']}-{i}.jpg", alt) for i, f in enumerate(a["fotos"], 1)]
    hist = json.dumps({"type":"root","children":[{"type":"paragraph","children":[{"type":"text","value":a["historia"]}]}]}, ensure_ascii=False)
    campos = {"nombre":a["nombre"],"frase":a["frase"],"galeria":json.dumps(media),"fecha_entrada":a["fecha"],"edad":a["edad"],
              "sexo":a["sexo"],"convive_ninos":a["ninos"],"convive_perros":a["perros"],"convive_gatos":a["gatos"],
              "historia":hist,"caracter":json.dumps(a["caracter"],ensure_ascii=False),"estado":"en_adopcion",
              "posts_instagram":json.dumps(a["posts"])}
    r = gql("""mutation($m:MetaobjectCreateInput!){metaobjectCreate(metaobject:$m){metaobject{id handle} userErrors{field message}}}""",
            {"m":{"type":"animal","handle":a["handle"],"capabilities":{"publishable":{"status":"ACTIVE"}},
                  "fields":[{"key":k,"value":v} for k,v in campos.items()]}})["metaobjectCreate"]
    print(r); ids.append(r["metaobject"]["id"])

g = gql('{g: metaobjectByHandle(handle:{type:"album",handle:"gatos"}){id b:field(key:"animales_mas"){value}}}')["g"]
mas = json.loads(g["b"]["value"]) + [i for i in ids if i not in g["b"]["value"]]
r = gql("""mutation($id:ID!,$m:MetaobjectUpdateInput!){metaobjectUpdate(id:$id,metaobject:$m){metaobject{id} userErrors{message}}}""",
        {"id":g["id"],"m":{"fields":[{"key":"animales_mas","value":json.dumps(mas)}]}})
print(r, len(mas))
