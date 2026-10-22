# -*- coding: utf-8 -*-
"""Escribe en cada ficha el campo `posts_instagram` a partir de insta_posts.json.

insta_posts.json lo genera insta_extract.py ({handle: [url, ...]}, en orden: la
primera es la del botón «Su post en Insta», el resto salen como «Más posts»).
Sustituye la lista entera de cada ficha que aparezca; no toca las demás.

    LA_TOKEN_REAL=... python aplica_posts_instagram.py          solo enseña qué cambiaría
    LA_TOKEN_REAL=... python aplica_posts_instagram.py aplicar  lo escribe
"""
import json, sys
from gql import gql

sys.stdout.reconfigure(encoding="utf-8")
APLICAR = len(sys.argv) > 1 and sys.argv[1] == "aplicar"
posts = json.load(open("insta_posts.json", encoding="utf-8"))

cambios = 0
for handle, urls in posts.items():
    a = gql('query($h:String!){metaobjectByHandle(handle:{type:"animal",handle:$h}){id field(key:"posts_instagram"){value}}}',
            {"h": handle})["metaobjectByHandle"]
    if not a:
        print("  sin ficha:", handle)
        continue
    actual = json.loads((a["field"] or {}).get("value") or "[]")
    if actual == urls:
        continue
    cambios += 1
    print(f"  {handle}: {len(actual)} -> {len(urls)}")
    if APLICAR:
        r = gql('mutation($id:ID!,$m:MetaobjectUpdateInput!){metaobjectUpdate(id:$id,metaobject:$m){userErrors{field message}}}',
                {"id": a["id"], "m": {"fields": [{"key": "posts_instagram", "value": json.dumps(urls)}]}})
        if r["metaobjectUpdate"]["userErrors"]:
            print("    ERROR", r["metaobjectUpdate"]["userErrors"])
print(f"{cambios} fichas {'actualizadas' if APLICAR else 'cambiarían (añade «aplicar»)'}")
