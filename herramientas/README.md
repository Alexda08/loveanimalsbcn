# Herramientas: los scripts que han montado los datos de la tienda

Esto **no es parte del tema**: Shopify ignora esta carpeta. Son los scripts de Python con los que
se cargaron en la tienda real los animales, sus fotos, los posts de Instagram y algunos productos.
Se guardan aquí para que, cuando Carla mande otro Excel u otro zip de fotos, no haya que
reinventar nada.

> **De dónde salen.** Se escribieron sesión a sesión en una carpeta temporal y se recuperaron el
> 22-10-2026 del historial de trabajo, reaplicando cada cambio en orden. Trece salen exactos;
> a `crea_animales.py` y `clasifica_fotos.py` les faltan sus últimos retoques (lo avisan en su
> cabecera). Son los que se ejecutaron
> de verdad, pero algunos se hicieron para un momento concreto (un Excel con un formato, 208
> fichas, el álbum Gatos…). **Léelos antes de relanzarlos**, y lanza siempre primero el modo que
> solo mira.

## Antes de nada

- **Python 3** con `openpyxl` (`pip install openpyxl`). `huella.py` usa además `Pillow`.
- **El token nunca va escrito en un fichero.** Todos lo leen de una variable de entorno:
  - `LA_TOKEN_REAL`: token de la app de Admin API de `loveanimalsbcn.myshopify.com`.
  - `LA_TOKEN_DEV`: el de la tienda de pruebas `test-shop-kv2uh85k.myshopify.com` (solo
    `migra_metaobjetos.py`).
  Se pasa al lanzar: `LA_TOKEN_REAL=shpat_… python vuelca_fichas.py` (Git Bash) o
  `$env:LA_TOKEN_REAL='shpat_…'; python vuelca_fichas.py` (PowerShell). Alex tiene los tokens.
- **Se lanzan desde esta carpeta**: leen y escriben sus `.json` intermedios aquí al lado
  (`fichas.json`, `fotos.json`, `asignacion.json`, `tienda_fichas.json`…). Están en `.gitignore`:
  se regeneran.
- **Las fotos** viven en `docs/img_loveanimalsbcn/` (los zips de Carla, medio giga, fuera de git).
  Algunos scripts tienen la ruta del repo escrita (`RAIZ = C:\Users\desca\OneDrive\Desktop\…`):
  si cambia de sitio, se cambia arriba del fichero.
- API: **Admin GraphQL 2026-01**. Todo va por `handle`, así que relanzar actualiza en vez de
  duplicar.

## El circuito completo de los animales

Así se cargaron las 208 fichas. Para un animal suelto no hace falta nada de esto: se da de alta a
mano desde el admin (ver `docs/METAOBJETOS.md`) o con `fichas_nuevas.py`.

```
excel_animales.py      genera el Excel en blanco que rellena Carla
        │
        ▼  (Carla lo rellena y manda zips de fotos)
lee_excel.py           Excel  ->  fichas.json (normalizado; avisa de erratas y fotos que no encuentra)
        │
sube_fotos.py          zips   ->  Archivos de Shopify; fotos.json (foto -> GID) y asignacion.json (animal -> fotos)
        │
crea_animales.py       albumes  ->  animales  ->  enlaza  ->  publica   (y «indice» regenera docs/INDICE-ANIMALES.md)
        │
adoptados.py           los marcados ADOPTADO en el Excel -> estado «adoptado» (muro de finales felices)
        │
vuelca_fichas.py       foto fija de la tienda -> tienda_fichas.json
insta_extract.py       columna «Notas» del Excel -> insta_posts.json
aplica_posts_instagram.py   insta_posts.json -> campo posts_instagram de cada ficha
```

### Uno por uno

| Script | Qué hace | Toca la tienda | Cómo se lanza |
|---|---|---|---|
| `gql.py` | La llamada al Admin GraphQL que usan los demás (`from gql import gql`). | — | — |
| `migra_metaobjetos.py` | Copia las **definiciones** `animal` y `album` de la tienda de pruebas a la real. Solo estructura, ninguna entrada. Ya está hecho: hoy solo sirve para montar otra tienda. | Sí (crea definiciones) | `python migra_metaobjetos.py` |
| `excel_animales.py` | Genera el Excel en blanco para Carla, con una fila de ejemplo y comentarios en cada columna. La última columna guarda el código de la ficha: es lo que permite reimportar sin duplicar. | No | `python excel_animales.py` |
| `lee_excel.py` | Lee el Excel de Carla (`docs/Love Animals BCN - fichas de los animales.xlsx`) y lo deja en `fichas.json`: nombres, fechas, sexo, convivencias, carácter, historia, álbumes, fotos. Arriba del fichero viven las decisiones de Carla por WhatsApp que **no** están en su Excel, cada una con su motivo y por número de fila: `BAJAS` (adoptados y fallecidos), `DUPLICADOS`, `DENTRO` (un «NO PONERLO» que sí va), `HANDLES` (los nombres repetidos, clavados por fecha) y `CORRIGE`; más `ALBUMES` y `FOTOS_A_MANO`. Su fichero no se edita nunca. | No | `python lee_excel.py` |
| `audita_excel.py` | Coteja el Excel con lo que Carla ha ido diciendo por WhatsApp y avisa donde no cuadra. | No | `python audita_excel.py` |
| `sube_fotos.py` | Saca las fotos de los zips (cada álbum tiene su zip: `ZIP_DE_ALBUM`), las sube a Archivos y apunta qué GID tiene cada una. Se puede cortar y seguir. | Sí (sube ficheros) | `prueba` · `subir` · `estado` |
| `crea_animales.py` | Da de alta álbumes y fichas, con su galería, y mete cada animal en sus álbumes. Crea **en borrador**; `publica` los pasa a publicados. `sobran` lista lo que está en la tienda y ya no toca; `baja` lo pasa a borrador. **⚠️ No relanzarlo sobre la tienda de hoy** (despublicaría, pisaría el orden de los álbumes y no conoce `animales_mas`): ver `docs/METAOBJETOS.md` §8. | Sí | `albumes` · `animales` · `enlaza` · `sobran` · `baja` · `limpia` (borra de verdad: no usar) · `indice` · `publica` |
| `adoptados.py` | Los adoptados del Excel del 04-10-2026: estado `adoptado`, publicados (Liquid no ve borradores), los que faltaban creados y metidos en su álbum. No inventa fechas de adopción. | Sí | `mirar` · `aplicar` |
| `sin_dueno.py` | Saca de los zips a `docs/img_loveanimalsbcn/_sin_dueno/` las fotos que no reclama ningún animal, con el zip de origen delante del nombre. | No (escribe en disco) | `python sin_dueno.py` |
| `clasifica_fotos.py` | Lista esas fotos sin dueño en grupos: de un animal que se quedó fuera, toma de más de uno publicado, material de la tienda, vídeos, y **sin pista** (las únicas que hay que preguntar a Carla). Las subcarpetas `1-de-quien-es/`, `2-para-la-tienda/`… y su `LEEME.txt` salen de este reparto. | No | `python clasifica_fotos.py` |
| `hoja.py` | Hoja de contactos de las fotos sin dueño (`_todas-juntas.jpg`), para mirarlas de un vistazo o mandárselas a Carla. Necesita Pillow. | No | `python hoja.py` |
| `huella.py` | Huella visual (dHash) para reconocer la misma foto aunque cambie de nombre, tamaño o compresión. La usa `cruce_fotos.py`. Necesita Pillow. | — | — |
| `cruce_fotos.py` | La auditoría grande: Excel ↔ fichas ↔ zips ↔ galerías ↔ Archivos. Deja `cruce_fotos.txt`. Necesita volcados previos de la tienda. | No | `python cruce_fotos.py` |
| `vuelca_fichas.py` | Vuelca todas las fichas a `tienda_fichas.json`. Hazlo antes de cualquier cambio masivo: es la copia para comparar o deshacer. | No | `python vuelca_fichas.py` |
| `insta_extract.py` <a id="instagram"></a> | Saca los enlaces de Instagram de la columna «Notas» del Excel, los casa con cada ficha por nombre + fecha de entrada y los normaliza. Necesita `excel_nuevo.xlsx` (copia del Excel de Carla) y `tienda_fichas.json` aquí al lado. | No | `python insta_extract.py` |
| `aplica_posts_instagram.py` | Escribe `posts_instagram` en cada ficha desde `insta_posts.json`. Sin argumento solo enseña qué cambiaría. | Sí | `python aplica_posts_instagram.py [aplicar]` |
| `fichas_nuevas.py` | El alta a mano de Chiquitita y Katsuki (22-10-2026): sube fotos, crea la ficha **publicada** y la añade al final de `animales_mas` del álbum Gatos. Plantilla para altas sueltas. | Sí | cambia la lista `ANIMALES` y `python fichas_nuevas.py` |

### Tienda solidaria

| Script | Qué hace | Cómo se lanza |
|---|---|---|
| `sube_galeria.py` | Sube las fotos de la franja de la tienda («gente con la ropa») como `tienda-NN`, con alt escrito a mano, para referenciarlas en la plantilla como `shopify://shop_images/tienda-NN.jpg`. | `mirar` · `subir` |
| `import_catalogo_pris.py` | Crea los productos del catálogo de El Armario de Pris (tazas, mochilas, fundas) con sus fotos. Hoy esos productos no se enseñan: «Otros productos» es una página de tarjetas (ver `docs/TIENDA.md`). | `python import_catalogo_pris.py` |
| `crea_adoptaresvida.py` | Camiseta y sudadera «Adoptar es vida», en borrador y luego publicadas. Las colecciones son automáticas por etiqueta: con poner `camiseta`/`sudadera` ya caen donde toca. | `crear` · `publicar` |

## Datos guardados

- `datos/insta_posts.json`: los 273 enlaces de Instagram que se cargaron el 22-10-2026 en 163
  fichas (`{handle: [url, …]}`; la primera URL es la del botón). El informe completo, con las 43
  fichas sin enlace y las filas que no casaron, está en `docs/INSTAGRAM-POSTS.md`.

## Trampas que ya han mordido

- **La lista `animales` de un álbum solo sirve 50 en Liquid.** Por eso cada álbum tiene una
  segunda lista, `animales_mas`. Al añadir: si `animales` tiene menos de 50, ahí; si no, al final
  de `animales_mas` (así lo hacen `adoptados.py` y `fichas_nuevas.py`).
- **Un metaobjeto en borrador no existe para Liquid.** Si un adoptado está en borrador, no sale en
  el muro de finales felices por mucho estado `adoptado` que tenga.
- **Las fotos del Excel no siempre dicen de quién son.** Cuando una ficha no tiene foto, la
  candidata está en `_sin_dueno/1-de-quien-es/`. La forma fiable de saber quién es: comparar con
  el post de Instagram del animal (`https://www.instagram.com/p/CODIGO/embed/` se ve sin sesión).
- **`/tmp` en Git Bash de Windows no es la carpeta temporal de Windows.** Usad rutas de esta
  carpeta.
- **Los JSON de las plantillas** (`templates/*.json`) empiezan con un comentario `/* … */` que
  hay que quitar antes de parsearlos con `json.loads`.
