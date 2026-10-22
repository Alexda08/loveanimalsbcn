# Love Animals BCN — tema de Shopify

La web de **Love Animals BCN**, asociación animalista de Barcelona que da visibilidad a los perros
y gatos del CAACB y a sus propios rescates: **loveanimalsbcn.com**.

Es un tema **muy a medida** sobre **Horizon 4.1.3** de Shopify, hecho pro bono por Alex. Tiene dos
sistemas propios que no existen en ningún tema estándar:

- **Las fichas de animales y sus álbumes.** Cada perro o gato es un metaobjeto `animal` con su
  página (`/pages/animal/<nombre>`), agrupado en álbumes (`/pages/album/<álbum>`): días esperando
  familia, convivencias, historia, botones de adoptar/acoger, su post de Instagram, y un muro de
  finales felices con los adoptados. Unas 200 fichas, cargadas desde el Excel de la protectora.
- **Una tienda solidaria que no vende.** Los productos se enseñan, pero el pedido se hace por
  Instagram o WhatsApp a la artesana que los fabrica (El Armario de Pris); parte de cada pedido
  vuelve a la protectora.

## Antes de tocar nada

1. **`main` es el tema publicado.** Un push a `main` sale en vivo al instante, y lo que se cambie
   en el editor de temas lo commitea Shopify en `main`: `git pull` antes de empezar. Detalle en
   [`docs/OPERACION.md`](docs/OPERACION.md).
2. **Los datos no están en git**: animales, álbumes, productos, páginas y menús viven en la tienda.
   Se tocan desde el admin o con los scripts de [`herramientas/`](herramientas/README.md).
3. **Ningún token en el repo.** Ni en código, ni en docs, ni en commits.

## Documentación

| Doc | Qué cuenta |
|---|---|
| [`docs/OPERACION.md`](docs/OPERACION.md) | Cómo se publica y se prueba, tokens, contraseña de la tienda, trucos para verificar, trampas de Liquid/Horizon, pendientes. **Empieza aquí.** |
| [`docs/METAOBJETOS.md`](docs/METAOBJETOS.md) | **El sistema de animales**: definiciones `animal` y `album`, cómo lo pinta el tema, límites, y cómo hace Carla cada tarea desde el admin. |
| [`docs/TIENDA.md`](docs/TIENDA.md) | **La tienda solidaria**: modo escaparate, colecciones y píldoras, ficha de producto, «Otros productos», metacampos. |
| [`docs/SECCIONES.md`](docs/SECCIONES.md) | Catálogo de todas las secciones, bloques y snippets propios, y de lo que se ha cambiado de Horizon. Paleta de color. |
| [`herramientas/README.md`](herramientas/README.md) | Los scripts de Python que cargaron animales, fotos y posts de Instagram, y cómo relanzarlos. |
| [`docs/PAGINAS.md`](docs/PAGINAS.md) | **El diario del proyecto**: páginas, menús y cada ronda de cambios de Carla, con fecha, qué se hizo y por qué. |
| [`docs/INDICE-ANIMALES.md`](docs/INDICE-ANIMALES.md) | Índice de fichas y álbumes, quién se ha ido, quién falta y por qué. |
| [`docs/INSTAGRAM-POSTS.md`](docs/INSTAGRAM-POSTS.md) | Qué ficha tiene qué post de Instagram y cuáles no tienen ninguno. |
| [`docs/CONTENIDO-CARLA.md`](docs/CONTENIDO-CARLA.md) | Los textos oficiales de la protectora (adopción, acogida, licencia PPP, contacto). |
| [`docs/BLOG-VIEJO.md`](docs/BLOG-VIEJO.md) | Copia del blog de la web anterior, que se archivó. |

## Estructura

```
assets/  blocks/  config/  layout/  locales/  sections/  snippets/  templates/   ← el tema (Horizon + piezas propias)
templates/metaobject/animal.json, album.json                                     ← páginas de ficha y de álbum
docs/                                                                            ← documentación (Shopify la ignora)
docs/img_loveanimalsbcn/                                                         ← zips de fotos de Carla (fuera de git)
design/                                                                          ← maquetas HTML de referencia
herramientas/                                                                    ← scripts de datos (Shopify los ignora)
```

Las piezas propias tienen nombre en castellano (`animal-main`, `album-main`, `finales-felices`,
`chips-colecciones`, `otros-productos`…); lo que tiene nombre en inglés es de Horizon.

## Herramientas de desarrollo

- [Shopify CLI](https://shopify.dev/docs/storefronts/themes/tools/cli) para temas (`shopify theme dev`,
  `shopify theme push`, `shopify theme check`).
- Theme Check no corre solo en GitHub: hay que lanzarlo a mano (`shopify theme check`) antes de
  subir.

## Base y licencia

Basado en [Horizon](https://github.com/Shopify/horizon) de Shopify, Copyright (c) 2025-present
Shopify Inc. Ver [`LICENSE.md`](LICENSE.md). Las novedades de cada versión de Horizon están en
[`release-notes.md`](release-notes.md).
