# -*- coding: utf-8 -*-
"""Copia a la tienda REAL la estructura de metaobjetos de la de pruebas.

Solo la estructura: ni una entrada (los datos llegan con el Excel de Carla).
Idempotente: si la definición ya existe, la deja como está y avisa.
"""
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

ADMIN_EQUIV = {
    "PUBLIC_READ_WRITE": "MERCHANT_READ_WRITE",
    "PUBLIC_READ": "MERCHANT_READ",
    "MERCHANT_READ_WRITE": "MERCHANT_READ_WRITE",
    "MERCHANT_READ": "MERCHANT_READ",
}

DEV = ("test-shop-kv2uh85k.myshopify.com", os.environ.get("LA_TOKEN_DEV", ""))
REAL = ("loveanimalsbcn.myshopify.com", os.environ.get("LA_TOKEN_REAL", ""))


def gql(tienda, q, v=None):
    dominio, token = tienda
    req = urllib.request.Request(
        "https://%s/admin/api/2026-01/graphql.json" % dominio,
        data=json.dumps({"query": q, "variables": v or {}}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read().decode())
    if "errors" in d:
        raise RuntimeError(json.dumps(d["errors"], ensure_ascii=False)[:400])
    return d["data"]


Q_DEFS = """
{
  metaobjectDefinitions(first: 20) {
    nodes {
      id type name description displayNameKey
      access { admin storefront }
      capabilities {
        publishable { enabled }
        translatable { enabled }
        renderable { enabled data { metaTitleKey metaDescriptionKey } }
        onlineStore { enabled data { urlHandle } }
      }
      fieldDefinitions {
        key name description required type { name }
        validations { name value }
      }
    }
  }
}
"""

M_CREATE = """
mutation($definition: MetaobjectDefinitionCreateInput!) {
  metaobjectDefinitionCreate(definition: $definition) {
    metaobjectDefinition { id type name fieldDefinitions { key } }
    userErrors { field message code }
  }
}
"""


def a_input(defi, mapa_ids):
    """Convierte una definición leída en un input de creación."""
    campos = []
    for f in defi["fieldDefinitions"]:
        val = []
        for v in f["validations"]:
            if v["value"] is None:
                continue
            valor = v["value"]
            # las referencias entre metaobjetos apuntan a ids de la otra tienda
            if v["name"] == "metaobject_definition_id" and valor in mapa_ids:
                valor = mapa_ids[valor]
            val.append({"name": v["name"], "value": valor})
        campo = {
            "key": f["key"],
            "name": f["name"],
            "required": f["required"],
            "type": f["type"]["name"],
        }
        if f.get("description"):
            campo["description"] = f["description"]
        if val:
            campo["validations"] = val
        campos.append(campo)

    caps = defi["capabilities"]
    capacidades = {
        "publishable": {"enabled": caps["publishable"]["enabled"]},
        "translatable": {"enabled": caps["translatable"]["enabled"]},
    }
    if caps["renderable"]["enabled"]:
        datos = caps["renderable"]["data"] or {}
        capacidades["renderable"] = {"enabled": True, "data": {
            "metaTitleKey": datos.get("metaTitleKey"),
            "metaDescriptionKey": datos.get("metaDescriptionKey"),
        }}
    if caps["onlineStore"]["enabled"]:
        datos = caps["onlineStore"]["data"] or {}
        capacidades["onlineStore"] = {"enabled": True, "data": {"urlHandle": datos.get("urlHandle")}}

    entrada = {
        "type": defi["type"],
        "name": defi["name"],
        "displayNameKey": defi["displayNameKey"],
        # el acceso de admin solo se puede fijar en tipos reservados de app: aquí solo storefront
        "access": {"storefront": defi["access"]["storefront"]},
        "capabilities": capacidades,
        "fieldDefinitions": campos,
    }
    if defi.get("description"):
        entrada["description"] = defi["description"]
    return entrada


def main():
    origen = {n["type"]: n for n in gql(DEV, Q_DEFS)["metaobjectDefinitions"]["nodes"]}
    destino = {n["type"]: n for n in gql(REAL, Q_DEFS)["metaobjectDefinitions"]["nodes"]}
    print("en pruebas:", sorted(origen), "| en la real:", sorted(destino) or "ninguna")

    mapa_ids = {}
    # el animal primero: el álbum le apunta
    for tipo in ["animal", "album"]:
        if tipo not in origen:
            continue
        if tipo in destino:
            print("  =", tipo, "ya existe en la real:", destino[tipo]["id"])
            mapa_ids[origen[tipo]["id"]] = destino[tipo]["id"]
            continue
        entrada = a_input(origen[tipo], mapa_ids)
        res = gql(REAL, M_CREATE, {"definition": entrada})["metaobjectDefinitionCreate"]
        if res["userErrors"]:
            print("  !!", tipo, json.dumps(res["userErrors"], ensure_ascii=False)[:300])
            continue
        nueva = res["metaobjectDefinition"]
        mapa_ids[origen[tipo]["id"]] = nueva["id"]
        print("  +", tipo, "→", nueva["id"], "(%d campos)" % len(nueva["fieldDefinitions"]))

    print("\ncomprobación en la tienda real:")
    for n in gql(REAL, Q_DEFS)["metaobjectDefinitions"]["nodes"]:
        caps = n["capabilities"]
        print("   %-8s %-8s campos=%-3d url=%s publicable=%s" % (
            n["type"], n["name"], len(n["fieldDefinitions"]),
            (caps["onlineStore"]["data"] or {}).get("urlHandle") if caps["onlineStore"]["enabled"] else "-",
            caps["publishable"]["enabled"]))


if __name__ == "__main__":
    main()
