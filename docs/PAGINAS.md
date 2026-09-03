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
5. Añadir «Otros productos» al menú de la tienda, como pidió Carla. **No se puede todavía**:
   las tazas, fundas, llaveros, láminas, mochilas, bodys, bolis y jabones no existen como
   producto en la tienda, solo hay fotos suyas. Hace falta darlos de alta con precio.
6. Decidir si se borran los dos blogs archivados. Es lo único que los saca del sitemap; su
   texto ya está a salvo en [`BLOG-VIEJO.md`](BLOG-VIEJO.md).
7. ~~Montar la franja de fotos de la tienda solidaria~~ — hecha, ver abajo.

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

La **sudadera** «Adoptar es vida 2022 Aniversario» se queda a la venta: Carla solo tachó la
camiseta y Alex prefirió ceñirse a eso. Si resulta que el dibujo va fuera del todo, es un clic.

La colección automática `prendas-misteriosas` se queda casi vacía, pero no está enlazada en
ningún menú.
