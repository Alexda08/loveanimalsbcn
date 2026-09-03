# Sistema de álbumes y fichas de animales — metaobjetos

El theme ya tiene todo el código. Lo único que hay que hacer en el **admin de Shopify**
es crear las dos definiciones de metaobjetos, activar sus web pages y dar de alta el contenido.

> **Estado (03-09-2026): el contenido bueno está en la TIENDA REAL, con fotos.** Del Excel
> final de Carla salen **198 fichas `animal` + 11 álbumes + 488 fotos** en
> `loveanimalsbcn.myshopify.com`, con todos los campos puestos (nombre, fecha de entrada, edad,
> tamaño, sexo, PPP, convivencias, carácter, frase, historia, estado y galería). Están
> **publicadas**, pero no se ven todavía: falta publicar el tema (§5). Cada ficha con su ID y su
> enlace de edición está en **[`INDICE-ANIMALES.md`](INDICE-ANIMALES.md)**.
>
> **Sigue sin ser el censo cerrado.** Cuatro gatos esperan a que Carla diga qué foto les toca,
> once se han ido esta semana (diez adopciones y Muso, que no salió de la panleucopenia) y
> seis están marcados «NO PONERLO». Como el alta va por `handle`, lo que venga después se
> carga encima sin duplicar ni rehacer nada.
>
> Los que se van **no se borran**: pasan a borrador, porque Carla los quiere en el rincón
> feliz en cuanto mande las fotos de las adopciones.
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

> **Las páginas de los metaobjetos cuelgan de `/pages/`, no de la raíz.** La ficha de Perla es
> `/pages/animal/perla` y su álbum `/pages/album/gatos`: ese prefijo lo pone la definición en el
> admin y es el que devuelve `album.system.url`. El theme nunca escribe la ruta a mano, siempre
> usa `system.url`, así que da igual lo que se configure; lo que sí importa es todo lo que se
> escriba fuera del theme —**las redirecciones del blog viejo apuntaban a `/album/…` y llevaban
> a un 404 que no se iba a arreglar ni publicando el tema**. Corregidas el 03-09-2026.
>
> **Y esas URLs dependen del tema PUBLICADO, no del contenido.** Shopify decide si la ruta
> existe mirando si el tema publicado tiene `templates/metaobject/album.json` y `…/animal.json`.
> Mientras mande Horizon de serie, que no las tiene, dan **404 para el público aunque las
> entradas estén publicadas**. Con la cookie de vista previa (`?preview_theme_id=205275332939`)
> sí se ven: es lo que está mirando Carla.

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
- Y al revés: **la misma foto puede estar en dos zips con 322 bytes de diferencia**, que son los
  metadatos de haberla reexportado. Las 13 fotos de gato de `FOTOS WEB QUE FALTAN.zip` están
  también en el de gatos. Por eso `clasifica_fotos.py` empareja por nombre y no por md5.
- **`clasifica_fotos.py` ordena todo lo que no usa nadie** en `_sin_dueno/`: lo que hay que
  preguntar, lo que es de la tienda solidaria, lo que ya tiene nombre (porque el animal se fue)
  y los dos vídeos, que la galería no admite. De 128 fotos sueltas, solo 31 hay que preguntarlas.
- El álbum **GATOS** ya existe en la tienda real (`gatos`, 81 animales): el Excel final trae 95
  gatos. Vienen sin tamaño ni PPP, que son campos opcionales.
- **Tres nombres se repiten y son animales distintos**: un perro PPP y un gato llamados
  *Balder*, un perro abuelo y una gata llamados *Peque*, y dos *Zeus* PPP de distinta edad. El
  segundo de cada par se lleva un `-2` en el handle, y hasta ahora ese `-2` se lo quedaba el que
  apareciera después en la hoja: bastaba con que Carla moviera una fila para que se
  intercambiaran las URLs y, como el alta va por handle, para que uno pisara los datos del
  otro. Desde el 03-09-2026 van clavados en `HANDLES` por fecha de entrada, que es del animal
  y no del sitio que ocupe en el Excel. Si sale un choque nuevo, el lector avisa.
- **Las decisiones que Carla da por WhatsApp no se escriben en su Excel.** Viven en `BAJAS`,
  `DUPLICADOS` y `DENTRO`, dentro de `lee_excel.py`, con su motivo al lado y la fila como clave.
  Así su fichero sigue siendo suyo y aquí queda por qué falta cada uno.
- Los 139 animales scrapeados se quedan en la tienda de pruebas y no se migran: eran
  placeholders (`dump_animales.py` los vuelca a JSON si hiciera falta comparar).

## 7. Pendiente de Carla

Los textos de la web (procesos de adopción y acogida, colabora, guía PPP y datos de contacto) ya
están: salen de **`docs/CONTENIDO-CARLA.md`**, que es la transcripción literal de su documento.
Lo que sigue abierto:

- **Si Papaya es PPP o no.** Carla la movió a «PPP ADULTOS», pero en su fila la casilla PPP
  sigue diciendo *No*. Es la única del Excel con esa contradicción. Mientras no lo diga, la
  ficha sale sin la línea de PPP ni la caja de licencia, aunque el álbum diga lo contrario: no
  es cosa de deducirlo, que de ahí cuelgan licencia y seguro
- **Qué foto le toca a Andrés, Chiquitita, Kaur y Katsuki.** Son los cuatro gatos que quedan
  sin subir: las cuatro casillas «Fotos» vinieron vacías. Está preparado para que sea un
  minuto: en **`docs/img_loveanimalsbcn/_sin_dueno/1-de-quien-es/`** hay **ocho gatos** y siete
  perros, cada foto con su grupo en el nombre (`gato-2-atigrado-dorado__…`) y todas juntas en
  `_todas-juntas.jpg`. Basta con que diga qué grupo es cada uno; los otros cuatro gatos serán
  tomas de más de alguno que ya está publicado
- **La portada de «Necesitamos casa de acogida»**, la de Trans. Es la única que falta: mandó
  `PORTADAS.zip` con siete fotos y la lista de a qué álbum va cada una, pero el fichero
  `85F21429-41F2-4D26-AA52-49015579EC84` no viene en el zip. En su sitio sobra una segunda
  foto de Leo (`E1BCDC46…`), que no está en su lista. Los otros seis álbumes ya la tienen;
  los cuatro «DESDE XXXX» no llevan, que la card les pinta la cubierta con el año
- **Adopciones con foto para el muro de Finales felices.** Ya hay once bajas esperando ahí en
  borrador (Behia, Bony, Dustin, Saitama, Thorin, Xulo y los que ni llegaron a subirse);
  faltan sus fotos de «después». Carla quiere aprender a añadirlos ella
- **Los gatos que faltan del final del Excel.** Los dio por perdidos, pero están todos
  subidos: xip, Kuka & Kuqui, Pitu, Patu, Ninu, Pepinillos, Canica, Mix & Max, Ron/Harry/
  Hermione, Huran, Felipe, Reina, Aixa, Flipi, Tracy y Enzo salen en el índice. Lo que no
  se veía eran los enlaces del menú, que no funcionaban (ver el commit de las anclas)
- Logo vectorial oficial (hay wordmark SVG provisional: `logo-loveanimalsbcn.svg` / `-blanco.svg`)

### Resuelto el 03-09-2026

- **Portadas de los álbumes**: seis puestas desde `PORTADAS.zip` con la lista que mandó Carla
  (Ciclone en Abuelos, Leo en Los más veteranos, Rei en PPP jóvenes, Odín en PPP adultos, Nanu
  en Mestizos y Perla en Gatos). Se suben con `sube_portadas.py`, que se puede relanzar: si el
  álbum ya tiene portada, no la toca. Comprobado que un `upsert` de álbumes **no** las borra
- **Papaya sí es PPP**: lo confirmó Alex. La corrección va en `CORRIGE`, dentro de
  `lee_excel.py`, sobre la fila 64, sin tocar el Excel de Carla
- **Teaming**: `https://www.teaming.net/adopta-loveanimals-bcn-delajaulaalavida-`, ya puesto en
  el botón de la home y en el menú del pie
- **Titular del IBAN**: «Asociación animalista sin ánimo de lucro *De la jaula a la vida bcn*»,
  junto al número en la home y en «Quiénes somos»
- **Qué parte de cada pedido vuelve**: no hay una cifra. Cambia con cada producto y lo calcula
  la chica que los prepara, así que la web dice «parte de los beneficios se donan a la
  asociación» y no promete porcentajes
- **Muso**: falleció, no hacía falta la fecha de entrada
- **Joker**: falleció también. El borrado estaba bien
- **Sakura**: era la misma gata que «Nina (abuelita)», con dos nombres
