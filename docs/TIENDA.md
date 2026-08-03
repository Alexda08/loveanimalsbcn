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
| `totebags` | Totebags | tipo = `Totebag` |
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

31 productos reales importados de `loveanimalsbcn.com` (títulos, descripciones, precios,
variantes y fotos reales), con los metacampos rellenados a partir de esa información:

- el impacto se calcula por tipo y precio (camiseta 15 € = una semana de pienso, sudadera =
  desparasitación, totebag = vacuna, sorpresa 8 € = media semana);
- la ficha técnica se genera con las opciones reales (cortes, tallas, colores);
- la historia sale de la descripción real de cada producto, quitando la parte técnica.

Scripts en el scratchpad de la sesión: `import_products.py`, `import_collections.py`,
`defs_producto.py`, `add_tipo_prenda.py`, `menus_tienda.py` (todos idempotentes por handle).

---

## 5. Diferencias conscientes con el diseño

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

## 6. Pendiente / a mano

- **Moneda:** la tienda de pruebas está en dólares, así que los precios salen como `$15.00`.
  Es un ajuste del panel (Configuración → Datos de la tienda → Moneda), no del theme;
  en la tienda real de la protectora saldrá en euros.
- Fotos: son las reales de su tienda, pero solo las 4 primeras de cada producto.
- Los textos de «Envíos y dudas» están escritos en la propia section: cámbialos ahí, no por producto.
