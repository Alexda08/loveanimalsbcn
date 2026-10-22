# Piezas del tema

Catálogo de todo lo que **no viene de Horizon**: las sections, bloques, snippets y CSS que son del
proyecto, y los ficheros de Horizon que se han tocado. Para cada pieza: qué hace, dónde se usa, qué
se ajusta desde el editor y qué trampas tiene.

La base es **Horizon v4.1.3** (commit `e038e9b`, el último de Shopify antes del primero del
proyecto, 29-07-2026). Todo lo de aquí sale de comparar el repo con ese commit:

```sh
git diff --name-status e038e9b HEAD -- sections snippets blocks assets templates layout config locales
```

`A` = pieza nuestra, `M` = fichero de Horizon editado. Al actualizar Horizon, **los `M` son los que
hay que revisar a mano**.

Cómo reconocer lo nuestro sin git:

- **Nombres en español** (`barra-cifras`, `ficha-tecnica`, `licencia-ppp`…). Horizon está en inglés.
- **Dentro de un fichero de Horizon**, lo añadido va entre `LA START` / `LA END` (en Liquid,
  `{% comment %} LA START … {% endcomment %}`; en CSS, `/* LA START … */`).
- **Dentro de un `{% schema %}` no se pueden poner comentarios**: ahí los añadidos van sin marcas y
  se reconocen porque la etiqueta está escrita en español y no es una clave `t:`.

El modelo de datos de los animales (metaobjetos `animal` y `album`, sus campos) está en
[`METAOBJETOS.md`](METAOBJETOS.md). La tienda, contada para quien la usa, en [`TIENDA.md`](TIENDA.md).

---

## 1. El sistema de color

### La paleta central

Los colores del diseño viven **en un solo sitio**: el ajuste `color_palette` del tema
(**Personalizar → Ajustes del tema → Colores**). Es un tipo de ajuste de Horizon 4
(`config/settings_schema.json`); nosotros solo le hemos puesto los valores (`config/settings_data.json`):

| Clave | Color | Para qué |
|---|---|---|
| `background` | `#E6DECF` nude claro | Fondo de página |
| `foreground` | `#4A3628` chocolate | Texto; botones oscuros |
| `color1` | `#6E4A44` vino / granate | Franjas granate, acentos |
| `color2` | `#D8CDBB` nude | Fondos de sección alternos |
| `color3` | `#B08D57` dorado | Detalles en dorado sobre claro |
| `color4` | `#F7F2E8` crema | Fondos de foto, cajas |
| `color5` | `#FDFBF6` blanco papel | Tarjetas |
| `color6` | `#5F7A5B` verde | Sellos «eco» |
| `color7` | `#8A625B` vino suave | Textos secundarios |
| `color8` | `#E3C08D` dorado claro | **Texto sobre granate** (el dorado normal no llega al contraste) |

### Cómo se usan

Dos caminos, y los dos leen la misma paleta:

1. **En las plantillas JSON** los ajustes de color no llevan un hex, llevan una referencia:
   `"background_color": "{{ settings.color_palette.color1 }}"`. Es una función de Horizon 4. Hay
   más de 200 referencias así (home, Quiénes somos, tienda, cabecera, pie). **Si se cambia un color
   de la paleta, cambia en toda la web.** Por eso no hay que escribir hex a mano en el editor: se
   rompe el vínculo.
2. **En el CSS de nuestras piezas**, con las variables `--la-*` que escribe
   `snippets/paleta-vars.liquid`:

   | Variable | Sale de |
   |---|---|
   | `--la-wine` | `color1` |
   | `--la-nude` | `color2` |
   | `--la-gold` | `color3` |
   | `--la-cream` | `color4` |
   | `--la-white` | `color5` |
   | `--la-green` | `color6` |
   | `--la-wine-soft` | `color7` (si falta, `color1`) |
   | `--la-gold-soft` | `color8` (si falta, `color3`) |
   | `--la-wine-rgb`, `--la-foreground-rgb` | para `rgb(… / opacidad)` |

   Cada color tiene reserva (`background` o `foreground`) por si un hueco de la paleta se queda vacío.

`paleta-vars` se renderiza **dos veces**: en `:root` desde `snippets/theme-styles-variables.liquid`
(así cualquier bloque las tiene) y otra vez dentro del `<style>` de cada section nuestra,
`#shopify-section-{{ section.id }} { {% render 'paleta-vars' %} }`. La segunda es redundante desde
que existe la primera, pero no estorba.

### El fondo de cada sección: `contrast-override`

Casi todas nuestras sections tienen un ajuste **«Color de fondo»**. Cuando se rellena, llaman a
`snippets/contrast-override.liquid` (**de Horizon, sin tocar**), que:

- escribe una clase `.color-custom-{id}` con ese fondo;
- elige el color del texto: el que se haya puesto a mano; si no, el texto de la página si contrasta
  4,5:1; si no, el color más claro o más oscuro de la paleta, el que contraste más.

Así un fondo granate se lleva el texto claro solo. **Trampa:** solo mira el fondo de la sección; si
dentro hay una tarjeta de otro color, el texto contrastará con la sección, no con la tarjeta. Por eso
`ficha-tecnica` llama a `contrast-override` **dos veces**: una para la sección y otra para el color
de las tarjetas.

---

## 2. Sections

### Tienda solidaria

#### `barra-cifras` — Barra de cifras
Franja granate con 2-3 números grandes y su texto (2019 · 1 · 6 €).
- **Dónde**: `templates/collection.json`.
- **Ajustes**: ancho máximo, separación, esquinas, sombra, fondo, color de los números. Bloques
  **Cifra** (número + texto).
- **Depende de**: `paleta-vars`, `contrast-override`, `color_palette` (reserva del fondo).
- **Ojo**: el comentario de cabecera aún dice «1 chica lo cose todo»; el texto real ya dice «artesana».

#### `chips-colecciones` — Píldoras de colección
Barra de píldoras entre colecciones, con contador de artículos. Se puede fijar al hacer scroll.
- **Dónde**: `templates/collection.json`.
- **Ajustes**: fijar, mostrar contador, palabra del contador, líneas, fondo. Bloques **Píldora**:
  colección **o** enlace suelto + texto.
- **Trampas**: una píldora con una colección que no existe **no pinta nada, sin aviso**.
  `/collections/all` no se puede elegir en el selector: va como enlace suelto, y entonces la píldora
  se marca activa comparando `request.path`.

#### `galeria-tienda` — Galería de la tienda
Cinta de fotos que se desplaza sola en bucle (dos pistas iguales para que no dé tirones). Se para con
el ratón o el foco; con «reducir movimiento», quieta y se arrastra.
- **Dónde**: `templates/collection.json` (28 fotos).
- **Ajustes**: frase fina, título, nota, alto de las fotos, separación, esquinas, segundos por vuelta,
  fondo. Bloques **Foto** (imagen, pie, enlace).
- **Trampa**: Shopify guarda los `.jpeg` como `.jpg`. Una referencia `shopify://shop_images/x.jpeg`
  deja el bloque en blanco sin error.

#### `franja-impacto` — Franja de impacto
Banda con cifra grande a la izquierda (opcional), título y texto en medio y botón a la derecha. Nació
como «¿A dónde va exactamente tu compra?»; hoy es «Los pedidos se hacen por Instagram o WhatsApp».
- **Dónde**: `templates/collection.json`.
- **Ajustes**: cifra, título, texto (rich text), botón (texto, enlace, estilo), ancho, esquinas,
  borde, fondo, color de la cifra.
- **Ojo**: el texto **por defecto** del esquema sigue siendo el de las cuentas de pienso/vacuna.
  Si se añade una franja nueva, cambiarlo.

#### `historia-producto` — Historia del diseño
La historia larga del producto: entradilla, título, párrafos, frase destacada, cierre y firma.
- **Dónde**: `templates/product.json`.
- **Datos**: metacampos `custom.historia_*` del producto. **Sin `historia_a` ni `historia_b`, no
  sale.** Hoy no sale en ninguno (los metacampos están vacíos en la tienda real).
- **Ajustes**: producto (para previsualizar), entradilla/título/firma de reserva, ancho, separación
  del título, fondo, acento.

#### `ficha-tecnica` — Ficha técnica
Tarjetas «El producto» y «Envíos» en dos columnas.
- **Dónde**: `templates/product.json`.
- **Ajustes**: ancho, separación, esquinas, fondo, color de las tarjetas. Bloques **Tarjeta**:
  título, origen de los puntos (*metacampo del producto* / *escritos a mano*), puntos (una línea por
  punto), mostrar certificaciones.
- **Trampa**: con origen «metacampo», los puntos escritos en el bloque son **solo la reserva**. Si
  un producto tiene `custom.ficha`, sus puntos **sustituyen** a los del bloque.

#### `otros-productos` — Otros productos
Lo que no es ropa: rejilla de tarjetas (foto, título, una línea) y recuadro final con texto y botón.
- **Dónde**: `templates/page.otros-productos.json`.
- **Ajustes**: entradilla, título, texto de entrada, «Este título es el titular de la página» (h1),
  texto del recuadro, botón, fondo. Bloques **Producto**.
- **Trampa resuelta (22-10-2026)**: las columnas eran `repeat(2, 1fr)` y «CELEBRACIONES» no cabía en
  media pantalla: `1fr` no baja del ancho de la palabra más larga y la tarjeta empujaba la página.
  Ahora `minmax(0, 1fr)` y el nombre puede cortarse con guion. Ver §6.

#### `a-quien-ayudas` — A quién ayudas
«Ellos»: tres peludos con su contador de días y botón a todos.
- **Dónde**: `templates/product.json`.
- **Ajustes**: entradilla, título, botón, columnas, separación, ancho, fondo. Bloques **Animal**
  (metaobjeto). **Sin bloques** (como está ahora) salen solos los que más días llevan esperando.
- **Depende de**: `animal-card`.
- **Trampa**: el modo automático recorre los álbumes, **no** `shop.metaobjects.animal.values`, que
  solo da 50 animales. Y dentro de cada álbum lee también `animales_mas` (ver §6).

### Animales

#### `peludo-destacado` — Peludo destacado
El «featured» de la home: polaroids que rotan con efecto barajado, pestañas con los nombres, sello
«busco familia desde…», coletilla manuscrita, botón «Conocer a…» y píldora de compartir por WhatsApp.
Pausa con ratón/foco; quieto con «reducir movimiento».
- **Dónde**: `templates/index.json` (con 4 bloques elegidos).
- **Ajustes**: entradilla, textos de botón y enlace, página de animales, coletilla, texto de
  compartir, sello, segundos entre peludos, máximo en automático, fondo. Bloques **Animal**.
- **Depende de**: `peludo-slide`, `dias-esperando`.
- **Posible fallo latente**: el modo automático (sin bloques) **sí** usa
  `shop.metaobjects.animal.values`, que corta en 50. Hoy no se nota porque lleva bloques.

#### `albums-grid` — Grid de álbumes
«Peludos»: rejilla de tarjetas de álbum.
- **Dónde**: `templates/index.json` (11 bloques) y `templates/page.nuestros-animales.json`.
- **Ajustes**: entradilla, título, texto, «Este título es el titular de la página» (solo activado en
  Nuestros animales, para que tenga h1), fondo. Bloques **Álbum**; sin bloques salen todos.
- **Depende de**: `album-card`.

#### `album-destacado` — Álbum destacado
«Así se ve un álbum por dentro»: eliges un álbum y se rellena con sus primeros animales (orden del
admin, sin adoptados).
- **Dónde**: `templates/index.json` (álbum PPP jóvenes, 3 animales).
- **Ajustes**: álbum, número de animales, entradilla, prefijo del título, texto del botón, enlace
  de volver, fondo.
- **Depende de**: `animal-card` (modo botón).

#### `album-main` — Álbum de animales
La página de un álbum: cabecera (y banda de días si es álbum de año), rejilla de fichas sin
adoptados y, al final, el desplegable de cómo se tramita la licencia PPP **en todos los álbumes**.
- **Dónde**: `templates/metaobject/album.json`. Solo se puede usar en plantillas de metaobjeto.
- **Ajustes**: página de animales (volver), texto si está vacío, mostrar licencia, fondo.
- **Depende de**: `animal-card`, `dias-esperando`, `licencia-ppp`.

#### `animal-main` — Ficha de animal
La parte de arriba de la ficha: migas, galería con miniaturas y la caja de adopción (datos, días
esperando, botones, contacto, compartir).
- **Dónde**: `templates/metaobject/animal.json`.
- **Ajustes**: página de animales, frase bajo el contador, textos de los datos fijos (vacunado,
  esterilizado, PPP), enlaces «Quiero adoptar» / «Quiero acoger», **Álbum de acogidas**, texto del
  botón de Instagram, línea de contacto, compartir.
- **Detalles**: «Quiero acogerle» solo sale si el animal está en el álbum elegido en «Álbum de
  acogidas» (lee `animales` y `animales_mas`). El botón «Su post en Insta» sale si el animal tiene
  `posts_instagram`; con más de uno, «Más posts: 2 · 3…».
- **Depende de**: `dias-esperando`.

#### `animal-historia` — Historia y carácter
La banda de abajo de la ficha: historia, carácter y caja de licencia PPP si el animal es PPP.
- **Dónde**: `templates/metaobject/animal.json`.
- **Ajustes**: nota de la valoración («por el equipo del CAACB…»), enlace a la guía PPP, fondo.
- **Depende de**: `licencia-ppp` (modo caja).

#### `animal-relacionados` — Más peludos del álbum
Otros animales del primer álbum que contiene al actual (sin adoptados ni él mismo).
- **Dónde**: `templates/metaobject/animal.json`.
- **Ajustes**: máximo de animales, fondo.
- **Depende de**: `animal-card`.

#### `finales-felices` — Finales felices
El muro de adoptados en polaroid. Con bloques eliges quién sale; sin bloques se rellena solo con los
que están en estado «adoptado». Con pocas tarjetas, usa tantas columnas como haya y se centra.
- **Dónde**: `templates/index.json` (automático, 8) y `templates/page.nuestros-animales.json` (24).
- **Ajustes**: entradilla, título, texto, columnas (escritorio y móvil), separación, giro, sello,
  año en el sello, máximo automático, nota final, ancho, fondo. Bloques **Animal adoptado** (+ frase
  de la familia).
- **Depende de**: `feliz-card`.
- **Trampa**: **un metaobjeto en borrador no lo ve Liquid**. Un adoptado tiene que estar
  **publicado** y con `estado: adoptado` para salir. Sin fecha de adopción, el sello dice «Adoptado»
  a secas.

---

## 3. Bloques

| Bloque | Nombre en el editor | Qué hace | Dónde está puesto |
|---|---|---|---|
| `fina` | Línea fina | La cursiva del diseño (entradillas, claim, cierres). Lo que va en **negrita** sale recto y en color destacado. Acepta Liquid (`{{ closest.product.metafields.custom.claim.value }}`) y tiene **texto de reserva** por si sale vacío | colección, ficha, Quiénes somos; permitido en tarjetas de producto |
| `etiqueta` | Etiqueta | Sello en mayúsculas (borde / sólido / verde). Lee `custom.etiqueta` del producto o un texto fijo | ficha |
| `impacto-banda` | Banda de impacto | Franja crema bajo la foto de la tarjeta con `custom.impacto_corto` | tarjetas de colección y buscador |
| `impacto-caja` | Caja de impacto | Caja granate con `custom.impacto_frase` (lo que va entre `**…**` en dorado) e icono | ficha |
| `garantias` | Garantías | Hasta 4 líneas con ✓ | ficha |
| `compra-externa` | Cómo comprarlo | Título, texto, botón principal, enlace secundario y nota. Sustituye a los botones de compra en modo escaparate | ficha |
| `migas` | Migas de pan | «Raíz › colección › actual». En producto pone sola la colección de llegada (o la primera real) | ficha |
| `ahorro` | Ahorro | Sello «Ahorras 4,90 €» con el precio comparativo | **sin usar** (precios ocultos) |
| `carta` | Carta | «Carta a mi futura familia»: papel con cinta adhesiva e inclinación | home (hero) |
| `pildora` | Píldora (enlace) | Botoncito redondeado con borde fino | home («Comparte en redes») |

Todos los que leen metacampos **no pintan nada si el metacampo está vacío** y no tienen reserva
(en el editor muestran un aviso). Hoy, en la tienda real, `etiqueta`, `impacto-banda` e
`impacto-caja` no pintan nada porque ningún producto tiene esos metacampos.

**Ojo con los valores por defecto**: `garantias` trae por defecto «Algodón ecológico certificado
PETA, Fair Wear y Oeko-Tex», y `compra-externa` un texto que solo habla de Instagram. Un bloque
**nuevo** sale con eso; los puestos ya están corregidos.

---

## 4. Snippets

| Snippet | Qué hace | Lo usan |
|---|---|---|
| `paleta-vars` | Escribe las variables `--la-*` desde `color_palette` (§1) | `theme-styles-variables` (`:root`) y todas nuestras sections y tarjetas |
| `animal-card` | Tarjeta de animal: foto con banda de días, nombre, datos, frase y enlace (o botón «Conocer a…») | `a-quien-ayudas`, `album-destacado`, `album-main`, `animal-relacionados` |
| `album-card` | Tarjeta de álbum: portada (o cubierta con el año), sello Álbum/Urgente, pestaña PPP si el álbum tiene `es_ppp`, banda de días | `albums-grid` |
| `feliz-card` | Polaroid del muro: foto, nombre, sello «Adoptado/a · año», frase | `finales-felices` |
| `peludo-slide` | Una diapositiva del peludo destacado | `peludo-destacado` |
| `licencia-ppp` | La licencia PPP en modo **caja** (ficha) o **desplegable** con la guía paso a paso (álbum). Textos de `CONTENIDO-CARLA.md` §6 | `animal-historia`, `album-main` |
| `dias-esperando` | Días desde una fecha, calculados en el servidor y con punto de miles («1.884»). Sin JS | `animal-main`, `album-main`, `album-card`, `animal-card`, `peludo-slide` |
| `anclas-secciones` | Hace funcionar los enlaces `#shopify-section-section_XXXX` (§6) | `layout/theme.liquid` |

Las tarjetas (`animal-card`, `album-card`, `feliz-card`, `peludo-slide`, `licencia-ppp`) **dan por
hecho que la section ya ha definido `--la-*`**. Hoy siempre lo están (también en `:root`).

## 5. CSS propio

Cargados desde `snippets/stylesheets.liquid`, después de `base.css` y en este orden:

| Fichero | Qué |
|---|---|
| `assets/botones.css` | Peso 500, 0,88 rem y espaciado 0,08 em en todos los botones (lo que los ajustes del tema no cubren) |
| `assets/tienda.css` | Piezas de Horizon de la tienda: precio tachado pequeño, botón de la tarjeta, etiquetas de las opciones de variante, margen interior de la foto de la tarjeta |
| `assets/titulares.css` | **El h1 en el móvil.** Horizon nunca baja el h1 de 48 px y con 0,24 em «PRODUCTOS» no cabía. Hasta 749 px: `clamp(1.625rem, 10vw, 3rem)` y 0,1 em, medido contra el titular más ancho (LEWANDOWSKI) |

El CSS de cada section nuestra va **dentro de la propia section** (`<style>` o `{% stylesheet %}`).

---

## 6. Trampas conocidas

**Scroll en escritorio.** A partir de **990 px** Horizon no hace scroll en la ventana sino dentro de
`.page-wrapper` (`height: 100dvh; overflow-y: auto` en `base.css`). `window.scrollTo` no hace nada.
Cualquier JS que mueva la página tiene que buscar el contenedor que scrollea. Para capturas de página
entera, devolverle el scroll a la ventana (CSS en `PAGINAS.md`, revisión del 19-09-2026).

**Anclas a secciones.** Shopify pinta el div como `shopify-section-template--NNNN__section_XXXX` y
ese número cambia al duplicar el tema, así que en el menú se escribe `#shopify-section-section_XXXX`
y `anclas-secciones` busca la sección **por el final del id**. Además: con el cajón del menú abierto
el scroll está bloqueado (`scroll-lock`), así que primero lo cierra y espera; y `--header-height`
está en el `<body>`, no en `<html>`.

**Grupos que se cortan en el móvil.** En un grupo de tarjetas que va en fila en escritorio y se
apila en el móvil, si las tarjetas tienen la altura en «Rellenar», en el móvil se reparten el alto y
**se cortan** (`overflow: hidden`). Regla: **«Altura en móviles» → «Ajustar al contenido»**
(`height_mobile: fit`). Pasó en la home («iii. Nuestros animales», 73 px de 173) y en Quiénes somos
(la tarjeta del IBAN).

**Columnas de rejilla.** `repeat(N, 1fr)` no deja que una columna sea más estrecha que la palabra
más larga que contiene: una palabra larga **ensancha su columna y desborda la página**. Se escribe
`repeat(N, minmax(0, 1fr))`. Ya está así en `otros-productos`; **el resto de nuestras sections siguen
con `1fr`** (`albums-grid`, `album-main`, `album-destacado`, `animal-relacionados`, `a-quien-ayudas`,
`barra-cifras`, `ficha-tecnica`, `finales-felices`). La revisión del 19-09 no encontró desbordes, pero
un nombre o un título largo nuevo podría provocarlo.

**50 referencias por lista.** Liquid solo lee las **50 primeras** de una lista de referencias y de
`shop.metaobjects.X.values`. Por eso los álbumes guardan la cola en un segundo campo,
`animales_mas`, y todas las sections que recorren un álbum leen los dos. Lo que se recorre «todos los
animales» se hace pasando por los álbumes. Detalle en `METAOBJETOS.md`.

**Borradores invisibles.** Un metaobjeto en borrador no existe para Liquid: no entra en ninguna
lista ni en ningún muro, aunque esté enganchado a un álbum.

**`.jpeg` → `.jpg`.** Shopify renombra al subir. Las referencias `shopify://shop_images/…` tienen que
llevar el nombre que da la tienda.

**Herencia de variables CSS.** Un grupo dentro de otro hereda `--size-style-width-mobile` del padre.
Por eso `blocks/group.liquid` reescribe la variable cuando el ajuste está vacío (ver §7).

**El tema publicado está conectado a GitHub**: cada push a `main` va directo a la web en vivo.

---

## 7. Ficheros de Horizon editados

Lo que hay que revisar al actualizar Horizon. Fecha y motivo sacados de los commits.

### Escaparate (03-08-2026, «Tienda en modo escaparate»)

| Fichero | Qué se cambió |
|---|---|
| `blocks/buy-buttons.liquid` | Todo envuelto en `unless settings.escaparate`: en escaparate no pinta botones de compra |
| `snippets/header-actions.liquid` | Sin icono de carrito en escaparate |
| `snippets/quick-add.liquid` | Sin añadir rápido en las tarjetas en escaparate |
| `snippets/price.liquid` | Todo envuelto en `unless settings.ocultar_precios` |
| `config/settings_schema.json` | Grupo nuevo **«Tienda solidaria»** con `escaparate` y `ocultar_precios` |

### Tarjeta y ficha de producto (03-08-2026)

| Fichero | Qué se cambió |
|---|---|
| `blocks/_product-card.liquid` | Acepta `impacto-banda`, `etiqueta`, `fina`, `button`; ajustes **«Sombra»** y **«Alinear el pie de la tarjeta»** (precio y botón a la misma altura en toda la fila) |
| `blocks/_product-card-group.liquid` | Acepta `button`, `impacto-banda`, `etiqueta`, `fina` |
| `blocks/_product-card-gallery.liquid` | Ajustes «Fondo de la foto», «Margen interior de la foto», «Ocultar el sello de rebaja del theme»; sello de `custom.etiqueta` junto a los del tema |
| `snippets/card-gallery.liquid` | Pinta ese fondo y margen |
| `snippets/product-card.liquid` | Clases de sombra y recorte de la tarjeta |
| `snippets/product-badges-styles.liquid` | Estilos del sello de `custom.etiqueta` |
| `blocks/_product-media-gallery.liquid` | Ajustes «Fondo de las fotos», «Margen interior», «Borde», «Sombra» |
| `snippets/product-media-gallery-content.liquid` | Panel de la foto (fondo, borde, sombra) y sello verde de `custom.eco_badge` |
| `sections/main-collection.liquid` + `snippets/product-grid.liquid` | Ajuste **«Columnas en escritorio»**: número fijo de columnas (una menos entre 750 y 1000 px). Ojo: escribe `repeat(N, 1fr)` |
| `templates/search.json` | Tarjetas del buscador iguales que las de la colección |

### Tipografía (30-07-2026 y 03-08-2026)

| Fichero | Qué se cambió |
|---|---|
| `config/settings_schema.json` | Opciones de espaciado **«Ancho (0.1em)»** y **«Display (0.24em)»** en los seis niveles de titular |
| `blocks/text.liquid`, `blocks/jumbo-text.liquid` | Las mismas dos opciones |
| `snippets/theme-styles-variables.liquid` | Las variables de esos espaciados y `render 'paleta-vars'` en `:root` |
| `snippets/stylesheets.liquid` | Carga `botones.css`, `tienda.css` y `titulares.css` |

### Grupos (30-07 y 06-08-2026)

| Fichero | Qué se cambió |
|---|---|
| `blocks/group.liquid` | Ajustes **«Sombra»**, **«Dónde se ve → Pantallas»** (móvil y escritorio / solo móvil / solo escritorio, corte en 750 px) y **«Altura en móviles»** (`height_mobile`: igual que en escritorio · ajustar · rellenar · personalizado). Los dos anchos llevan apellido (escritorio / móvil) y suman «igual que en escritorio». Si el ajuste de móvil está vacío, reescribe la variable apuntando al valor de escritorio del propio bloque para **cortar la herencia** del grupo padre |
| `snippets/group.liquid` | Sombras, la clase de «Dónde se ve» (reutiliza `hidden--mobile` / `hidden--desktop` de `base.css`) y la regla que deja mandar a la altura de móvil. Arreglo: con «Apilar en el móvil» el grupo conserva `layout-panel-flex--row` y seguían aplicando las reglas de **ancho** de `base.css`, que en vertical se convierten en **altura**; en móvil y solo si apila, vuelve a `flex: 0 1 auto` |
| `snippets/size-style.liquid` | Escribe `--size-style-height-mobile`. `base.css` ya la leía, pero nadie la escribía |

### Resto

| Fichero | Fecha | Qué se cambió y por qué |
|---|---|---|
| `layout/theme.liquid` | 03-09-2026 | `render 'anclas-secciones'` al final del `<body>`: los enlaces del menú a secciones de la home no llevaban a ninguna parte |
| `snippets/meta-tags.liquid` | 12-09, 19-09 y 04-10-2026 | `og:image` / `twitter:image` con la foto del propio metaobjeto en fichas y álbumes (al compartir no salía foto); imagen de reserva `imagen_social`; en la home, título y descripción de los ajustes `titulo_home` / `descripcion_home`, porque los de Preferencias eran de la tienda vieja y la API no deja cambiarlos |
| `config/settings_schema.json` | 19-09 y 04-10-2026 | Ajustes `imagen_social`, `titulo_home`, `descripcion_home` en «Logo y favicon» |
| `locales/es.json` | 06-09-2026 | «Tu carrito esta vacío» → «está» |
| `templates/404.json`, `cart.json`, `list-collections.json`, `page.contact.json`, `password.json` | 05-08-2026 | Textos que quedaban en inglés, traducidos |
| `templates/index.json`, `collection.json`, `product.json` | varias | Las plantillas, montadas al diseño (son contenido, no código) |
| `sections/header-group.json`, `footer-group.json` | 29-07 a 05-08-2026 | Cabecera y pie al diseño, con referencias a la paleta en vez de hex |
| `config/settings_data.json` | varias | Los valores: paleta, tipografías, botones, favicon, escaparate y precios ocultos |

Plantillas **nuevas**: `templates/metaobject/album.json`, `templates/metaobject/animal.json`,
`page.nuestros-animales.json`, `page.otros-productos.json`, `page.sobre-nosotras.json` (esta última
sin ninguna section propia: todo son grupos, textos, botones y `fina`).
