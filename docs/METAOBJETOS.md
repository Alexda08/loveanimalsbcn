# Sistema de álbumes y fichas de animales — metaobjetos

El theme ya tiene todo el código. Lo único que hay que hacer en el **admin de Shopify**
es crear las dos definiciones de metaobjetos, activar sus web pages y dar de alta el contenido.

> **Estado (02-09-2026): el contenido bueno ya está en la TIENDA REAL, con fotos.** Del Excel
> final de Carla salen **200 fichas `animal` + 11 álbumes + 483 fotos** en
> `loveanimalsbcn.myshopify.com`, con todos los campos puestos (nombre, fecha de entrada, edad,
> tamaño, sexo, PPP, convivencias, carácter, frase, historia, estado y galería). Están
> **publicadas**, pero no se ven todavía: falta publicar el tema (§5). Cada ficha con su ID y su
> enlace de edición está en **[`INDICE-ANIMALES.md`](INDICE-ANIMALES.md)**.
>
> **Sigue sin ser el censo cerrado.** Siete fichas se han quedado fuera porque no se sabe qué
> foto les toca, doce están marcadas «NO PONERLO» en el Excel, y cualquier dato puede cambiar
> cuando Carla mande más información. Como el alta va por `handle`, lo que venga después se
> carga encima sin duplicar ni rehacer nada.
>
> La tienda de pruebas (`test-shop-kv2uh85k`) sigue con los **139 animales scrapeados** del
> blog antiguo y 11 álbumes (los 10 + GATOS), con fotos de muestra de dog.ceo/thecatapi.
> Eso es material de preview, no contenido bueno: no se migra, se borrará.

## 1. Crear las definiciones (Configuración → Datos personalizados → Metaobjetos)

### Definición `animal`

Nombre: **Animal** · tipo: `animal`

| Campo (nombre visible) | key | Tipo | Notas |
|---|---|---|---|
| Nombre | `nombre` | Texto de una línea | **requerido** |
| Frase | `frase` | Texto de una línea | la cita del animal ("me flipa la pelota") |
| Galería | `galeria` | Archivo → **lista** | la 1ª imagen es la principal |
| Fecha de entrada | `fecha_entrada` | Fecha | **requerido** — alimenta el contador de días |
| Edad | `edad` | Texto de una línea | texto libre ("joven (1–4 años)", "+9 años") |
| Tamaño | `tamano` | Texto de una línea | **key sin ñ**; el valor se pinta tal cual, así que va como en el diseño: `Pequeño` / `Mediano` / `Grande` |
| Sexo | `sexo` | Texto de una línea | `macho` / `hembra` en minúscula (lo exige la validación); la ficha lo pinta con `capitalize`. "hembra" activa "Adoptada" en el muro |
| PPP | `ppp` | Verdadero o falso | activa el dato PPP y la caja de licencia |
| Convive con niños | `convive_ninos` | Texto de una línea | valores: `si` / `no` / `consultar` — **key sin ñ** |
| Convive con perros | `convive_perros` | Texto de una línea | `si` / `no` / `consultar` |
| Convive con gatos | `convive_gatos` | Texto de una línea | `si` / `no` / `consultar` |
| Historia | `historia` | Texto enriquecido | texto libre de las voluntarias |
| Carácter | `caracter` | Texto de una línea → **lista** | etiquetas del equipo de etología |
| Estado | `estado` | Texto de una línea | `en_adopcion` / `en_acogida` / `adoptado` |
| Fecha de adopción | `fecha_adopcion` | Fecha | opcional, para el año del muro de finales felices |

> Consejo: en los campos con valores cerrados (`estado`, `convive_*`) añadid la
> validación "limitar a valores preestablecidos" con esos valores exactos, así
> nadie puede escribir "Sí!" y romper los chips.

**Opciones de la definición → Storefronts: activar "Web pages"** (plantilla: `animal`).
Así cada animal tiene URL propia y usa `templates/metaobject/animal.json`.

### Definición `album`

Nombre: **Álbum** · tipo: `album`

| Campo | key | Tipo | Notas |
|---|---|---|---|
| Título | `titulo` | Texto de una línea | títulos EXACTOS de Carla (abajo) |
| Subtítulo | `subtitulo` | Texto de una línea | la línea en cursiva ("sabiduría y siestas") |
| Portada | `portada` | Archivo | los álbumes "desde XXXX" pueden ir sin portada: sale la cubierta con el año |
| Animales | `animales` | Metaobjeto (animal) → **lista** | **el orden manual manda**: arrastrar en el admin |
| Es urgente | `es_urgente` | Verdadero o falso | badge URGENTE en la card y en la cabecera |
| Año de espera | `anio_espera` | Número entero | solo en los "desde XXXX"; activa la banda de días (base: 1 de enero) |

**Activar también Web pages** (plantilla: `album`).

### Álbumes a crear (títulos literales de Carla)

1. NECESITAMOS CASA DE ACOGIDA (`es_urgente` ✓)
2. ABUELOS
3. LOS MÁS VETERANOS
4. PPP JÓVENES
5. PPP ADULTOS
6. MESTIZOS
7. DESDE 2021 ESPERANDO FAMILIA (`anio_espera` = 2021)
8. DESDE 2022 ESPERANDO FAMILIA (`anio_espera` = 2022) — y siguientes años según recuento

## 2. Qué hace el theme (ya implementado)

- `templates/metaobject/animal.json` → secciones **Ficha de animal** (`animal-main`),
  **Historia y carácter** (`animal-historia`) y **Más peludos del álbum** (`animal-relacionados`).
- `templates/metaobject/album.json` → sección **Álbum de animales** (`album-main`).
- Secciones para añadir desde el editor: **Grid de álbumes** (home / página Nuestros animales,
  con blocks para elegir y ordenar álbumes) y **Finales felices** (muro de adoptados).
- Snippets: `dias-esperando` (contador server-side con miles es-ES), `animal-card`,
  `album-card`, `licencia-ppp` (caja y desplegable), `paleta-vars`.
- Reglas automáticas: un animal `estado = adoptado` desaparece de álbumes y relacionados
  y aparece en Finales felices. La caja/desplegable PPP solo sale si hay animales `ppp` ✓.
  Los contadores de días se renderizan en servidor y suben solos (sin JS).

## 3. Pasos manuales tras crear las definiciones

1. **Tipografías** (Ajustes del tema → Tipografía) para clavar los mockups:
   - Título (heading): **Cormorant Garamond** (si no está en la biblioteca, EB Garamond)
   - Cuerpo (body): **Figtree**
   - Acento (accent): **Oswald** — todos los rótulos condensados del sistema usan la fuente accent
2. Crear la página **"Nuestros animales"** y añadirle la sección **Grid de álbumes**.
3. En la ficha de animal (editor de plantilla metaobjeto animal): rellenar los enlaces
   «Quiero adoptar», «Quiero acoger», la página de migas y el perfil de Instagram.
4. Añadir **Finales felices** donde toque (home y/o página propia).

## 4. Migración de los animales actuales

Los animales vivían como artículos del blog (Ciclone, Tuco, Rocky, Jhonny, Woody, Thor, gatos…).

1. ~~Crear una entrada `animal` por cada uno~~ — **hecho**, pero no desde el blog: desde el
   Excel que devolvió Carla, con datos mucho mejores que los del blog (historia, carácter,
   convivencias, fechas reales). Ver [`INDICE-ANIMALES.md`](INDICE-ANIMALES.md).
2. ~~Pedir a Carla las fechas de entrada reales~~ — **vinieron en el Excel**, una por animal.
3. ~~Crear los álbumes~~ — **hecho**: los 11, con sus animales en el orden del Excel.
4. ~~Subir las **fotos** y enlazarlas en el campo `galeria`~~ — **hecho el 02-09-2026**: 483
   fotos, renombradas por animal y con texto alternativo.
5. **No borrar los artículos antiguos** hasta validar todo con Carla.
6. ~~Redirects 301 de cada URL de blog antigua a la nueva URL del metaobjeto~~ — **hecho**:
   12 redirecciones y los 8 artículos despublicados. Ver [`PAGINAS.md`](PAGINAS.md).
7. ~~Al publicar el tema: pasar las entradas de borrador a activas~~ — **hecho el 02-09-2026**:
   las 211 están en ACTIVE. No se ven hasta publicar el tema, por lo del recuadro de §5.

## 5. Límites conocidos

> **Las URLs `/album/…` y `/animal/…` dependen del tema PUBLICADO, no del contenido.**
> Shopify decide si esa ruta existe mirando si el tema publicado tiene
> `templates/metaobject/album.json` y `…/animal.json`. Mientras mande Horizon de serie, que no
> las tiene, dan **404 aunque las entradas estén publicadas** — y tampoco valen la cookie de
> vista previa (`?preview_theme_id=…`) ni el dominio de myshopify: la ruta se resuelve antes de
> elegir tema. Comprobado el 02-09-2026 con las 211 entradas ya en ACTIVE.
>
> Para verlas sin publicar el tema: *Tienda online → Temas → `loveanimalsbcn/main` →
> Personalizar*, y en el desplegable de arriba elegir la plantilla **Álbum** o **Animal**.


- `shop.metaobjects.X.values` devuelve **máximo 50 entradas** por tipo, y ya hay 200 animales.
  Solo afecta a los *fallbacks* automáticos (`a-quien-ayudas`, `peludo-destacado`,
  `finales-felices` cuando no llevan bloques puestos a mano): elegirían «el que más lleva
  esperando» mirando solo 50 de 200, así que el resultado sería falso. En la home no pasa
  porque las tres secciones llevan sus bloques fijados. Con `album` no hay problema: son 11.
- Los importes de la licencia PPP del snippet son genéricos a propósito — pendientes
  los reales de Carla.

## 6. El Excel de los animales

Para no pedirle a Carla que rellene 139 fichas a mano en el admin, los datos se piden en un
Excel y se importan de una tacada: **`Love Animals BCN - fichas de los animales.xlsx`**
(se genera con `excel_animales.py`, que lee las entradas de la tienda de pruebas).

Se mandó **en blanco**: la fila 2 es un ejemplo (Woody, en verde y cursiva) para que se vea el
formato, y debajo quedaban 199 filas listas. Tres hojas: «Cómo se rellena» (instrucciones +
qué va en cada columna), «Animales» (la tabla) y «Listas» (los valores válidos).

Volvió con 111 animales el 12-08-2026 y **con los 219 definitivos el 02-09-2026**, ya con la
columna «Fotos» rellena. La copia buena está en `docs/`. De ahí sale el alta de la tienda real;
el detalle del cruce, en [`INDICE-ANIMALES.md`](INDICE-ANIMALES.md).

Las fotos llegan aparte, en zips por álbum, dentro de `docs/img_loveanimalsbcn/`. Son 517
ficheros y medio giga, así que **esa carpeta está en el `.gitignore`**: no entra en el repo.

Convenciones que hacen que la vuelta sea automática:

| Columna del Excel | Campo del metaobjeto | Traducción al importar |
|---|---|---|
| Nombre * | `nombre` | tal cual |
| Álbum(es) | (lista `animales` del `album`) | separados por `;`, por título de álbum |
| Estado * | `estado` | En adopción→`en_adopcion`, En acogida→`en_acogida`, Adoptado→`adoptado` |
| Fecha de entrada * | `fecha_entrada` | fecha de Excel → `AAAA-MM-DD` |
| Fecha de adopción | `fecha_adopcion` | ídem |
| Sexo | `sexo` | Macho→`macho`, Hembra→`hembra` |
| Edad | `edad` | tal cual (texto libre) |
| Tamaño | `tamano` | tal cual: `Pequeño` / `Mediano` / `Grande` |
| PPP | `ppp` | Sí→`true`, No→`false` |
| Convive con niños/perros/gatos | `convive_ninos` / `_perros` / `_gatos` | Sí→`si`, No→`no`, Consultar→`consultar` |
| Carácter | `caracter` | separado por comas → lista JSON |
| Frase | `frase` | tal cual |
| Historia | `historia` | texto → `rich_text_field` (un párrafo por línea) |
| Fotos | `galeria` | nombres de archivo; las fotos llegan aparte y se suben a Archivos |
| Notas | — | solo para hablar entre nosotras (`ya no está` = quitar de la web) |
| código (no tocar) | `handle` | **la clave del upsert**: con código actualiza, sin código crea |

- Las cabeceras **doradas** son los campos imprescindibles; las **granates**, opcionales.
- Los desplegables llevan validación con aviso (no bloquean, pero avisan si se escribe otra cosa).
- Las fotos no se pegan en el Excel: en la columna «Fotos» va el nombre del fichero, y la 1 es
  la principal. Al subirlas se renombran a `handle-1.jpg`, `handle-2.jpg`… para poder buscarlas
  por animal en Contenido → Archivos, y llevan texto alternativo.
- La columna «código» volvió vacía, así que en el alta la clave fue el **handle sacado del
  nombre** (`simba-abuelo`, `rocky-marron`…). A partir de ahora esa es la clave: si Carla manda
  otra versión del Excel, las fichas con el mismo nombre se actualizan en vez de duplicarse.
- **«NO PONERLO» / «NO PONERLA» en la columna «Notas» saca al animal de la web.** Es como Carla
  marca las adopciones cerradas y los que no quiere publicar; el lector los aparta solo.
- Las erratas se corrigen solas al leer: los álbumes mal escritos (`LOS MAS VETERANOS`,
  `DESDE 2021 ESPERANDO`, `ESPERANDO FAMILIA DESDE 2024`) y los nombres de foto copiados a mano
  con la O por el 0 (`OC8F9B97…` → `0C8F9B97…`). Van listadas en `INDICE-ANIMALES.md`.
- **Un mismo nombre de foto puede estar en dos zips y ser dos fotos distintas** de dos animales
  distintos: `IMG_1352` es de Cay en el zip de abuelos y de Hedy Lamarr en el de 2023. El
  reparto se deshace por el zip que corresponde al álbum del animal.
- El álbum **GATOS** ya existe en la tienda real (`gatos`, 81 animales): el Excel final trae 95
  gatos. Vienen sin tamaño ni PPP, que son campos opcionales.
- Los 139 animales scrapeados se quedan en la tienda de pruebas y no se migran: eran
  placeholders (`dump_animales.py` los vuelca a JSON si hiciera falta comparar).

## 7. Pendiente de Carla

Los textos de la web (procesos de adopción y acogida, colabora, guía PPP y datos de contacto) ya
están: salen de **`docs/CONTENIDO-CARLA.md`**, que es la transcripción literal de su documento.
Lo que sigue abierto:

- **Qué foto le toca a Behia, Crowley, Andrés, Chiquitita, Kaur, Rusty y Katsuki.** Son los
  siete que no se han podido subir. Seis vinieron con la casilla «Fotos» vacía y Crowley pide
  un fichero que no está en ningún zip. Sobran 43 fotos que nadie reclama, 22 de ellas en el
  zip de gatos y en tandas de tres seguidas: pinta a que son justo esas
- **La fecha de entrada de Muso**, que es obligatoria y vino vacía. Es lo único que le falta
- **Qué pasa con Joker**: estaba en la primera tanda y ha desaparecido del Excel final. Se ha
  borrado de la tienda; si es un despiste, se vuelve a añadir al Excel y entra solo
- Las portadas de los 7 álbumes que no son «desde XXXX» (ahora también GATOS)
- Adopciones con foto para el muro de **Finales felices**: en esta tanda no hay ni un animal
  en estado «adoptado», así que la sección se esconde sola
- Enlace del grupo de Teaming y titular de la cuenta del IBAN
- Qué parte de cada pedido vuelve a la protectora
- Logo vectorial oficial (hay wordmark SVG provisional: `logo-loveanimalsbcn.svg` / `-blanco.svg`)
