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
apuntan a secciones de `templates/index.json`; están verificados uno a uno.

- `main-menu`: Quiero adoptar · Quiero acoger · Nuestros animales · **Tienda solidaria**
  (con Novedades, Camisetas, Sudaderas, Totebags y Niños colgando) · Colabora
- `footer-adopcion` «Adopción y acogida»: Quiero adoptar · Quiero acoger · Nuestros animales ·
  Licencia PPP · Quiénes somos
- `footer-colabora` «Colabora»: Tienda solidaria · Teaming · Donación puntual · Redes sociales
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
| `…/necesitamos-casas-de-acogida` | `/album/necesitamos-casa-de-acogida` |
| `…/abuelos`, `…/abuelitos` | `/album/abuelos` |
| `…/los-mas-veteranos` | `/album/los-mas-veteranos` |
| `…/veteranos` | `/album/desde-2021-esperando-familia` |
| `…/ppp-jovenes-1-a-4-anos` | `/album/ppp-jovenes` |
| `…/ppp-adultos-5-a-9-anos`, `…/ppps-en-adopcion` | `/album/ppp-adultos` |
| `…/no-ppps` | `/album/mestizos` |
| `…/gatos`, `…/gatos-en-adopcion` | `/album/gatos` |

> ⚠️ **Las redirecciones apuntan a un 404 hasta que se publiquen los metaobjetos.** Las fichas y
> los álbumes están en borrador, así que `/album/abuelos` todavía no existe. Mientras tanto esas
> 8 URLs, que es lo que Carla reparte por Instagram, están rotas en la web en vivo. O se publica
> el contenido, o se vuelven a publicar los artículos hasta el día del lanzamiento (las 301 se
> quedan puestas y entran solas en cuanto se oculten otra vez).

## Qué queda para publicar

1. Publicar el tema `loveanimalsbcn/main` (ahora el que manda es Horizon de serie, sin configurar:
   ni siquiera pinta `main-menu`, por eso los cambios de menú todavía no se ven).
2. Pasar las 211 entradas de borrador a publicadas: `crea_animales.py publica`.
3. Repasar los *fallbacks* que miran `shop.metaobjects.animal.values`, que solo ven 50 de 200.
