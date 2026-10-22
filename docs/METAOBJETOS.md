# Sistema de álbumes y fichas de animales — metaobjetos

La referencia completa de cómo están montados los animales de la web: qué hay en la tienda, cómo
lo pinta el tema, qué trampas tiene Liquid y cómo se mantiene. Si vas a tocar algo de animales,
empieza por aquí.

> **En una frase.** Cada animal es una entrada del metaobjeto **`animal`**; cada álbum, una
> entrada de **`album`** que lleva una lista ordenada de animales. El tema no guarda ni un dato
> de ningún animal: todo sale de esas entradas, y lo que se cambie en el admin sale en la web al
> momento.

> **Estado a 22-10-2026** (números sacados de la API de la tienda real ese día, detalle en §9):
> **208 fichas** (205 publicadas y 3 en borrador), **11 álbumes**, **497 fotos** distintas en las
> galerías y **275 enlaces de Instagram** en 165 fichas. El tema `loveanimalsbcn/main` está
> **publicado desde el 18-10-2026**, pero la tienda sigue con **contraseña**: el público aún no
> ve nada.

Documentos hermanos:

- [`INDICE-ANIMALES.md`](INDICE-ANIMALES.md): cada ficha con su ID y su enlace de edición. **Está
  desfasado** (es el del alta del 02-09-2026); se regenera con `crea_animales.py indice`.
- [`PAGINAS.md`](PAGINAS.md): las rondas de cambios de Carla, con el porqué de cada una.
- [`CONTENIDO-CARLA.md`](CONTENIDO-CARLA.md): los textos oficiales (de ahí sale la licencia PPP).
- [`../herramientas/README.md`](../herramientas/README.md): qué hace cada script de Python.

---

## 1. Visión general

### Por qué metaobjetos

Antes, los animales vivían como **11 artículos del blog** `/blogs/animales-en-adopcion`, uno por
álbum, escritos a mano: una foto y un párrafo por perro, todo en el mismo texto. No había forma
de contar días, filtrar adoptados, enlazar una ficha suelta ni reutilizar un animal en dos sitios.

Con metaobjetos cada animal es un **dato** con sus campos (fecha de entrada, PPP, convivencias…),
y el tema decide cómo pintarlo. Eso permite:

- un **contador de días esperando** que sube solo, sin tocar nada;
- que un mismo animal esté en **varios álbumes** (Ciclone está en Acogidas, Abuelos y 2021) sin
  copiar su ficha;
- que al marcarlo **adoptado** desaparezca de los álbumes y pase solo al **muro de finales
  felices**;
- que cada animal tenga **su propia URL** para compartir por WhatsApp o Instagram, con su foto en
  la vista previa del enlace.

El blog viejo está archivado (artículos en borrador, handles cambiados a `archivo-…`) y sus URLs
redirigen con 301 a los álbumes nuevos. Ver [`PAGINAS.md`](PAGINAS.md) → «El blog viejo».

### Las URLs

| Qué | URL | Plantilla del tema |
|---|---|---|
| Ficha de un animal | `/pages/animal/<handle>` (p. ej. `/pages/animal/perla`) | `templates/metaobject/animal.json` |
| Un álbum | `/pages/album/<handle>` (p. ej. `/pages/album/gatos`) | `templates/metaobject/album.json` |
| Todos los álbumes | `/pages/nuestros-animales` (página normal) | `templates/page.nuestros-animales.json` |

- **Cuelgan de `/pages/`, no de la raíz.** El prefijo lo pone Shopify; el `animal`/`album` de
  después es el `urlHandle` de la definición. El tema **nunca escribe la ruta a mano**: siempre
  usa `system.url`. Lo que sí hay que escribir bien es lo de fuera del tema (redirecciones, menús,
  posts de Instagram): la primera tanda de 301 apuntaba a `/album/…` y daba 404.
- **La ruta existe solo si el tema PUBLICADO tiene la plantilla de metaobjeto.** Mientras mandó
  Horizon de serie, todas daban 404 aunque las entradas estuvieran publicadas. Desde el 18-10-2026
  manda `loveanimalsbcn/main`, que sí las tiene.
- El `handle` es la URL: **no se cambia**. Las definiciones permiten crear una redirección al
  cambiarlo (`canCreateRedirects`), pero los enlaces ya repartidos por Instagram y WhatsApp
  dependen de ella; mejor no tentar a la suerte.

### Qué ve el visitante

1. En la **home**: el «Peludo destacado» (cuatro animales rotando), la parrilla de los 11
   álbumes, un álbum de muestra (PPP jóvenes, tres fichas) y el muro de finales felices.
2. En **Nuestros animales**: los 11 álbumes y, debajo, el muro con hasta 24 adoptados.
3. En un **álbum**: título, subtítulo, banda de días si es de año, las fichas en el orden del
   admin (sin los adoptados) y al final el desplegable de cómo se tramita la licencia PPP.
4. En una **ficha**: migas, galería con miniaturas, días esperando, datos, convivencias, botones
   (adoptar, acoger si toca, su post de Instagram), contacto, compartir; debajo su historia, su
   carácter y la caja PPP si es PPP; y al final tres «peludos más» de su álbum.

---

## 2. La definición `animal`

Datos de la tienda real (`metaobjectDefinitionByType`, 22-10-2026):

- Nombre interno y tipo: **`animal`**. Campo que da nombre a la entrada en el admin: `nombre`.
- **Publicable** (activo/borrador), **renderizable** (título SEO = `nombre`, descripción SEO =
  `frase`), **tienda online** con `urlHandle: animal` (y opción de redirección al cambiar un handle),
  **traducible**.
- Acceso: el admin lee y escribe; el storefront lee.

| Campo (admin) | Clave | Tipo | Oblig. | Valores | Para qué / dónde sale |
|---|---|---|---|---|---|
| Nombre | `nombre` | texto 1 línea | **sí** | libre | Todo: H1 de la ficha, tarjetas, migas, textos de botones («Quiero adoptar a …») y mensaje de WhatsApp |
| Frase | `frase` | texto 1 línea | no | libre | La cita en cursiva («me flipa la pelota»): ficha, tarjetas de álbum y de la home, peludo destacado. También es la **meta descripción** de la página |
| Galería | `galeria` | lista de archivos | no | solo imágenes | **La 1.ª es la principal**: la de todas las tarjetas, el muro, el peludo destacado y la vista previa al compartir. La ficha las pinta todas con miniaturas |
| Fecha de entrada | `fecha_entrada` | fecha | **sí** | AAAA-MM-DD | Alimenta los **días esperando** (ficha, tarjetas, peludo destacado), el sello «busco familia desde AAAA» y «ya son N navidades aquí dentro». Sin ella no se puede crear la ficha |
| Edad | `edad` | texto 1 línea | no | libre («joven (1–4 años)», «+9 años», «2 años») | Dato de la ficha y línea de datos de las tarjetas (en minúscula) |
| Tamaño | `tamano` | texto 1 línea | no | **`Pequeño` / `Mediano` / `Grande`** (sin validación) | Ídem. **Clave sin ñ**. Se pinta tal cual, por eso va con mayúscula. Los gatos van sin tamaño |
| Sexo | `sexo` | texto 1 línea | no | **`macho` / `hembra`** (validación) | La ficha lo pinta con mayúscula inicial. `hembra` hace que el sello del muro diga «Adopta**da**» |
| PPP | `ppp` | verdadero/falso | no | — | Enciende la línea «PPP · Sí · licencia sencilla» en la ficha y la **caja de licencia PPP** de la historia. Vacío cuenta como «no» |
| Convive con niños | `convive_ninos` | texto 1 línea | no | **`si` / `no` / `consultar`** (validación) | Chip ✓ / ✗ / ? en la ficha. **Clave sin ñ** |
| Convive con perros | `convive_perros` | texto 1 línea | no | ídem | ídem |
| Convive con gatos | `convive_gatos` | texto 1 línea | no | ídem | ídem |
| Historia | `historia` | texto enriquecido | no | libre | Bloque «Su historia» bajo la ficha |
| Carácter | `caracter` | lista de textos | no | una etiqueta por línea | Bloque «Su carácter» (etiquetas en minúscula). **La 1.ª etiqueta** va también en la línea de datos de las tarjetas |
| Estado | `estado` | texto 1 línea | no | **`en_adopcion` / `en_acogida` / `adoptado`** (validación) | Solo `adoptado` cambia algo: lo saca de álbumes, relacionados y modos automáticos, y lo mete en el muro. `en_acogida` **no lo lee el tema** (ver §5.4) |
| Fecha de adopción | `fecha_adopcion` | fecha | no | AAAA-MM-DD | El año del sello del muro («Adoptado · 2026»). Sin ella el sello se queda en «Adoptado» |
| Posts de Instagram | `posts_instagram` | lista de URL | no | `https://www.instagram.com/p/…/` o `/reel/…/` | **El 1.º** es el botón «Su post en Insta» de la ficha; los demás salen debajo como «Más posts: 2 · 3…». Sin enlaces, no sale nada |

Notas:

- En la tienda la descripción del campo `tamano` dice «pequeño / mediano / grande» en minúscula,
  pero todos los valores reales van con mayúscula (67 Mediano, 54 Grande, 2 Pequeño, 85 vacíos).
  Mandan los valores, no la descripción.
- **«Vacunado y con chip» y «Esterilizado» no son campos del animal.** Son textos fijos de la
  sección (`vacunado_valor`, `esterilizado_valor`, «Sí ✓» en todas). Si algún día hay un animal
  sin esterilizar, eso necesita un campo nuevo.
- Los campos con valores cerrados llevan la validación «limitar a valores preestablecidos» para
  que nadie escriba «Sí!» y rompa los chips. `tamano` no la lleva.

---

## 3. La definición `album`

- Nombre interno y tipo: **`album`**. Campo que da nombre a la entrada: `titulo`.
- Publicable, renderizable (título y descripción SEO = `titulo`), tienda online con
  `urlHandle: album`, traducible.

| Campo (admin) | Clave | Tipo | Oblig. | Para qué / dónde sale |
|---|---|---|---|---|
| Título | `titulo` | texto 1 línea | no | El nombre del álbum, **en mayúsculas, literal de Carla**: H1 del álbum, tarjeta, migas y etiqueta «Álbum · …» de la ficha |
| Subtítulo | `subtitulo` | texto 1 línea | no | La línea en cursiva («sabiduría y siestas») en la cabecera y en la tarjeta |
| Portada | `portada` | archivo | no | Foto de la tarjeta (recorte casi cuadrado, 1 : 0,95). Sin portada, los álbumes de año pintan una **cubierta con el año**; los demás, una huella. También es la foto al compartir el álbum |
| Animales | `animales` | lista de `animal` | no | **La lista del álbum, en orden: el orden del admin es el de la web.** Liquid solo lee los **50 primeros** (§6) |
| Animales (continuación) | `animales_mas` | lista de `animal` | no | La cola cuando `animales` ya tiene 50. El tema la pinta detrás, seguida, como si fuera la misma lista. Hoy solo la usa Gatos |
| Es urgente | `es_urgente` | verdadero/falso | no | Badge **URGENTE** en la tarjeta y en el título del álbum. Solo Acogidas |
| Es un álbum de PPP | `es_ppp` | verdadero/falso | no | **Solo** la pestaña «ℹ licencia PPP» de la tarjeta. No se deduce de los animales. Hoy: PPP jóvenes y PPP adultos |
| Año de espera | `anio_espera` | número entero | no | Solo en los «DESDE XXXX»: banda «N días esperando familia» contados desde el **1 de enero** de ese año, en la tarjeta y en la cabecera, y cubierta con el año si no hay portada |

**Por qué dos listas.** Liquid sirve como mucho 50 referencias de una lista, aunque la lista
tenga 82. El 12-09-2026 se descubrió que 28 gatos no salían en ningún sitio por eso (§10). La
solución fue partir la lista: `animales` hasta 50 y el resto en `animales_mas`. **Para quien
edita, es una sola lista que sigue en otro campo.**

**El desplegable de la licencia PPP** del final del álbum **no depende de `es_ppp`**: sale en
todos los álbumes, Gatos incluido, porque así lo pidió Alex el 13-09-2026. Lo controla el ajuste
`mostrar_licencia` de la sección.

---

## 4. Los álbumes de hoy

A 22-10-2026, en el orden en que salen en la web (bloques de `albums-grid`). «Visibles» son los
publicados y no adoptados, que es lo que pinta el álbum.

| Título | Handle | `animales` | `animales_mas` | Visibles | Marcas |
|---|---|---:|---:|---:|---|
| NECESITAMOS CASA DE ACOGIDA | `necesitamos-casa-de-acogida` | 9 | 0 | 9 | urgente · portada (Trans) |
| ABUELOS | `abuelos` | 29 | 0 | 28 | portada (Ciclone) |
| LOS MÁS VETERANOS | `los-mas-veteranos` | 20 | 0 | 20 | portada (Leo) |
| PPP JÓVENES | `ppp-jovenes` | 24 | 0 | 24 | PPP · portada (Rei) |
| PPP ADULTOS | `ppp-adultos` | 43 | 0 | 42 | PPP · portada (Odín) |
| MESTIZOS Y NO PPP | `mestizos` | 34 | 0 | 33 | portada (Nanu) |
| DESDE 2021 ESPERANDO FAMILIA | `desde-2021-esperando-familia` | 20 | 0 | 20 | año 2021, sin portada |
| DESDE 2022 ESPERANDO FAMILIA | `desde-2022-esperando-familia` | 20 | 0 | 18 | año 2022, sin portada |
| DESDE 2023 ESPERANDO FAMILIA | `desde-2023-esperando-familia` | 22 | 0 | 22 | año 2023, sin portada |
| DESDE 2024 ESPERANDO FAMILIA | `desde-2024-esperando-familia` | 25 | 0 | 24 | año 2024, sin portada |
| GATOS | `gatos` | **50** | **32** | 71 | portada (Perla) |

- **Gatos es el único que ha pasado de 50.** `animales` está lleno: todo gato nuevo va al final de
  `animales_mas`.
- **111 animales están en más de un álbum** (el 53 %). Es lo normal: Ciclone es acogida, abuelo
  y de 2021 a la vez.
- **Los cuatro «DESDE XXXX» no llevan portada a propósito**: la tarjeta les pinta la cubierta con
  el año. Las siete portadas se revisaron una a una el 12-09-2026.
- El handle `mestizos` se quedó corto cuando Carla cambió el título a «MESTIZOS Y NO PPP». No se
  toca: cambiarlo rompería las URLs compartidas.

---

## 5. Cómo lo pinta el tema

### 5.1 Plantillas

| Plantilla | Secciones |
|---|---|
| `templates/metaobject/animal.json` | `animal-main` → `animal-historia` → `animal-relacionados` |
| `templates/metaobject/album.json` | `album-main` |
| `templates/page.nuestros-animales.json` | `albums-grid` (11 bloques, título como h1) → `finales-felices` (automático, hasta 24) |
| `templates/index.json` (home) | `peludo-destacado` (bloques: Leo, Tomás, Julieta, Blue) · `albums-grid` (11 bloques) · `album-destacado` (PPP jóvenes, 3) · `finales-felices` (automático, 8) |
| `templates/product.json` | `a-quien-ayudas` (sin bloques: los tres que más esperan) |

> **Los 11 bloques de `albums-grid` están puestos a mano**, en la home y en Nuestros animales.
> Un álbum nuevo **no sale solo**: hay que añadirle un bloque en las dos plantillas desde el
> editor del tema. (Sin ningún bloque, la sección pinta todos los álbumes por orden de handle.)

### 5.2 Secciones

**`animal-main` — Ficha de animal (parte de arriba).** Lee casi todos los campos del animal.

- **Su álbum** (`primer_album`): recorre `shop.metaobjects.album.values` y, en cada uno, las dos
  listas, hasta encontrar al animal. Se queda con **el primero que lo contiene en el orden en que
  Liquid devuelve los álbumes** (por handle, alfabético), no con el más «importante». Ciclone sale
  con «Álbum · ABUELOS», no con Acogidas. De ese álbum salen las migas, la etiqueta «Álbum · …» y
  los relacionados. **Un animal que no está en ningún álbum** no tiene ni migas de álbum ni
  relacionados.
- **Días esperando**: `dias-esperando` desde `fecha_entrada`, con la frase del ajuste `sub_dias`
  («hoy puede ser el último»).
- **Datos**: edad, tamaño, sexo, PPP (texto del ajuste `ppp_valor`) y las filas fijas de vacunado
  y esterilizado (ajustes; vacíos = no salen).
- **Convivencias**: lee `convive_ninos/perros/gatos`; acepta `si`/`sí`, `no` y cualquier cosa
  que contenga `consultar`.
- **Botones**:
  - **«Quiero adoptar a {nombre}»** — siempre, si el ajuste `link_adoptar` tiene enlace (hoy, el
    ancla del bloque de adopción de la home).
  - **«Quiero acogerle»** — solo si el animal está en el álbum del ajuste **`album_acogida`**
    (hoy `necesitamos-casa-de-acogida`), mirando sus dos listas, y `link_acoger` tiene enlace.
    **Ajuste vacío = no sale en ninguna ficha.** El porqué: las acogidas son para perros
    concretos, y con el botón en todas parecía que se podía acoger a cualquiera.
  - **«Su post en Insta»** (texto del ajuste **`texto_instagram`**) — si el animal tiene algún
    enlace en `posts_instagram`, en pestaña nueva, también en los de acogida. Si tiene más de uno,
    debajo: «Más posts: 2 · 3 · …». Ajuste vacío = no sale en ninguna. Carla reparte los álbumes
    por WhatsApp y lo que mejor funciona es que la gente entre al post.
- **Contacto** (ajuste `contacto`) y **compartir**: Instagram (perfil del ajuste
  `instagram_url`), WhatsApp con «Mira a {nombre}, está esperando familia 🐾 {url}» y copiar
  enlace.

**`animal-historia` — Historia y carácter.** `historia` (con `metafield_tag` sobre el campo
entero, no sobre `.value`), `caracter` con la nota del ajuste `nota_etologia` («Valoración
realizada por el equipo del CAACB…», sirve para perros y gatos: cuidado con poner «canina»), y si
`ppp` es verdadero, `licencia-ppp` en modo **caja** con enlace a la guía (`guia_ppp`). Si el animal
no tiene ninguna de las tres cosas, la sección no pinta nada.

**`animal-relacionados` — Más peludos del álbum.** Hasta `max_animales` (3) del mismo
`primer_album`, en el orden del álbum, saltándose al propio animal y a los adoptados.

**`album-main` — Álbum de animales.** Cabecera (subtítulo, título, URGENTE si `es_urgente`, banda
de días si `anio_espera`, «← volver a los álbumes»), parrilla con `animal-card` (con frase)
recorriendo **`animales` y luego `animales_mas`** y saltándose los `adoptado`. Si no queda ninguno,
el texto del ajuste `texto_vacio`. Al final, `licencia-ppp` en modo **desplegable** si
`mostrar_licencia`. **En el editor** avisa si `animales` pasa de 50.

**`albums-grid` — Grid de álbumes.** Con bloques, los álbumes elegidos en su orden; sin bloques,
`shop.metaobjects.album.values`. Ajuste `es_titular_de_pagina`: el título sale como h1 (solo en
Nuestros animales; en la home, h2).

**`album-destacado` — «Así se ve un álbum por dentro».** Un álbum elegido en el ajuste `album`
y sus primeros `max_animales` no adoptados, con botón «Conocer a {nombre}».

**`finales-felices` — Muro de adoptados.** Dos modos:

- **Con bloques «Animal adoptado»** (máx. 12): los elegidos, en su orden, con frase opcional de la
  familia. En el editor avisa si el elegido no está marcado `adoptado`.
- **Sin bloques (lo que hay hoy)**: recorre **los álbumes** (por handle) y sus dos listas,
  recogiendo los `adoptado` sin repetir, hasta `max_animales` (8 en la home, 24 en Nuestros
  animales). Consecuencias: **un adoptado tiene que seguir dentro de algún álbum** para salir; y
  el orden no es por fecha de adopción, sino el de los álbumes (primero Abuelos, al final Gatos).
- La rejilla usa tantas columnas como tarjetas haya y se centra. Si no sale ninguna tarjeta, la
  sección no se pinta (en el editor sí, con un aviso).

**`peludo-destacado` — Peludo destacado (home).** Con bloques (hoy: Leo, Tomás, Julieta y Blue),
rotan esos. Sin bloques, los `max_animales` con la `fecha_entrada` más antigua **sacados de
`shop.metaobjects.animal.values`**, que solo ve 50 animales (§6, discrepancia en §9). Pinta cada
uno con `peludo-slide`: foto, días, sello «busco familia desde AAAA», «ya son N navidades aquí
dentro», frase, «Conocer a {nombre}» y una píldora para compartir por WhatsApp con los días.

**`a-quien-ayudas` — Ellos (ficha de producto).** Con bloques, los elegidos; sin bloques (lo que
hay), los `columns` (3) que más días llevan esperando, **recorriendo los álbumes** (no la lista de
50) y sin adoptados.

### 5.3 Snippets

| Snippet | Qué hace | Lee |
|---|---|---|
| `animal-card` | Tarjeta de animal: foto cuadrada, banda «N días esperando», nombre, línea «edad · tamaño · 1.er rasgo», frase opcional, «Conocerle →» o botón «Conocer a {nombre}» | `nombre`, `galeria` (1.ª), `fecha_entrada`, `edad`, `tamano`, `caracter` (1.º), `frase` |
| `album-card` | Tarjeta de álbum: portada / cubierta con año / huella, banda de días o badge Urgente/Álbum, pestaña «ℹ licencia PPP» si `es_ppp`, título y subtítulo | `portada`, `anio_espera`, `es_urgente`, `es_ppp`, `titulo`, `subtitulo` |
| `feliz-card` | Polaroid del muro: foto, nombre, sello «Adoptado/Adoptada · año», frase de la familia | `galeria` (1.ª), `nombre`, `sexo`, `fecha_adopcion`, `estado` |
| `peludo-slide` | Diapositiva del peludo destacado | como `animal-card` + `fecha_entrada` para el sello y las navidades |
| `dias-esperando` | Días desde una fecha, **calculados en el servidor** y con punto de miles (`1.884`). Nunca negativo | una fecha `AAAA-MM-DD` |
| `licencia-ppp` | Modo `caja` (ficha de un PPP, con su nombre) o `desplegable` (final de los álbumes). Importes reales del apartado 6 de `CONTENIDO-CARLA.md` | — |
| `meta-tags` | Foto al compartir una ficha o un álbum: 1.ª de `galeria` o, si no hay, `portada` | `galeria`, `portada` |

**Los días suben solos, pero con la caché de Shopify.** Se calculan al renderizar, sin JS (el
peludo destacado solo anima la cifra). Una página cacheada puede ir un día por detrás.

### 5.4 Reglas que conviene tener claras

- **`adoptado` lo quita de todo** (álbum, relacionados, álbum destacado, peludo automático, «Ellos»)
  **y lo pone en el muro**, pero **su ficha sigue viva** en su URL, igual que antes (ver §9).
- **`en_acogida` no lo lee el tema.** Lo que hace que un animal sea «de acogida» en la web es
  **estar en el álbum de acogidas**. El estado se mantiene coherente por orden, nada más.
- **Borrador = no existe para Liquid.** Un animal en borrador no sale en ningún álbum ni en el
  muro aunque esté en la lista y marcado `adoptado`, y su URL da 404.
- **El orden lo manda el admin.** Álbumes, relacionados y álbum destacado siguen el orden de la
  lista; para cambiarlo se arrastra.

---

## 6. Límites y trampas de Liquid (comprobados)

Comprobado contra la tienda real el 12-09-2026 con una sonda en un tema de usar y tirar.

1. **Una lista de referencias sirve 50 y para.** `album.animales.value.size` decía 78, pero el
   `for` daba 50 vueltas. Por eso existe `animales_mas`, y **todos los recorridos de álbumes**
   (`album-main`, `animal-main` ×2, `animal-relacionados` ×2, `album-destacado`,
   `finales-felices`, `a-quien-ayudas`) leen las dos listas con este patrón:

   ```liquid
   for parte in (1..2)
     if parte == 1
       assign trozo = album.animales.value
     else
       assign trozo = album.animales_mas.value
     endif
     for a in trozo
       …
     endfor
   endfor
   ```

   Si `animales_mas` llegara también a 50 (habría 100 gatos), haría falta un tercer campo y una
   tercera vuelta.

2. **`shop.metaobjects.X.values` sirve 50 entradas por tipo, por orden alfabético de handle.** Con
   `album` (11) da igual. Con `animal` (208) se queda en `adam … dali`. Por eso los modos
   automáticos recorren **los álbumes**, no los animales. La única sección que aún mira
   `shop.metaobjects.animal.values` es `peludo-destacado` sin bloques.

3. **`| concat` no junta dos listas de referencias** (devuelve la primera tal cual: son drops
   perezosos, no arrays). Por eso el `for parte in (1..2)`.

4. **`.value.first` no es de fiar con listas de referencias.** Se recorre con
   `for x in lista limit: 1` (así lo hacen `animal-main` con los posts y `meta-tags` con la
   galería). Ojo: `animal-card`, `feliz-card` y `peludo-slide` sacan la foto con
   `animal.galeria.value | first` y funciona (0 fotos rotas en los repasos del 12-09 y el 13-09),
   pero para código nuevo, mejor el `for … limit: 1`.

5. **Los borradores no los ve Liquid**, ni en listas ni en `shop.metaobjects`. Un adoptado en
   borrador no sale en el muro.

6. **`metafield_tag` quiere el campo, no el valor**: `animal.historia | metafield_tag`. Con
   `.value` el texto enriquecido no se pinta.

7. **El tema no puede depender de que la lista quepa**: `album-main` avisa en el editor cuando
   `animales` pasa de 50, para que no vuelva a colarse.

---

## 7. Cómo se hacen las tareas habituales desde el admin

Todo está en **Contenido → Metaobjetos** → **animal** o **album**. Cada entrada tiene arriba a la
derecha su **estado** (Activo / Borrador). Lo que se guarda sale en la web al momento.

### Dar de alta un animal nuevo

1. **Contenido → Metaobjetos → animal → Añadir entrada.**
2. Rellenar como mínimo **Nombre** y **Fecha de entrada** (obligatorios). Luego, todo lo que se
   tenga: frase, edad, tamaño (`Pequeño`/`Mediano`/`Grande`, con mayúscula; los gatos, vacío),
   sexo, PPP, las tres convivencias, historia, carácter (una etiqueta por línea), estado
   `en_adopcion` y sus posts de Instagram.
3. **Galería**: subir las fotos. **La primera es la principal**: es la de todas las tarjetas.
   Convención: nombre de fichero `handle-1.jpg`, `handle-2.jpg`… y texto alternativo
   «{Nombre}, perro/gato en adopción en Love Animals BCN».
4. **Handle**: Shopify lo saca del nombre. Si ya existe (dos *Zeus*, dos *Peque*), el segundo
   lleva `-2`. Comprobarlo antes de compartir la URL: después no se cambia.
5. Estado de la entrada: **Activo**. Guardar.
6. **Meterlo en su álbum** (o en varios): abrir el álbum →
   - si **Animales** tiene **menos de 50**, añadirlo ahí;
   - si ya tiene 50 (hoy, **Gatos**), añadirlo al final de **Animales (continuación)**.
   - Arrastrar para ponerlo en su sitio. Si no está en ningún álbum, **su ficha existe pero no se
     llega a ella** desde ninguna página.

### Marcar un adoptado

1. Abrir el animal → **Estado: `adoptado`** y **Fecha de adopción** (si no se sabe, vacía: el
   sello dice «Adoptado» a secas; no inventarla).
2. **Dejarlo publicado y dentro de su álbum.** No sacarlo de la lista ni pasarlo a borrador: el
   muro automático lo encuentra recorriendo los álbumes, y en borrador Liquid no lo ve.
3. Si es una hembra, comprobar `sexo: hembra` para que el sello diga «Adoptada».
4. Una foto «de después» con su familia es lo mejor para el muro: ponerla **la primera** de la
   galería.

### Pasar un animal a acogida (o sacarlo)

1. Abrir **NECESITAMOS CASA DE ACOGIDA** → Animales → añadirlo y ordenarlo. Con eso le sale
   «Quiero acogerle» en la ficha.
2. Por coherencia, poner su **Estado: `en_acogida`** (el tema no lo usa, pero sirve para saber
   quién es quién).
3. Para sacarlo: quitarlo de la lista de ese álbum y volver a `en_adopcion`.

### Añadir un post de Instagram

1. Abrir el animal → **Posts de Instagram** → añadir la URL, del tipo
   `https://www.instagram.com/p/CODIGO/` o `…/reel/CODIGO/` (sin `?igsh=…`).
2. **El orden importa**: el primero es el botón «Su post en Insta»; los demás, «Más posts».
   Arrastrar para cambiar cuál va al botón.

### Cambiar la portada de un álbum

1. Abrir el álbum → **Portada** → cambiar archivo (o subir uno nuevo).
2. Se recorta casi cuadrada: mejor una foto con el animal centrado. Las actuales son verticales,
   1086 × 1448.
3. Antes de borrar la vieja de Contenido → Archivos, comprobar que no la usa nadie más.

### Quitar un animal de la web

- **Pasarlo a Borrador. No borrarlo.** Conserva fotos, historia y posts, y si vuelve (o se le
  quiere en el muro de adoptados) basta con publicarlo. Así se ha hecho con todas las bajas.
- En borrador su URL da 404 y desaparece de todos los sitios, aunque siga en la lista del álbum.
- Si ha fallecido, igual: borrador.

### Crear un álbum nuevo

1. **Contenido → Metaobjetos → album → Añadir entrada**: título en mayúsculas, subtítulo, portada
   o año de espera, las marcas que toquen y sus animales.
2. **Añadirle un bloque en `albums-grid`** de la home y de Nuestros animales (editor del tema).
   Sin eso, el álbum existe en su URL pero no sale en ninguna parrilla.
3. Si es un nuevo «DESDE 2025», sin portada y con **Año de espera** = 2025.

---

## 8. Cambios masivos: el Excel y los scripts

Para no rellenar 200 fichas a mano, los datos llegan en un Excel de Carla y se cargan con scripts
de Python que hablan con la Admin API. El detalle de cada script, sus modos y sus ficheros
intermedios está en **[`herramientas/README.md`](../herramientas/README.md)**. Aquí, el flujo.

### El Excel

**`docs/Love Animals BCN - fichas de los animales.xlsx`**, generado por `excel_animales.py`. Tres
hojas: «Cómo se rellena», «Animales» (cabecera en la fila 1, ejemplo en la 2, datos desde la 3) y
«Listas» (valores válidos). Cabeceras doradas = imprescindibles; granates = opcionales.

| Columna | Campo | Traducción |
|---|---|---|
| Nombre * | `nombre` | tal cual |
| Álbum(es) | listas de los `album` | separados por `;`, por título (se corrigen solas las erratas: `LOS MAS VETERANOS`, `DESDE 2021 ESPERANDO`…) |
| Estado * | `estado` | En adopción → `en_adopcion`, En acogida → `en_acogida`, Adoptado → `adoptado` |
| Fecha de entrada * | `fecha_entrada` | → `AAAA-MM-DD`; **sin ella la fila no entra** |
| Fecha de adopción | `fecha_adopcion` | ídem |
| Sexo | `sexo` | Macho → `macho`, Hembra → `hembra` |
| Edad | `edad` | tal cual |
| Tamaño | `tamano` | `Pequeño` / `Mediano` / `Grande` |
| PPP | `ppp` | Sí → `true`, No → `false` |
| Convive con niños/perros/gatos | `convive_*` | Sí → `si`, No → `no`, Consultar → `consultar` |
| Carácter | `caracter` | separado por comas → lista |
| Frase | `frase` | tal cual |
| Historia | `historia` | → texto enriquecido, un párrafo por bloque |
| Fotos | `galeria` | nombres de fichero de los zips; la 1.ª es la principal |
| Notas | — / `posts_instagram` | «NO PONERLO»/«NO PONERLA» saca al animal; los enlaces de Instagram que haya se extraen aparte |
| código (no tocar) | `handle` | vino vacío: la clave real es el handle sacado del nombre |

Las fotos llegan en zips por álbum dentro de `docs/img_loveanimalsbcn/` (medio giga, **fuera del
repo** por `.gitignore`).

### El circuito

1. **`lee_excel.py`** lee el Excel y lo deja normalizado en `fichas.json` (sin tocar la tienda):
   aparta los «NO PONERLO» y los que no tienen fecha de entrada, corrige erratas de álbum y de
   nombres de foto (la O por el 0), casa cada foto con su zip.
2. **`sube_fotos.py`** sube las fotos a Contenido → Archivos con nombre `handle-N` y texto
   alternativo. Si dos zips tienen una foto con el mismo nombre (Cay y Hedy Lamarr comparten
   `IMG_1352`), manda el zip del álbum del animal.
3. **`crea_animales.py`** da de alta álbumes y fichas por `handle` (`metaobjectUpsert`), los
   enlaza en sus álbumes y los publica.
4. **`insta_extract.py`** saca los enlaces de Instagram de la columna «Notas», casando cada fila
   con su ficha por nombre + fecha de entrada; **`aplica_posts_instagram.py`** los escribe en
   `posts_instagram`. **`vuelca_fichas.py`** hace la foto fija de la tienda que necesita el
   primero.
5. **`adoptados.py`** (04-10-2026) marcó los adoptados de un Excel nuevo y los metió en sus
   álbumes **respetando el tope**: a `animales` si hay hueco, si no a `animales_mas`.
6. **`fichas_nuevas.py`** (22-10-2026) es la plantilla para dar de alta **uno o dos** animales
   sueltos con fotos, publicados y al final de `animales_mas` de Gatos.
7. De control, sin escribir nada: **`audita_excel.py`** (Excel contra lo dicho por WhatsApp),
   **`clasifica_fotos.py`** (ordena las fotos sin dueño en `_sin_dueno/`), **`cruce_fotos.py`** y
   **`huella.py`** (cruce de fotos por huella visual).
8. **`migra_metaobjetos.py`** copió las definiciones de la tienda de pruebas a la real. Ya no
   hace falta.

> ⚠️ **No relanzar `crea_animales.py` tal cual sobre la tienda de hoy.** Se escribió para el alta
> de septiembre y hoy haría daño:
>
> - `upsert` manda **borrador** por defecto: `albumes` o `animales` **despublicarían** todo
>   hasta lanzar `publica`;
> - `enlaza` **sustituye** la lista `animales` de cada álbum por la del Excel: pierde el orden
>   manual, no conoce `animales_mas` y metería los 82 gatos en una lista de la que Liquid solo
>   lee 50;
> - `albumes` vuelve a los títulos y subtítulos de `lee_excel.py` («MESTIZOS», «caballeros con
>   corazón grande») y no pone `es_ppp`.
>
> Para un Excel nuevo, lo seguro es el patrón de `adoptados.py`: tocar solo los campos que
> cambian y añadir a los álbumes respetando el tope de 50.

---

## 9. Estado a 22-10-2026

Sacado de la Admin API (solo lectura) el 22-10-2026.

| | Publicadas | Borrador | Total |
|---|---:|---:|---:|
| En adopción | 182 | 2 (Bony, Xulo) | 184 |
| En acogida | 9 | 1 (Dustin) | 10 |
| Adoptados | 14 | 0 | 14 |
| **Total** | **205** | **3** | **208** |

- **Visibles en los álbumes** (publicadas y no adoptadas): **191**.
- **Adoptados (14, todos publicados y dentro de algún álbum)**: Behia, Bibi & Sepi, Bulma
  (cachorra), Fabrizzio, Felipe, Gnar, Kuka & Kuqui, Laks, Ninu (siamés), Pepinillos, Saitama,
  Seimus, Simba (abuelo) y Thorin. **Solo Gnar tiene fecha de adopción** (05-09-2026); los demás
  salen con «Adoptado» a secas. En la home salen 8 (los primeros por orden de álbum); en Nuestros
  animales, los 14.
- **Las 3 en borrador** (Bony, Dustin, Xulo) no están en ningún álbum. Son bajas de septiembre
  que no se marcaron adoptadas; si Carla las quiere en el muro, hay que publicarlas, ponerles
  `adoptado` y meterlas en un álbum.
- **Galerías**: todas las fichas tienen al menos una foto. **497 fotos distintas** (500
  referencias: alguna foto de pareja está en las dos fichas).
- **PPP**: 84 sí, 39 no, 85 sin marcar (gatos, sobre todo).
- **Instagram**: **275 enlaces** (212 posts y 63 reels) en **165 fichas**; 58 tienen más de uno
  (hasta 10). **43 fichas publicadas no tienen ningún enlace**: 37 en adopción, Mister Jack (en
  acogida) y 5 adoptados (Bibi & Sepi, Felipe, Laks, Pepinillos, Seimus). Son sobre todo de la
  fila 106 del Excel en adelante.
- **Faltan en la tienda**: **Andrés y Kaur**, dos gatos del Excel que siguen sin foto: Carla tiene
  que decir cuál de `docs/img_loveanimalsbcn/_sin_dueno/1-de-quien-es/` es cada uno. Chiquitita y
  Katsuki, que estaban en el mismo caso, se dieron de alta el 22-10-2026.
- **Papaya** es PPP (lo confirmó Alex el 03-09-2026) y lo tiene marcado.

### Lo que falta o conviene mirar

- Las **fechas de adopción** de 13 de los 14 adoptados (Carla).
- Los **posts de Instagram** de las 43 fichas sin enlace.
- Qué hacer con **Bony, Dustin y Xulo** (borrador).
- Las fotos de **Andrés y Kaur**.
- Regenerar [`INDICE-ANIMALES.md`](INDICE-ANIMALES.md), que sigue con los números del 02-09.
- Las discrepancias de código apuntadas al final de §10 (la ficha de un adoptado,
  `peludo-destacado` sin bloques, textos del editor desfasados).

---

## 10. Historia y decisiones

**Julio-agosto 2026 — el diseño y las definiciones.** Se montan las secciones (30-07: peludo
destacado y la página Nuestros animales con 11 álbumes y el muro). Las dos definiciones se crean
en la tienda de pruebas con 139 animales sacados del blog (con fotos de muestra) y se copian a la
real con `migra_metaobjetos.py`, sin contenido. La tienda de pruebas no se migra.

**04-08 — el Excel.** Para no pedirle a Carla 139 fichas en el admin, se le manda un Excel en
blanco con una fila de ejemplo. Vuelve con 111 animales el 12-08 (primer alta) y con **los 219
definitivos el 02-09**, con fotos.

**02-09 — el alta buena.** 200 fichas con 483 fotos y los 11 álbumes (se crea GATOS), todo
publicado. Los handles salen del nombre; la columna «código» volvió vacía. Se descartan las filas
«NO PONERLO».

**03-09 — correcciones de Carla.** Once bajas (diez adopciones y Muso, que falleció; Joker
también falleció), tres altas. Las bajas **pasan a borrador, no se borran**, para el futuro muro.
Los tres nombres repetidos (*Balder*, *Peque*, *Zeus*) se clavan por fecha de entrada para que el
`-2` no baile si Carla mueve una fila. Seis portadas desde `PORTADAS.zip`. Papaya es PPP. Las 301
del blog se corrigen de `/album/…` a `/pages/album/…`.

**06-09 — segunda ronda.** «Reservado» se leía como «ya tiene familia»: pasa a «tímido» en tres
fichas. Guiness a PPP jóvenes. **Gnar, primer adoptado publicado** (05-09-2026). Se descubre que
**un borrador no lo ve Liquid**: las bajas en borrador nunca saldrían en el muro.

**12-09 — los 28 gatos escondidos.** GATOS tenía 78 animales y la página pintaba 49: **Liquid
sirve 50 referencias por lista**. Los 28 últimos (los que entraron entre marzo y agosto) no
salían en el álbum, no se enlazaban desde ninguna página y su ficha no sabía de qué álbum era.
Arreglo: el campo **`animales_mas`** y el patrón `for parte in (1..2)` en todos los recorridos.
Ese día también: el muro apuntaba a animales de la tienda de pruebas y desaparecía (pasa a
recorrer álbumes); «Ellos» de la ficha de producto sacaba siempre a Blue, Cay y Coco por mirar los
50 primeros por orden alfabético (pasa a recorrer álbumes); `og:image` para compartir fichas;
`link_acoger` estaba vacío y «Quiero acogerle» no salía en ninguna; la nota de etología decía
«canina» también en los gatos. La portada de Acogidas era una segunda foto de Leo: se pone la de
Trans.

**13-09 — la pestaña PPP la decide el álbum.** Se calculaba sola (bastaba un PPP dentro) y la
llevaban nueve de once álbumes: parecía que todo era PPP y echaba para atrás. Campo nuevo
**`es_ppp`**, solo en PPP jóvenes y adultos. Ese mismo día, lo contrario para el desplegable de
la licencia: **en todos los álbumes**. Cruce completo de fotos: 493 de 493 vienen del fichero que
el Excel da a cada animal.

**04-10 — los adoptados del Excel nuevo.** Catorce filas con «ADOPTADO/A»: todas marcadas
`adoptado` y publicadas; Simba y Fabrizzio se crean (el Excel viejo decía NO PONERLO); Behia
recibe foto (la asignación de esa foto y la de Fabrizzio se dedujo de la ficha: **pendiente de
que Carla la confirme**). Los que no tenían álbum se meten en los del Excel, porque sin álbum el
muro automático no los encuentra. **No se inventa ninguna fecha de adopción.** El muro de la home
pasa de fijado a automático.

**18-10 — se publica el tema** `loveanimalsbcn/main`. Las URLs de metaobjeto dejan de dar 404
(la tienda sigue con contraseña).

**22-10 — cuarta ronda de Carla.** «Quiero acogerle» **solo en los animales del álbum de
acogidas** (ajuste `album_acogida`). Botón **«Su post en Insta»** con el campo nuevo
**`posts_instagram`**: 273 enlaces en 163 fichas sacados de la columna «Notas» (206 de 206 fichas
casan por nombre + fecha). Altas de **Chiquitita y Katsuki**, con fotos sacadas de `_sin_dueno`
comparando con su post. Ese día se reescribe este documento.

### Decisiones que siguen en pie

- **Nunca se borra un animal**: borrador. Las bajas pueden volver o acabar en el muro.
- **El orden lo pone Carla** arrastrando en el admin; ningún script debe reordenar.
- **Lo que Carla decide por WhatsApp no se escribe en su Excel**: va en el script o en los docs,
  con su motivo. Su fichero sigue siendo suyo.
- **No se deducen datos que tienen consecuencias** (PPP, fechas de adopción): se preguntan.
- **El tema nunca escribe rutas a mano**: `system.url`.
- **El tema nunca recorre `shop.metaobjects.animal.values`** para nada que deba ver a todos (con
  la excepción pendiente de `peludo-destacado` sin bloques).

### Discrepancias encontradas al reescribir (22-10-2026), sin arreglar

- **La ficha de un adoptado** sigue diciendo «N días esperando una familia» y «Quiero adoptar a
  {nombre}»: `animal-main` no mira `estado`. Solo se llega a ella por URL directa o buscador
  (la tarjeta del muro no enlaza).
- **`peludo-destacado` sin bloques** aún usa `shop.metaobjects.animal.values` (50 animales,
  alfabético). Hoy no se nota porque la home tiene cuatro bloques.
- **`a-quien-ayudas`** explica en el editor que elige «de los primeros 50 animales de la lista»;
  desde el 12-09 recorre los álbumes y ve a todos.
- **`album-main`**: el texto por defecto si el álbum queda vacío dice «adoptados o en acogida»,
  pero solo se saltan los adoptados.
- **Los scripts se reconstruyeron del historial de trabajo** (22-10-2026). `lee_excel.py` está
  completo, con las tablas de decisiones de Carla (`BAJAS`, `DUPLICADOS`, `DENTRO`, `HANDLES`,
  `CORRIGE`); a `crea_animales.py` y `clasifica_fotos.py` les faltan los últimos retoques (lo
  avisan en su cabecera), y `crea_animales.py` además es peligroso de relanzar (§8).
