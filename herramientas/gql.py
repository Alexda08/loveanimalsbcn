# -*- coding: utf-8 -*-
"""Llamada mínima al Admin GraphQL (2026-01) de la tienda real.

El token NUNCA va escrito: se lee de la variable de entorno LA_TOKEN_REAL.

    from gql import gql
    datos = gql("query($h:String!){...}", {"h": "katsuki"})

Devuelve `data`; si la API responde con `errors`, los imprime por stderr.
"""
import json, urllib.request, os, sys
TOKEN = os.environ["LA_TOKEN_REAL"]
def gql(q, v=None):
    req = urllib.request.Request("https://loveanimalsbcn.myshopify.com/admin/api/2026-01/graphql.json",
        data=json.dumps({"query": q, "variables": v or {}}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    r = json.load(urllib.request.urlopen(req))
    if r.get("errors"): print(json.dumps(r["errors"], indent=1), file=sys.stderr)
    return r.get("data")
