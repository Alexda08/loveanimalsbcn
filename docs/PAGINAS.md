# Páginas y menús

Los menús y las páginas **no son theme**: viven en el admin de Shopify (Contenido → Páginas y
Navegación → Menús). El theme solo pone la plantilla con la que se pintan.

## Estado de la tienda real (05-08-2026, menús y blog al 02-09-2026)

El theme publicado en `loveanimalsbcn.myshopify.com` es **Horizon de serie**, no el nuestro:
`loveanimalsbcn/main` está subido pero sin publicar. Todo lo de este repo entra en la web el día que
se publique.

**Las 7 páginas estaban sin publicar**, así que los 7 enlaces del menú que apuntaban a ellas daban
404 en la web en vivo (incluidos «Legal» y «Cookies»). Se publicaron seis:

| Página | Estado |
|---|---|
| `/pages/legal` | publicada |
| `/pages/cookies` | publicada |
| `/pages/envios` | publicada |
| `/pages/cambios-y-devoluciones` | publicada |
| `/pages/formulario-de-contacto` | publicada |
| `/pages/sobre-nosotras` | publicada |
| `/pages/guia-de-tallas` | **sin publicar y fuera del menú** — Alex no la quiere |

El cuerpo de las siete está copiado en el scratchpad de la sesión (`copias_paginas/*.html`) por si
hiciera falta recuperar alguna.

> ⚠️ «Envíos» y «Cambios y devoluciones» describen la operativa antigua (fabricación de **Role
> Clothing**, envío por Correos en 7-15 días laborables) y «Cambios y devoluciones» remite a la guía
> de tallas que ya no está enlazada. Con la tienda en modo escaparate habría que reescribirlas.

## La plantilla «Quiénes somos»

`templates/page.sobre-nosotras.json` — implementa `design/loveanimalsbcn-about-us.html` **sin crear
ninguna section ni bloque nuevo**: todo son `section`, `group`, `text`, `button` y el bloque `fina`
del proyecto, con los mismos moldes que la home (tarjeta blanca de «Colabora», caja de la cuenta,
franja de color a sangre).

Orden: hero · el puente · qué hacemos · no estás solo/a · colaborar · cierre.

| Sección | Qué es | Fondo |
|---|---|---|
| `hero` | entradilla, titular a dos voces y la intro del docx | el de la página |
| `puente` | la frase del PUENTE y el DESTINO | granate (`color1`) |
| `hacemos` | 4 tarjetas 2×2 + la caja «no te soltamos la mano» | el de la página |
| `solo` | «adoptar impone, pero no estás solo/a» + 3 tarjetas de contacto | crema (`color4`) |
| `colabora` | las 4 formas de ayudar, con la cuenta bancaria | el de la página |
| `cierre` | «de la jaula a la vida» + tres botones a la home | nude (`color2`) |

Detalles del montaje que no son evidentes:

- **Las filas de 2 tarjetas** son dos grupos en fila dentro de un grupo en columna: una sección en
  fila no hace salto de línea (`--flex-wrap: nowrap`), así que 2×2 solo sale anidando.
- **Los titulares a dos voces** (una línea chocolate y otra granate en cursiva) son dos bloques de
  texto con el mismo tamaño dentro de un grupo con separación 0. No se puede colorear media frase
  dentro de un solo bloque.
- **Las anchuras** salen de la proporción del diseño sobre su lienzo (`.hace-grid` 920 px de 1036 →
  88 %; `.solo-in` 760 px → 73 %), no de píxeles fijos.
- **Los teléfonos y correos son enlaces** (WhatsApp y mailto); en el diseño eran texto plano.
- Diferencias conscientes: la caja «no te soltamos la mano» lleva borde granate por los cuatro lados
  en vez de solo a la izquierda, y la cuenta bancaria sale en caja crema en vez de con borde dorado
  discontinuo (el bloque de texto no tiene borde).

> ⚠️ **El texto que escribieron Amanda, Carla y Lara ya no se pinta aquí.** La versión anterior de
> esta plantilla (commit `a354060`) contaba el origen de la cuenta, el equipo, la ley de sacrificio
> cero, la lista de protectoras ayudadas y la historia de Javi el Rey Chatarrero. El diseño nuevo no
> los incluye. El texto sigue estando en el cuerpo de `/pages/sobre-nosotras` de la tienda real y en
> el historial de git; si se quiere recuperar, lo suyo sería una página aparte («Nuestra historia»).

Para verla hay que tener una página con handle `sobre-nosotras` y plantilla `sobre-nosotras`.
Las dos tiendas la tienen ya: en la real se le asignó la plantilla el 02-09-2026, junto con la
página nueva `/pages/nuestros-animales` (publicada, plantilla «nuestros-animales»).

Como la plantilla no lleva la sección `main-page`, **el cuerpo que haya en el admin no se pinta**:
para cambiar el texto se toca la plantilla, igual que en la home.

## Menús de la tienda real

Reescritos el 02-09-2026 con la estructura del diseño nuevo. Los anclajes `#shopify-section-…`
apuntan a secciones de `templates/index.json`.

> ⚠️ **Esos anclajes no funcionan solos.** Shopify no pinta el div con el nombre que la sección
> tiene en la plantilla (`section_mG9zrt`), sino con `template--31409172316491__section_mG9zrt`:
> el prefijo lo pone él y ese número cambia si se duplica el tema, así que no hay forma de
> escribirlo a mano en un menú. Sin ayuda, el navegador no encuentra el destino y se queda
> arriba del todo — que es lo que le pasaba a «Colabora» y al enlace de la licencia PPP de las
> fichas. Lo resuelve `snippets/anclas-secciones.liquid`, que busca la sección por el final de
> su id. Si algún día se dejan de usar anclas, ese snippet sobra.

- `main-menu`: Quiero adoptar · Quiero acoger · Nuestros animales · **Tienda solidaria**
  (con Novedades, Camisetas, Sudaderas, Totebags y Niños colgando) · Colabora
- `footer-adopcion` «Adopción y acogida»: Quiero adoptar · Quiero acoger · Nuestros animales ·
  Licencia PPP · Quiénes somos
- `footer-colabora` «Colabora»: Tienda solidaria · Teaming (al grupo de teaming.net, desde el
  03-09-2026) · Donación puntual · Redes sociales
- `footer-legal` «Legal»: privacidad · envío · términos · aviso legal · Cookies · Contacto

«Quiénes somos» y «Contacto» están en el pie porque el menú de arriba son cinco entradas y no
caben; si no fuera por eso se quedarían sin ningún enlace en toda la web.

Los menús `footer` y `footer-1` son del tema viejo y ya no los usa nadie. No se han borrado, pero
tampoco se pintan. Con ellos dejan de estar enlazadas `/pages/envios`, `/pages/cambios-y-devoluciones`
y `/pages/legal` — las dos primeras describen la operativa antigua de Role Clothing, así que
tampoco convenía enlazarlas tal como están.

## El blog viejo

Los álbumes vivían como 11 artículos en `/blogs/animales-en-adopcion`, escritos a mano. Ahora
son metaobjetos, así que el blog se ha **ocultado**: los 8 artículos publicados pasaron a
borrador (no se han borrado) y hay **12 redirecciones 301** de cada URL vieja a su álbum nuevo.

| Artículo viejo | Va a |
|---|---|
| `/blogs/animales-en-adopcion` | `/pages/nuestros-animales` |
| `…/necesitamos-casas-de-acogida` | `/pages/album/necesitamos-casa-de-acogida` |
| `…/abuelos`, `…/abuelitos` | `/pages/album/abuelos` |
| `…/los-mas-veteranos` | `/pages/album/los-mas-veteranos` |
| `…/veteranos` | `/pages/album/desde-2021-esperando-familia` |
| `…/ppp-jovenes-1-a-4-anos` | `/pages/album/ppp-jovenes` |
| `…/ppp-adultos-5-a-9-anos`, `…/ppps-en-adopcion` | `/pages/album/ppp-adultos` |
| `…/no-ppps` | `/pages/album/mestizos` |
| `…/gatos`, `…/gatos-en-adopcion` | `/pages/album/gatos` |

> ⚠️ **Ojo con el destino: es `/pages/album/…`, no `/album/…`.** La página de un metaobjeto
> cuelga de `/pages/`, y la primera tanda de 301 apuntaba a la raíz: llevaban a un 404 que no se
> iba a arreglar ni publicando el tema. Corregidas el 03-09-2026 y comprobadas una a una.
>
> ⚠️ **Aun así siguen en 404 para el público hasta que se publique el TEMA**, porque la ruta la
> decide el tema publicado. En vista previa funcionan. Esas 8 URLs son lo que Carla reparte por
> Instagram; si el lanzamiento se retrasa, lo suyo es volver a publicar los artículos: las 301
> se quedan puestas y entran solas en cuanto se oculten otra vez.
>
> **Los blogs están fuera de circulación desde el 03-09-2026.** No los van a usar, y sus dos
> portadas seguían vivas y vacías: `/blogs/news`, que Shopify crea de serie, y
> `/blogs/animales-en-adopcion`, que es la que Carla reparte. Una 301 no las arreglaba, porque
> solo salta en un 404 y esas páginas existían. Se les ha cambiado el handle a
> `archivo-animales-en-adopcion` y `archivo-news` (`archiva_blogs.py`): ahora las URLs viejas
> son 404 y entran las redirecciones. Los 11 artículos siguen ahí, en borrador, y su texto está
> copiado en [`BLOG-VIEJO.md`](BLOG-VIEJO.md) por si algún día se borra el blog entero.
>
> Ningún menú ni plantilla del theme enlaza a un blog. Lo único que queda: los dos blogs
> archivados **siguen apareciendo en `sitemap_blogs_1.xml`**, y de ahí solo salen borrándolos.

## Qué queda para publicar

1. **Publicar el tema `loveanimalsbcn/main`.** Es lo único que falta. Ahora manda Horizon de
   serie, sin configurar: ni siquiera pinta `main-menu`, y como no tiene las plantillas de
   metaobjeto, `/pages/album/…` y `/pages/animal/…` dan 404 aunque las entradas estén
   publicadas. En vista previa sí se ven.
   Comprobado el 02-09-2026 que lo subido coincide con el repo (solo cambian los saltos de línea).
2. ~~Pasar las entradas a publicadas~~ — hecho: las 211 están en ACTIVE.
3. Repasar los *fallbacks* que miran `shop.metaobjects.animal.values`, que solo ven 50 de 200.
4. Decidir qué se hace con `/pages/envios` y `/pages/cambios-y-devoluciones`, que se quedan sin
   enlace y siguen contando la operativa antigua de Role Clothing.
5. Añadir «Otros productos» a la tienda, como pidió Carla (lo repitió el 06-09). **Sigue sin
   poderse**: las tazas, fundas, llaveros, láminas, mochilas, bodys, bolis y jabones no existen
   como producto, solo hay fotos suyas, y las del «último enlace de Smash» que menciona no han
   llegado al repo. La barra de píldoras ya acepta un enlace suelto, así que en cuanto haya
   dónde apuntar es un bloque más.
6. Decidir si se borran los dos blogs archivados. Es lo único que los saca del sitemap; su
   texto ya está a salvo en [`BLOG-VIEJO.md`](BLOG-VIEJO.md).
7. ~~Montar la franja de fotos de la tienda solidaria~~ — hecha, ver abajo.
8. ~~La ronda de revisión de Carla del 06-09-2026~~ — hecha, ver abajo.
9. ~~La segunda ronda del 06-09-2026~~ — hecha salvo «Otros productos» (punto 5), ver abajo.

## La franja de la tienda solidaria

La pidió Carla: «fotos chulas de gente con la ropa o productos, que vayan cambiando». Es
`sections/galeria-tienda.liquid`, y va en la página de colección entre los chips y la franja de
«los pedidos se hacen por Instagram». **28 fotos** subidas como `tienda-01`…`tienda-28`,
alternando el catálogo cuidado (`PRODUCTOS LAB CATÁLOGO BONITO.zip`) con la gente real que ha
comprado (venía mezclada en `FOTOS WEB QUE FALTAN.zip`), y con texto alternativo escrito a mano
una por una, que salen personas y animales.

Es una cinta que se desplaza sola en bucle, con dos pistas iguales para que no dé tirones. Se
para al pasar el ratón por encima o al llegar con el teclado, y con «reducir movimiento»
activado no se mueve: se arrastra a mano. Las fotos son bloques, así que Carla puede quitar,
añadir y reordenar desde el editor sin tocar nada más; cada una admite pie y enlace.

> ⚠️ **Shopify renombra los `.jpeg` a `.jpg`** al guardar el fichero. Si en la plantilla se
> escribe `shopify://shop_images/tienda-02.jpeg`, el bloque se queda en blanco y la foto no sale
> — sin ningún error, ni en el log ni en la página. La mitad de la cinta estuvo así hasta que se
> miró el HTML. Las referencias hay que sacarlas de los nombres que devuelve la tienda.

Quedan sin usar 35 fotos más en `_sin_dueno/2-para-la-tienda/`, por si se quiere ampliar.

Para revisar antes de publicar, sin tocar la web: *Temas → `loveanimalsbcn/main` → Personalizar*,
y en el desplegable de plantillas elegir **Álbum** o **Animal**.

## Prendas retiradas (03-09-2026)

Carla marcó siete que ya no se venden. Están **en borrador**, no borradas: conservan fotos,
precios y variantes, y se reactivan con un clic.

| Producto | Por qué |
|---|---|
| Camiseta Sorpresa · Camiseta Sorpresa Día de la madre 2022 | solo para campañas de stock |
| Sudadera Sorpresa · Sudadera Sorpresa Día de la madre 2022 | solo para campañas de stock |
| De la jaula a la vida \| Diseño delantero y trasero (camiseta y sudadera) | diseño retirado |
| Camiseta \| Adoptar es vida 2022 Aniversario | dibujo retirado |

La **sudadera** «Adoptar es vida 2022 Aniversario» se quedó a la venta en aquella ronda porque
Carla solo había tachado la camiseta. En la segunda ronda la tachó también, así que ya está en
borrador y el par vuelve a ir junto: el dibujo de 2022 (frase **y silueta**, `SILUETAADOPTAR` en
los SKU) sale entero del catálogo.

La colección automática `prendas-misteriosas` se queda casi vacía, pero no está enlazada en
ningún menú.

## La ronda de revisión de Carla (06-09-2026)

Repasó la web entera y pasó cinco cosas. Están las cinco hechas.

### El «Colabora» del menú llevaba al principio de la página

Ya se había arreglado una vez, con `snippets/anclas-secciones.liquid`, y **seguía sin
funcionar**: el snippet resolvía bien el id de la sección pero luego no conseguía mover la
página. Tenía tres fallos, uno por cada trampa de Horizon:

1. **A partir de 990 px el que hace scroll no es la ventana, es `.page-wrapper`**, que lleva
   `height:100dvh; overflow-y:auto` (`base.css`). En escritorio `window.scrollTo` no hace
   absolutamente nada. Ahora el snippet mira quién es el contenedor con scroll y le habla a él.
2. **Con el menú de las rayitas abierto, el scroll está bloqueado**: el `<details>` del cajón
   lleva el atributo `scroll-lock`, que pone `scroll-lock` en el `<html>` y de ahí sale un
   `overflow:hidden`. Como el snippet hacía `preventDefault()`, el menú ni se cerraba: se
   quedaba abierto y el scroll bloqueado. Justo lo que veía Carla. Ahora cierra el cajón,
   **espera a que suelte el bloqueo** y entonces salta.
3. **`--header-height` la escribe `header.js` en el `<body>`**, no en el `<html>`, así que el
   hueco para la cabecera pegajosa salía siempre 0.

Los enlaces del menú (`/#shopify-section-section_mG9zrt` y compañía) no hay que tocarlos: el
prefijo real del id (`template--32056139120971__`) cambia cada vez que se duplica el tema, y por
eso el snippet busca por el final del id y no por el id entero.

### «PRODUCTOS» salía partido en el móvil

`assets/titulares.css`, cargado el último desde `snippets/stylesheets.liquid`. El h1 del tema
nunca baja de 48 px por estrecha que sea la pantalla — Horizon calcula el suelo del tamaño
fluido a partir del siguiente tamaño de los ajustes, y aquí h1 vale 56 y h2 vale 48 — y con el
espaciado de 0,24 em la palabra no cabía en los 358 px de un móvil. Como `base.css` pone
`overflow-wrap: break-word` en los h1, se partía por la mitad.

Los números están medidos con la propia Cormorant (`fontTools`), no a ojo, y contra el titular
más ancho que existe en la web, que no es «PRODUCTOS» sino **LEWANDOWSKI**: 7,31 em de letras.
Con `clamp(1.625rem, 10vw, 3rem)` y `0.1em` cabe en cualquier pantalla desde 320 px con un 7-10 %
de hueco de sobra, y de 480 px en adelante vuelve a sus 48 px de siempre.

### La portada de acogidas (Trans)

Carla apuntó `85F21429-41F2-4D26-AA52-49015579EC84`, **y ese fichero no venía en el zip**. Lo que
sí venía era `E1BCDC46-CDF2-49E2-8356-84032FB5B552`, que no reclamaba ningún álbum. Es Trans: el
mismo perro atigrado, la misma oreja doblada, el mismo arnés lila y los ojos color miel de su
propia frase («Ojitos color miel para endulzarte»). Comparado con las fotos de su ficha antes de
ponerla. Los siete álbumes tienen ya su portada.

### Ortografía

**73 correcciones en 48 fichas** y 7 en el texto del tema. Solo ortografía: no se ha cambiado
ni una palabra de sitio ni la manera de contar las cosas.

Salieron sin diccionario — los de español que hay a mano marcan «fue» y «tiene» —, comparando
cada palabra rara con el resto del corpus: si aparece una o dos veces y está a un carácter de
otra que aparece muchas, casi siempre es errata. Los scripts quedan en el scratchpad
(`corrector.py`, `arregla_erratas.py`), con la lista entera.

Lo gordo, por si Carla quiere revisarlo: `rión`→`riñón` (Trans), `ship`→`chip` (Lewandowski),
`sociavle`→`sociable` (Tristán), `deshaucio`→`desahucio` (Reina y Kintsugi), `familis`→`familia`
(Reina), `hogara`→`hogar` (Guiness), `odas`→`Todas` (Betty, se comió la T inicial),
`llegón`→`llegó` (Fígaro), `Charli`→`Charlie` (en su propia ficha), `mayoria`→`mayoría` (15
fichas de gatos, venía de un párrafo copiado), `otroa`→`otros` (8 fichas, del mismo párrafo),
y `porqué`→`por qué` donde tocaba — en Tuca se queda `el porqué`, que ahí sí lleva artículo.

En el tema: «Tu carrito **esta** vacío» → «está» (`locales/es.json`), «siguen habiendo problemas»
→ «sigue habiendo» (dos veces, *haber* impersonal siempre en singular), «pre-adopción» →
«preadopción», «tote-bags» → «totebags» (el menú ya decía Totebags), y los `...` sueltos pasados
a `…` para que no bailen con los del resto.

Y una de concordancia: la entradilla de **todas** las páginas de colección decía «mientras
esperan, puedes ayudarles con la…» y debajo el título de la colección, así que se leía «con
la… PRODUCTOS», «con la… CAMISETAS», «con la… SUDADERAS». Ninguna colección tiene el metafield
`custom.fina`, así que ese texto de reserva sale en todas. Ahora dice «puedes ayudarles con…».

### Pendiente de Carla

- **Las 31 fotos sin dueño** de `_sin_dueno/1-de-quien-es/`, agrupadas por animal en
  `_todas-juntas.jpg`. Solo hace falta que diga qué grupo es Andrés, Chiquitita, Kaur y Katsuki.
- El producto **«Mestizos - Diseño trasero.»** tiene un guion y un punto final que sus hermanos
  no tienen («Logo | Diseño trasero»). Es el título del producto, no del tema: se cambia desde
  el admin y cambia también su URL, por eso no se ha tocado.

## La segunda ronda de Carla (06-09-2026, por la mañana)

Llegó con cuatro capturas y un resumen. Lo que se ha hecho:

### Dos cosas que ya estaban arregladas cuando escribió

- **«Falta foto álbum acogidas».** La portada de Trans se subió a las **14:22**, y su captura es
  de las **11:04**. Comprobado que el fichero responde 200 y que la tarjeta la pinta.
- **«Palabras que se cortan en móvil: productos, novedades, camisetas, sudaderas».** Es lo mismo
  que ya se arregló en la ronda anterior con `assets/titulares.css`; el CSS estaba servido en el
  tema antes de su mensaje. Medidas las cuatro contra la propia Cormorant: la más apretada,
  PRODUCTOS, cabe con un **31 %** de hueco de sobra a 320 px, y las otras con 34-44 %. La única
  que no entra en una línea es «TIENDA SOLIDARIA», pero son dos palabras y parte por el espacio,
  que es lo que tiene que hacer.

Las dos son cuestión de que recargue del todo (Ctrl+F5, o cerrar y abrir la pestaña).

### La barra de píldoras de la tienda

Era peor de lo que ella vio. De las ocho píldoras **solo salían dos**: las otras seis apuntaban
a colecciones que no existen en la tienda (`tienda-solidaria`, `tazas`, `bolsas`, `fundas`,
`infantil`, `causa-stop-ley-ppp`). Una píldora sin colección detrás no pinta nada, sin aviso.

Ahora son seis y son las mismas que el submenú de «Tienda solidaria»: **Todo · Novedades ·
Camisetas · Sudaderas · Totebags · Niños**.

El «Todo» no se podía hacer con el selector de colecciones, porque `/collections/all` no es una
colección elegible. Por eso `sections/chips-colecciones.liquid` acepta ahora un **enlace suelto**
en la píldora: si no hay colección, usa el enlace y se marca activa comparando `request.path`.
Es también el hueco por donde entrará «Otros productos» cuando exista.

### Textos

| Dónde | Qué |
|---|---|
| Álbum PPP adultos | «caballeros con corazón grande» → **«caballeros de gran corazón»** |
| Pie de la cinta de fotos | → **«Fotos de quienes ya visten SOLIDARIDAD. Tú también puedes formar parte de este museo. ¡Haz tu pedido!»** |
| Franja «Los pedidos se hacen por Instagram» | segundo párrafo nuevo, el de **personalizar** color, diseño y fotos |
| Texto del PPP en la home | «el trámite, y aunque parezca pesado» → **«el trámite y, aunque parezca pesado»** |

Lo de personalizar va en esa franja y no en otro sitio porque es la que explica **cómo se pide**
y está justo encima de la parrilla de productos, que es donde se lee «solo hay blanco y negro».
El texto va tal cual lo escribió ella, mayúsculas incluidas.

### Fichas

- **«Reservados» se leía como «ya tiene familia».** Carla lo vio en Logan & Trunks, pero la
  palabra estaba en tres fichas. Cambiadas las tres: Logan & Trunks (`reservados`→`tímidos`),
  y **Blue** y **Nito** (`reservado`→`tímido`), que tenían el mismo malentendido y ella no llegó
  a ver.
- **Guiness** pasa de PPP adultos a **PPP jóvenes** (tiene 2 años). Era error suyo al montarlo.
- **Gnar** se marca `estado: adoptado` con fecha 05-09-2026. Con eso desaparece del álbum de
  gatos y entra en el grupo del que se nutre el muro de finales felices.

### Los adoptados: cuidado con dos maneras distintas

Gnar se ha marcado **adoptado y publicado**. Los diez de la semana pasada (Behia, Rusty, Kenia,
Simba, Fabrizzio, Saitama, Dustin, Bony, Xulo, Thorin) están **en borrador**, que es otra cosa:
un metaobjeto en borrador **no lo ve Liquid**, así que no puede salir en el rincón feliz aunque
se quiera. Para que salgan hay que publicarlos y ponerles `estado: adoptado` y su fecha.

No se ha hecho porque **no se sabe la fecha de adopción de ninguno** y `feliz-card` la usa para
pintar el año. Es lo que Carla ofrece justo en este mensaje («¿organizo unos cuantos adoptados
para empezar? No sé, 10-20?»): con nombre, foto y mes ya se montan.

### Prendas

La **«Sudadera | Adoptar es vida 2022 Aniversario»**, la que tachó en rojo, pasa a borrador.

Y se dan de alta los dos **diseños nuevos** que mandó, a la venta y **sólo en blanco**, que es lo
único que enseñan sus mockups:

| | Precio | Opciones | SKU |
|---|---|---|---|
| Camiseta \| Adoptar es vida | 15 € | Unisex/Mujer · S-2XL · Blanco | `…ADOPTARESVIDA_LIGHT-US002-WH-…` / `-WS002-` |
| Sudadera \| Adoptar es vida | 25 € | Unisex · XS-2XL · Blanco | `…ADOPTARESVIDA_LIGHT-SWH02-WH-…` |

El diseño ya existía en el catálogo de Pris — es **`ADOPTARESVIDA`** en los SKU, la frase sola, y
no hay que confundirlo con **`SILUETAADOPTAR`**, que es el de 2022 (frase *y* silueta) y el que
acaba de salir. Se crearon primero en borrador para revisarlos y se publicaron después.

Las colecciones de esta tienda son **todas automáticas por etiqueta**: con `camiseta`/`sudadera`
y `novedades` entran solas donde tienen que entrar, no hay que añadirlas a mano. Y hay que
publicarlos en los canales aparte del estado: Online Store, Buy Button y Shop, que es donde
están sus hermanos.

### Pendiente

- **Las fotos del «último enlace de Smash»** (tazas, fundas de móvil, boli, punto de libro,
  bodys de bebé). Sin ellas no hay «Otros productos» que montar.
- **Confirmar con Pris los dos diseños nuevos**: si los hace en más colores que el blanco, hay
  que añadir el valor a la opción *Color* y su foto. La camiseta negra de ese mismo diseño ya
  existe como foto en la tienda (`loveanimalsbcn-adoptaresvida_dark-us002-bk…`), de las prendas
  del Giving Tuesday.
- Sigue en pie lo de la ronda anterior: las 31 fotos sin dueño y el título de «Mestizos -
  Diseño trasero.».
