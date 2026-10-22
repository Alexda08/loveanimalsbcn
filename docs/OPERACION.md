# Operación: cómo se publica, cómo se prueba y qué no hay que romper

La guía para quien coja el proyecto mañana. Lo que hace cada pieza está en los otros docs (ver el
[README](../README.md)); esto es **cómo se trabaja** con él sin llevarse un susto.

## 1. Dónde vive cada cosa

| Qué | Dónde |
|---|---|
| Tienda real | `loveanimalsbcn.myshopify.com` → **loveanimalsbcn.com** (plan Basic, EUR) |
| Tienda de pruebas | `test-shop-kv2uh85k.myshopify.com` (dev store; solo para probar estructura, sus datos están viejos) |
| Tema | **`loveanimalsbcn/main`**, id `205275332939`, base **Horizon 4.1.3** |
| Código | GitHub `Alexda08/loveanimalsbcn`, rama `main`, conectada al tema por la integración de GitHub de Shopify |
| Datos (animales, álbumes, productos, páginas, menús) | En la tienda, no en git. Se tocan desde el admin o por Admin API (`herramientas/`) |
| Fotos originales de Carla | `docs/img_loveanimalsbcn/` (zips; fuera de git por tamaño) |
| Diseños de referencia | `design/*.html` (home, ficha de perro, colecciones, producto, quiénes somos) |

## 2. Publicar: **un push a `main` sale en vivo al momento**

Desde el **18-10-2026** `loveanimalsbcn/main` es el **tema publicado**. La integración de GitHub
sincroniza en los dos sentidos:

- **git → tienda**: cualquier commit que llegue a `main` en GitHub se aplica al tema publicado en
  segundos. No hay paso de «publicar».
- **tienda → git**: lo que se cambie en el editor de temas (textos, secciones, `settings_data.json`)
  lo commitea Shopify solo en `main`. **Antes de editar plantillas JSON en local, `git pull`**, o
  se pisan los cambios que hayan hecho desde el editor.

**Regla del proyecto:** el asistente (Claude) hace los commits **en local**; **el push lo hace
Alex**, o lo autoriza explícitamente cada vez.

Los cambios de **datos** (fichas de animales, descripciones de producto, menús) no pasan por git:
se hacen en la tienda y son inmediatos. Se dejan escritos en `docs/PAGINAS.md`.

### La trampa de la sincronización

Shopify **valida cada plantilla JSON al sincronizar y la descarta en silencio** si usa una fuente
dinámica (`{{ product.metafields.custom.X.value }}`) cuyo metacampo **no existe en esa tienda**. El
síntoma: el editor dice «No se han encontrado plantillas…» o al tema le faltan ficheros que en git
sí están. Arreglo: crear primero la definición del metacampo en la tienda y volver a sincronizar.
Comprobación: comparar `git ls-files templates` con los ficheros del tema en el admin.

## 3. La tienda tiene contraseña

A 22-10-2026 la tienda online sigue con **contraseña** (Tienda online › Preferencias). Quien la
tiene la ve normal; el resto, la pantalla de contraseña. **Toda vista previa también redirige a
`/password`**, así que un tema de pruebas no se puede enseñar a nadie sin la contraseña.
Quitarla es decisión de Carla/Alex: es el paso que abre la web al público.

## 4. Tokens y credenciales

- La Admin API se usa con dos apps propias, una por tienda. Sus tokens (`shpat_…`) los tiene Alex.
- **Nunca van en un fichero del repo.** Los scripts los leen de `LA_TOKEN_REAL` / `LA_TOKEN_DEV`;
  el CLI de temas, de `SHOPIFY_CLI_THEME_TOKEN`.
- `claude-resume.txt` (notas locales de Alex) está en `.gitignore`. Comprobado el 22-10-2026: no
  hay ningún token en todo el historial de git.
- La contraseña de la tienda y las de admin no las introduce el asistente: las pone Alex.

## 5. Probar antes de que salga en vivo

Como `main` es lo publicado, lo arriesgado se prueba fuera:

1. **Theme Check**: `shopify theme check` (o la extensión de VS Code). Los ficheros tocados deben
   quedar sin avisos nuevos.
2. **Tema de prueba sin publicar**, con el CLI y el token:
   ```bash
   SHOPIFY_CLI_THEME_TOKEN=shpat_… SHOPIFY_FLAG_STORE=loveanimalsbcn.myshopify.com \
     shopify theme push --unpublished --theme "prueba"
   ```
   **El primer push a un tema recién creado deja ficheros fuera y da 404**: se repite el push contra
   el id que devuelve y ya renderiza. Se mira con `?preview_theme_id=<id>` (con la contraseña de la
   tienda puesta) y **se borra al acabar**.
3. **`shopify theme dev`** contra la tienda de pruebas: lanzar siempre con `--ignore "*.tmp*"`,
   porque los temporales de OneDrive envenenan la subida («Failed to Upload», con un error falso de
   `color_palette`).
4. **Plantillas JSON**: empiezan con un comentario `/* … */`; para editarlas con un script hay que
   quitarlo, parsear, y volver a volcar con `indent=2, ensure_ascii=False`.

## 6. Verificar en el navegador (lo que se ha aprendido revisando)

- **Por encima de 990 px Horizon hace scroll dentro de `.page-wrapper`, no de la ventana.**
  `window.scrollTo` y `scrollIntoView` no hacen nada útil; hay que desplazar el propio
  `.page-wrapper` (o hacer scroll con la rueda). En móvil sí se desplaza la ventana.
- **Móvil**: la ventana de Chrome no debe estar maximizada, o no se puede estrechar. A 360 px de ancho
  hay que comprobar que `document.documentElement.scrollWidth` no supera `clientWidth`: si lo hace,
  algo se sale por la derecha.
- **Shopify no deja meter la tienda en un `<iframe>`**, ni desde su propio dominio
  (`frame-ancestors`): no sirve para simular un móvil.
- **Imágenes con carga diferida**: una tarjeta «sin foto» en una captura hecha justo después de bajar
  rápido suele estar todavía cargando. Mirar `img.complete` antes de darlo por roto.
- **Animaciones de entrada**: una captura a media animación puede enseñar elementos montados unos
  encima de otros. Repetir la captura antes de tocar nada.
- **Contar texto en el HTML engaña**: el HTML lleva también los datos estructurados (JSON-LD) y
  la descripción de producto, aunque no se pinten. Para «sale en pantalla» hay que mirar el texto
  visible.
- **Instagram sin sesión**: `https://www.instagram.com/p/CODIGO/embed/` enseña la foto del post
  (los reels a veces no cargan; la página normal sí, tras rechazar las cookies opcionales).

## 7. Trampas de Liquid y de Horizon que ya han mordido

- Una **lista de referencias a metaobjetos solo sirve 50** elementos en un `for`, y
  `shop.metaobjects.X.values` también se queda en 50. Por eso los álbumes tienen dos listas
  (detalle en `docs/METAOBJETOS.md`).
- **Liquid no ve los metaobjetos en borrador.**
- En un setting de plantilla, un metacampo debe acabar en `.value`; un `richtext` exige que el
  primer nivel sean `<p>`, `<ul>`, `<ol>` o `<h1-h6>`; `inline_richtext` no admite `<br>`.
- Los settings de tipo `metaobject` en las plantillas JSON guardan el **handle**, no el gid.
- **Grupos con altura «Rellenar» apilados en móvil se cortan**: en móvil, `height_mobile: "fit"`.
- **Rejillas en móvil**: usar `minmax(0, 1fr)` y no `1fr`, o una palabra larga («CELEBRACIONES»)
  ensancha su columna y saca la página por la derecha.
- Los números de teléfono en textos llevan espacios de no separación (`674 58 36 89`) para que
  no se partan en dos líneas.

## 8. A quién se pregunta qué

- **Carla** (voluntaria de la protectora): todo el contenido. Animales, textos, fotos y qué se
  publica. Manda Excel, zips y audios por WhatsApp. Su Excel no se edita: lo que dice por WhatsApp
  se apunta en `docs/INDICE-ANIMALES.md` / `docs/PAGINAS.md` y se aplica en la tienda.
- **El Armario de Pris** (artesana): hace y vende los productos. Pedidos por Instagram
  `@el_armario_de_pris` o WhatsApp `674 58 36 89`.
- **Formularios de la web**: todo debe llegar a `loveanimalsbcn@gmail.com`.

## 9. Pendiente a 22-10-2026

- **Contraseña de la tienda**: quitarla cuando se quiera abrir la web al público (§3).
- **Admin, a mano (Alex)**: email de contacto y remitente de la tienda → `loveanimalsbcn@gmail.com`;
  revisar que las notificaciones y el checkout no nombren a la empresa de la plataforma anterior.
- **Animales**: Andrés y Kaur sin ficha (falta saber cuáles son sus fotos); 43 fichas sin post de
  Instagram (lista en `docs/INSTAGRAM-POSTS.md`); confirmar con Carla que la foto de Chiquitita es
  ella.
- **Tema de prueba olvidado**: `sonda-ronda` (id `210734743883`), creado el 22-10-2026 para probar
  la cuarta ronda, sigue en la tienda sin publicar. Se puede borrar.
- **Posibles fallos de código** vistos al documentar (22-10-2026), sin arreglar:
  - la ficha de un **adoptado** sigue diciendo «N días esperando» y «Quiero adoptar a …»
    (`animal-main` no mira `estado`); solo se llega a ella por URL directa;
  - `peludo-destacado` **sin bloques** aún mira `shop.metaobjects.animal.values` (50, alfabético);
    hoy tiene cuatro bloques y no se nota;
  - textos por defecto viejos en bloques nuevos: `garantias` («certificado PETA, Fair Wear y
    Oeko-Tex»), `franja-impacto` (cuentas de pienso y vacuna), `compra-externa` (solo Instagram);
    textos de ayuda desfasados en `a-quien-ayudas` y `album-main`;
  - ocho sections propias siguen con `repeat(N, 1fr)` (§7): sin desbordes hoy, pero un título
    largo nuevo podría provocarlo;
  - las dos «Adoptar es vida» dicen «no admiten devolución» y la tarjeta «Envíos» invita a
    escribir por devoluciones;
  - las migas de un producto al que se llega desde Google pueden mostrar «Novedades» o
    «Clásicos», que ya no están en el menú.
  Detalle en `METAOBJETOS.md` §10 y `SECCIONES.md` §6.
- **Opcional, ofrecido y sin decidir**: enlaces de «Cambios y devoluciones» y «Guía de tallas» en el
  pie; desactivar el checkout del todo; las tres URL `copia-de-…` de productos; meta descripciones
  más ricas en las fichas.
