# -*- coding: utf-8 -*-
"""Vuelca todas las fichas `animal` de la tienda real a tienda_fichas.json. Solo lee.

Es la entrada de insta_extract.py (y sirve de foto fija antes de tocar nada).

    LA_TOKEN_REAL=... python vuelca_fichas.py
"""
import json, sys
from gql import gql

sys.stdout.reconfigure(encoding="utf-8")
Q = """query($c:String){metaobjects(type:"animal",first:250,after:$c){
  pageInfo{hasNextPage endCursor}
  nodes{id handle capabilities{publishable{status}} fields{key value}}}}"""

animales, cursor = [], None
while True:
    r = gql(Q, {"c": cursor})["metaobjects"]
    animales += r["nodes"]
    if not r["pageInfo"]["hasNextPage"]:
        break
    cursor = r["pageInfo"]["endCursor"]
json.dump({"animales": animales}, open("tienda_fichas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
pub = sum(a["capabilities"]["publishable"]["status"] == "ACTIVE" for a in animales)
print(f"{len(animales)} fichas ({pub} publicadas) -> tienda_fichas.json")
