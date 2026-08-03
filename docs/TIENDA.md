# Tienda solidaria — colecciones y ficha de producto

Cómo está montada la parte de tienda (colección + ficha) y qué hay que rellenar para
que un producto nuevo salga completo.

Diseños de referencia: `design/loveanimalsbcn-collections.html` y `design/loveanimalsbcn-pdp.html`.

---

## 1. Metacampos de producto (`custom.*`)

Todos son opcionales: lo que falta, no se pinta (la sección o el bloque desaparece solo).

| Clave | Tipo | Dónde sale | Ejemplo |
| --- | --- | --- | --- |
| `etiqueta` | texto | Sello sobre la foto en la tarjeta y etiqueta de la ficha | `Aniversario 2022` |
| `etiqueta_eco` | booleano | Pinta ese sello en verde | `true` |
| `tipo_prenda` | texto | Línea corta bajo el título en la tarjeta | `Camiseta · unisex y mujer` |
| `impacto_corto` | texto | Banda crema bajo la foto | `= 1 semana de pienso` |
| `impacto_icono` | texto | Icono de la caja de impacto | `🥣` |
| `impacto_frase` | texto largo | Caja granate de la ficha; lo que va entre `**dobles asteriscos**` sale en dorado | `Con esta camiseta pagas **una semana de pienso** para un perro grande.` |
| `claim` | texto | Frase en cursiva bajo el título de la ficha | `tres años haciendo posible lo imposible` |
| `eco_badge` | texto | Sello verde sobre la foto grande | `Algodón orgánico · Vegano` |
| `historia_fina` | texto | Entradilla de la sección de historia | `la historia detrás de este diseño` |
| `historia_titulo` | texto | Título grande de esa sección | `Tres años` |
| `historia_a` | texto largo | Párrafos (línea en blanco = párrafo nuevo) | |
| `historia_destacada` | texto largo | Frase grande centrada en cursiva (salto de línea = `<br>`) | |
| `historia_b` | texto largo | Párrafos de cierre | |
| `historia_firma` | texto | Firma | `— el equipo de Love Animals BCN` |
| `ficha` | lista de textos | Viñetas de la tarjeta «El producto» | |
| `certificaciones` | lista de textos | Píldoras verdes | `PETA`, `Fair Wear`, `Oeko-Tex`, `Vegano` |

**Metacampo de colección:** `custom.fina` (texto) = la entradilla en cursiva sobre el título.

Si un producto no tiene `historia_a` ni `historia_b`, la sección de historia no aparece.
Si no tiene `impacto_frase`, la caja granate tampoco.

---

## 2. Colecciones

Son inteligentes: los productos entran solos.

| Handle | Título | Regla |
| --- | --- | --- |
| `tienda-solidaria` | Tienda | proveedor = `Love Animals BCN` |
| `camisetas` | Camisetas | tipo = `Camiseta` |
| `sudaderas` | Sudaderas | tipo = `Sudadera` |
| `tazas` | Tazas | tipo = `Taza` |
| `bolsas` | Bolsas | tipo = `Totebag` **o** `Mochila` |
| `fundas` | Fundas de móvil | tipo = `Funda de móvil` |
| `infantil` | Infantil | etiqueta `infantil` |
| `causa-stop-ley-ppp` | Stop Ley PPP | etiqueta `ppp` |

Las píldoras de la barra superior se configuran en la section «Píldoras de colección»:
un bloque por colección, con texto propio opcional («Todo», «Causa · Stop Ley PPP»).

---

## 3. Piezas nuevas del theme

### Bloques

| Bloque | Para qué | Dónde se puede usar |
| --- | --- | --- |
| `fina` | La línea en cursiva del diseño (entradillas, claim, cierre) | Secciones, grupos, ficha, tarjeta |
| `etiqueta` | Sello en mayúsculas (contorno, sólido o verde) | Ficha y tarjeta |
| `impacto-banda` | Banda «= 1 semana de pienso» | Tarjeta de producto |
| `impacto-caja` | Caja granate del «por qué» | Ficha |
| `garantias` | Líneas con ✓ bajo el botón | Ficha |
| `ahorro` | Sello dorado «Ahorras 4,90 €» | Ficha (junto al precio) |
| `migas` | Migas de pan | Cualquier sección |

### Secciones

| Sección | Para qué |
| --- | --- |
| `barra-cifras` | Franja granate con 3 cifras |
| `chips-colecciones` | Barra de píldoras + contador de artículos |
| `franja-impacto` | «¿A dónde va exactamente tu compra?» |
| `historia-producto` | La historia del diseño (metacampos) |
| `ficha-tecnica` | Tarjetas «El producto» y «Envíos y dudas» |
| `a-quien-ayudas` | Tres peludos con su contador de días |

`a-quien-ayudas` funciona con bloques (eliges tú) o sin bloques (salen los que llevan
más tiempo esperando, saltándose a los adoptados).

### Ediciones al theme original

En Liquid y CSS van entre marcadores `LA START` / `LA END`:

- `snippets/product-card.liquid`: clases de sombra y recorte de la tarjeta.
- `snippets/card-gallery.liquid`: fondo de la foto de la tarjeta.
- `blocks/_product-card-gallery.liquid`: sello de `custom.etiqueta` junto a los del theme.
- `snippets/product-badges-styles.liquid`: estilos de ese sello.
- `snippets/product-media-gallery-content.liquid`: panel de la foto (fondo, borde, sombra) y sello ecológico.
- `snippets/theme-styles-variables.liquid`: paleta `--la-*` en `:root` y trackings anchos.

Dentro de un `{% schema %}` no se pueden poner comentarios, así que **estos añadidos van sin
marcadores** (se reconocen porque las etiquetas están en español):

- `blocks/_product-card.liquid`: acepta los bloques nuevos (`impacto-banda`, `etiqueta`, `fina`, `button`)
  y añade los ajustes «Sombra» y «Alinear el pie de la tarjeta» (precio y botón abajo del todo, para
  que queden a la misma altura en toda la fila).
- `blocks/_product-card-gallery.liquid`: ajustes «Fondo de la foto», «Margen interior de la foto» y
  «Ocultar el sello de rebaja del theme».
- `blocks/_product-media-gallery.liquid`: ajustes «Fondo de las fotos», «Margen interior de las fotos»,
  «Borde en las fotos» y «Sombra de las fotos».
- `sections/main-collection.liquid` + `snippets/product-grid.liquid`: ajuste «Columnas en escritorio»
  (número fijo de columnas, una menos entre 750 y 1000px).
- `assets/tienda.css` (cargado desde `snippets/stylesheets.liquid`): precio comparativo, botón de la
  tarjeta, etiquetas de las opciones de variante y margen interior de la foto de la tarjeta.
- `blocks/text.liquid`: opciones de separación «Ancho (0.1em)» y «Display (0.24em)».
- `config/settings_schema.json`: esas mismas dos opciones en la tipografía global (de la fase anterior).

---

## 4. Datos de la tienda de muestra

**31 productos** (agosto 2026, tras la limpieza):

- **21 de la tienda antigua** (camisetas, sudaderas, infantil y totebags) con sus fotos, textos y
  precios reales de `loveanimalsbcn.com`. Fuera: la campaña del Día de la Madre 2022, las
  «sorpresa» de última talla y los diseños repetidos con otra colocación del estampado.
- **10 del catálogo actual de El Armario de Pris** (6 tazas, 2 mochilas-saco, 2 fundas de móvil),
  con los precios de su Canva y las fotos recortadas de ese mismo catálogo. Cada uno hereda la
  historia del diseño de su prenda hermana.

Todos tienen **una sola variante**: en escaparate no se elige talla en la web (las tallas y colores
reales siguen contados en el metacampo «ficha»).

Los metacampos se rellenaron a partir de esa información:

- el impacto se calcula por tipo y precio (camiseta 15 € = una semana de pienso, sudadera =
  desparasitación, totebag = vacuna, sorpresa 8 € = media semana);
- la ficha técnica se genera con las opciones reales (cortes, tallas, colores);
- la historia sale de la descripción real de cada producto, quitando la parte técnica.

Scripts en el scratchpad de la sesión: `import_products.py`, `import_collections.py`,
`defs_producto.py`, `add_tipo_prenda.py`, `menus_tienda.py` (todos idempotentes por handle).

---

## 5. Modo escaparate (sin compra online)

Desde agosto de 2026 **no se compra por la web**: los pedidos los prepara
[El Armario de Pris](https://www.instagram.com/el_armario_de_pris) y se piden por Instagram.
Su catálogo con precios está en Canva:
<https://www.canva.com/design/DAFpS5kxTqo/O18dCNZNGhcp2cTfY5Ijrw/view>.

Dos interruptores en **Ajustes del tema → Tienda solidaria**:

| Ajuste | Qué hace |
| --- | --- |
| «Modo escaparate (sin compra online)» | Quita el carrito de la cabecera, los botones de compra de la ficha y el añadir rápido de las tarjetas. |
| «Ocultar los precios» | Deja de pintar importes en toda la web (tarjetas, ficha, buscador, carrito). |

La ficha lleva en su lugar el bloque **«Cómo comprarlo»** (`blocks/compra-externa.liquid`):
explicación + botón «Compra aquí» al Instagram de Pris + enlace al catálogo con precios.
En la colección, la franja de arriba cuenta lo mismo.

Con volver a desmarcar los dos ajustes, la tienda vuelve a vender: los bloques de precio y compra
siguen en su sitio en las plantillas (solo hay que añadirlos otra vez a la ficha desde el
personalizador, porque ahí sí se quitaron del `product.json`).

**Catálogo actual de Pris** (sacado de su Canva, agosto 2026): tazas de cerámica 10 € (nº 3 «De la
jaula a la vida», nº 5 «Si tú me dices MIAU», nº 6 «Yo también soy de raza(s)», nº 10 «Stop Ley PPP»),
tazas personalizables con foto 11 € (nº 11 y nº 12), mochila-saco 10 €, funda de móvil 14,95 €,
envío 6 €. El catálogo dice «10% será donado para la asociación».

> ⚠️ **Pendiente de confirmar con Carla:** qué parte de cada pedido vuelve a la protectora.
> De eso dependen las bandas «= 1 semana de pienso» de las tarjetas, la caja de impacto de la ficha
> y las cifras de la cabecera. Mientras tanto la web no afirma ningún porcentaje.

## 6. Diferencias conscientes con el diseño

- **La franja «¿a dónde va tu compra?» va después de la rejilla**, no intercalada tras la primera fila:
  la rejilla de Horizon no admite meter contenido entre tarjetas sin reescribirla.
- **El botón de la tarjeta dice «Lo quiero»** y lleva a la ficha: desde la rejilla no se puede añadir al
  carrito una camiseta de 40 variantes sin elegir talla.
- **El sello «Ahorras …» no se recalcula al cambiar de variante** (solo el precio, que sí lo hace el theme).
  En este catálogo todas las tallas valen lo mismo, así que el importe es correcto; si algún día una
  variante cambia de precio, habría que darle su propio JS.
- **La guía de tallas** del diseño no está: hacen falta las medidas reales de las prendas.
- Los números y destacados sobre granate usan `color8` (#E3C08D, el dorado claro del diseño) en vez del
  dorado normal: el dorado oscuro sobre granate no llega al contraste mínimo.

## 7. Pendiente / a mano

- **Moneda:** la tienda de pruebas está en dólares, así que los precios salen como `$15.00`.
  Es un ajuste del panel (Configuración → Datos de la tienda → Moneda), no del theme;
  en la tienda real de la protectora saldrá en euros.
- Fotos: las de ropa son las reales de su tienda (las 4 primeras de cada producto). Las de tazas,
  mochilas y fundas están recortadas del catálogo en Canva y son pequeñas (393 px de origen):
  en cuanto Pris pase las suyas, se cambian en un minuto.
- Los textos de «Envíos y dudas» están escritos en la propia section: cámbialos ahí, no por producto.
