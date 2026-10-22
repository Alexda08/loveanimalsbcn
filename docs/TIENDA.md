# Tienda solidaria

Cómo funciona hoy la parte de tienda de la web: qué se ve, de dónde sale cada cosa y qué hay que
tocar para cambiarla. Estado a **22-10-2026**, con los datos sacados de la tienda real
(`loveanimalsbcn.myshopify.com`) por Admin API.

Diseños de referencia: `design/loveanimalsbcn-collections.html` y `design/loveanimalsbcn-pdp.html`.
El catálogo técnico de cada pieza del tema (sections, bloques, snippets) está en
[`SECCIONES.md`](SECCIONES.md).

---

## 1. La idea: un escaparate, no una tienda

**La web no vende.** Enseña los diseños y manda a la gente a pedirlos fuera:

- Los hace **El Armario de Pris**, una artesana que lo prepara todo **a mano**.
- Se piden por **Instagram** ([@el_armario_de_pris](https://www.instagram.com/el_armario_de_pris))
  o por **WhatsApp** al **674 58 36 89** (`https://wa.me/34674583689`).
- **Parte de cada pedido va a la protectora.** La web no da ningún porcentaje: no está confirmado
  (el catálogo de Pris en Canva dice «10 %», pero Carla no lo ha validado).
- El botón **«Compra aquí»** lleva al Instagram de Pris. El WhatsApp va como enlace en el texto.

Por qué así: la protectora no prepara pedidos ni gestiona stock. Si la web cobrara, alguien tendría
que tramitar cada pedido, y quien los hace ya los recibe por mensaje.

### Los dos interruptores

En **Personalizar → Ajustes del tema → Tienda solidaria**. Los dos están **activados**:

| Ajuste | Qué hace |
|---|---|
| «Modo escaparate (sin compra online)» (`escaparate`) | Quita el carrito de la cabecera, los botones de compra de la ficha y el añadir rápido de las tarjetas |
| «Ocultar los precios» (`ocultar_precios`) | No pinta ningún importe en toda la web (tarjetas, ficha, buscador, carrito) |

Por qué ocultar los precios: los pone quien prepara el pedido, y con la personalización (color,
diseño, foto) el precio final puede cambiar. Los precios **siguen en el admin** (camiseta 15 €,
sudadera 25 €, totebag 15 €), solo que no salen.

**Si algún día se quiere vender por la web:** desmarcar los dos ajustes **no basta**. La ficha de
producto no lleva ni precio, ni selector de talla, ni botón de compra: se quitaron de
`templates/product.json`. Habría que volver a añadirlos desde el editor (bloques *Precio*,
*Selector de variantes* y *Botones de compra* dentro de «Detalles del producto»).

---

## 2. Colecciones y píldoras

### Cómo se forman las colecciones

**Todas son automáticas por etiqueta.** Un producto entra en una colección en cuanto lleva su
etiqueta; no hay que añadirlo a mano.

| Colección | Handle | Etiqueta | En el menú y en las píldoras |
|---|---|---|---|
| Camisetas | `camisetas` | `camiseta` | **sí** |
| Sudaderas | `sudaderas` | `sudadera` | **sí** |
| Totebags | `totebags` | `Totebag` | **sí** |
| Niños | `ninos` | `Infantil` | **sí** |
| Novedades | `novedades` | `novedades` | no (retirada el 22-10-2026) |
| Clásicos | `clasicos` | `Clásicos` | no |
| De la jaula a la vida | `de-la-jaula-a-la-vida` | `jaulavida` | no |
| Mestizos | `mestizos` | `mestizos` | no |
| En mi casa manda el gato | `en-mi-casa-manda-el-gato` | `mandagato` | no |
| Día de la madre | `dia-de-la-madre-2022` | `diamadre` | no |
| Colección Especial de aniversario | `coleccion-especial-de-aniversario` | `adoptar2022` | no |
| Prendas misteriosas | `prendas-misteriosas` | `sorpresa` | no (casi todo en borrador) |

Las que no están en el menú **siguen existiendo** y se pueden abrir por URL, pero no las enlaza
nadie. No se han borrado porque sus etiquetas agrupan los diseños y no molestan.

> Ojo: **las infantiles no llevan la etiqueta `camiseta`**, solo `Infantil`. Por eso salen en Niños y
> no en Camisetas. Es a propósito: si no, se repetirían.

**«Tienda solidaria» es `/collections/all`**, la colección que Shopify crea sola con todo lo
publicado. No es una colección del admin: su título sale como **«Productos»** y no se puede elegir
con el selector de colecciones del editor (por eso las píldoras aceptan un enlace suelto, ver abajo).

### Las píldoras

La barra de píldoras es la section **«Píldoras de colección»** (`chips-colecciones`) de la plantilla
de colección. Hoy son cinco y coinciden con el submenú de «Tienda solidaria»:

**Camisetas · Sudaderas · Totebags · Niños · Otros productos**

- Cada píldora es un bloque. Con **colección** elegida, se marca sola cuando estás en ella.
- Con **«Enlace suelto»** (sin colección) sirve para lo que no es una colección: así está «Otros
  productos» (`/pages/otros-productos`). Ahí el texto hay que escribirlo a mano.
- **Una píldora que apunta a una colección que no existe no pinta nada, sin avisar.** Pasó el
  06-09-2026: de ocho píldoras salían dos.
- A la derecha, el contador de artículos de la colección que estás viendo.

No hay «Todo» ni «Novedades» porque Carla lo pidió el 22-10-2026, sin dar motivo. A «todo» se
llega igualmente desde «Tienda solidaria» del menú y desde las migas de la ficha. La colección
Novedades sigue existiendo (y las «Adoptar es vida» llevan su etiqueta): solo no se enlaza.

---

## 3. La página de colección

Plantilla: `templates/collection.json`. La usan **todas** las colecciones, `/collections/all`
incluida. De arriba abajo:

| # | Sección | Qué es | Dónde se edita |
|---|---|---|---|
| 1 | `cabecera` (section de Horizon) | Entradilla en cursiva + título de la colección + descripción | Entradilla: metacampo de colección `custom.fina`; si está vacío, «mientras esperan, puedes ayudarles con…» (bloque «Línea fina», editor). Título y descripción: admin de la colección |
| 2 | `cifras` — Barra de cifras | Franja granate: **2019** «desde entonces vistiendo a la familia LAB» · **1** «artesana lo prepara todo a mano: El Armario de Pris» · **6 €** «de envío a toda España» | Editor, un bloque por cifra |
| 3 | `chips` — Píldoras de colección | Ver arriba | Editor |
| 4 | `galeria` — Galería de la tienda | Cinta de 28 fotos que pasa sola: «así la lleváis» / **La familia LAB** | Editor, una foto por bloque |
| 5 | `donde` — Franja de impacto | **«Los pedidos se hacen por Instagram o WhatsApp, lo que prefieras»** + botón «Compra aquí» | Editor |
| 6 | `main` — rejilla de productos (Horizon) | Tarjetas de producto | Editor (diseño de la tarjeta); productos, admin |
| 7 | `cierre` | «Cada prenda que sale de aquí / es un día menos esperando para alguno de ellos.» + botón «Conoce a nuestros peludos» | Editor |

Ninguna colección tiene descripción ni `custom.fina` rellenos (salvo «Prendas misteriosas», que tiene
descripción vieja y no está enlazada). Por eso en todas sale el texto de reserva.

### La tarjeta de producto

Dentro de la rejilla, de arriba abajo: **foto** (cuadrada, fondo crema) · **banda de impacto**
(`custom.impacto_corto`) · **título** · **tipo de prenda** (`custom.tipo_prenda`) · botón
**«Ver el diseño»**, que lleva a la ficha.

Hoy **ningún producto tiene esos dos metacampos**, así que la tarjeta queda en foto + título + botón.
No hay precio (ocultos) ni añadir rápido (escaparate).

### La galería de fotos

La pidió Carla: «fotos chulas de gente con la ropa o productos, que vayan cambiando». Fotos
`tienda-01` … `tienda-28` (Contenido → Archivos), alternando el catálogo cuidado con fotos de gente
real que ha comprado. Pie: «Fotos de quienes ya visten SOLIDARIDAD. Tú también puedes formar parte
de este museo. ¡Haz tu pedido!».

Se para al pasar el ratón o con el teclado; con «reducir movimiento» no se mueve y se arrastra a
mano. Cada foto admite pie y enlace.

> **Shopify renombra los `.jpeg` a `.jpg`** al subirlos. Si en la plantilla pone `tienda-02.jpeg`, el
> bloque sale en blanco sin ningún error. Las referencias, siempre con el nombre que da la tienda.

---

## 4. La ficha de producto

Plantilla: `templates/product.json`. Ningún producto usa plantilla alternativa.

### Sección a sección

| # | Sección / bloque | Qué pinta | Dónde se cambia |
|---|---|---|---|
| 1 | `migas` → bloque **Migas de pan** | «Tienda solidaria › Camisetas › título» | Editor. «Tienda solidaria» va a `/collections/all`; el segundo nivel es la colección desde la que llegaste (o la primera del producto) |
| 2 | `main` (Horizon «Información del producto») → **galería** | Fotos con miniaturas, fondo crema, borde y sombra | Fotos: admin del producto. Aspecto: editor |
| 2 | → **Etiqueta de la edición** | Sello pequeño sobre el título | Metacampo `custom.etiqueta` (verde si `custom.etiqueta_eco`). **Vacío en todos** |
| 2 | → **Título** | El título del producto | Admin del producto |
| 2 | → **Claim** (Línea fina) | Frase en cursiva bajo el título | Metacampo `custom.claim`. **Vacío en todos** |
| 2 | → **Caja de impacto** | Caja granate «con esto pagas…» | Metacampos `custom.impacto_frase` / `impacto_icono`. **Vacío en todos** |
| 2 | → **Cómo conseguirlo** (bloque `compra-externa`) | Texto + botón **«Compra aquí»** a Instagram + «ver el catálogo con precios» (Canva) + nota | Editor |
| 2 | → **Garantías** | Tres líneas con ✓ | Editor |
| 2 | → **Desplegables** (Horizon) | Vacío hoy | Editor |
| 3 | `historia` — Historia del diseño | La historia del diseño, con frase destacada y firma | Metacampos `custom.historia_*`. **Vacío en todos: la sección no sale** |
| 4 | `tecnica` — Ficha técnica | Dos tarjetas: **«El producto»** y **«Envíos»** | Editor (ver abajo) |
| 5 | `ayudas` — A quién ayudas | «tu compra les llega directamente a…» / **Ellos**: tres peludos con sus días esperando + «Conocerlos a todos» | Editor. Sin bloques: salen solos los que más llevan esperando |
| 6 | `relacionados` (Horizon) | «También te puede gustar» | Automático (recomendaciones de Shopify) |

**La descripción del producto no se pinta en la ficha.** No hay bloque de descripción: la historia
iba a salir de los metacampos. Aun así **la descripción importa**: Google la lee (datos estructurados
y meta descripción) y sale al compartir el enlace. Por eso se limpió el 22-10-2026 (ver §8).

### Las dos tarjetas de la ficha técnica

| Tarjeta | De dónde salen los puntos |
|---|---|
| **El producto** | Del metacampo `custom.ficha` del producto; **si está vacío, de los puntos escritos en el bloque**. Hoy ningún producto lo tiene, así que salen los de Carla en todos |
| **Envíos** | Siempre los escritos en el bloque |

> Cuidado: si algún día se rellena `custom.ficha` en un producto, **sus puntos sustituyen a los de
> Carla** en esa ficha, no se suman. Y si se rellena `custom.certificaciones`, salen como píldoras
> verdes en «El producto» (el bloque tiene «Mostrar certificaciones» activado). No afirmar
> certificaciones que no estén confirmadas.

---

## 5. Otros productos

Lo que **no es ropa**: tazas, fundas de móvil, bodys, mochilas, llaveros, bolígrafos, puntos de
libro, jabones, detalles de boda, el cuadro con la historia del adoptado. **No son productos de
Shopify**: no tienen ficha, ni precio, ni tallas. Son tarjetas con foto para que se vea qué hay; el
pedido es por mensaje, como todo.

- Página `/pages/otros-productos` (publicada), plantilla `page.otros-productos`
  (`templates/page.otros-productos.json`), section **«Otros productos»** (`otros-productos`).
- Enlazada desde el submenú de «Tienda solidaria» (debajo de «Niños») y desde la última píldora.
- Arriba: «también en la tienda solidaria…» / **Otros productos** (es el h1 de la página) y el texto
  de entrada, que acaba con «TODOS LOS PRODUCTOS SON PERSONALIZABLES con el diseño, frase o foto que
  quieras».
- **12 tarjetas** en rejilla (4 columnas en escritorio, 3 en tableta, **2 en el móvil**).
- Al final, el recuadro de personalización con el Instagram y el WhatsApp de Pris y el botón
  **«Pídelo por Instagram»**.

### Cómo añadir (o cambiar) una tarjeta

1. Subir la foto en **Contenido → Archivos**. Mejor cuadrada o casi (la tarjeta la recorta).
2. **Personalizar** → en el desplegable de plantillas, **Páginas → otros-productos**.
3. En la section «Otros productos», **Añadir bloque → Producto**.
4. Rellenar **Foto**, **Título** y **Una línea** (corta: en el móvil la tarjeta mide media pantalla).
5. Arrastrar el bloque a su sitio y **Guardar**.

Para quitar una, se oculta (ojo) o se borra el bloque. Las fotos que no se usan se quedan en
Archivos (`otros-jabones.jpg`, por ejemplo, quedó fuera el 04-10-2026).

---

## 6. Metacampos de producto (`custom.*`)

Las 16 definiciones existen en la tienda real. **Hoy no hay ni un valor rellenado en ningún
producto** (comprobado el 22-10-2026): se crearon para la tienda de pruebas, donde sí se rellenaron
con datos de muestra, y no se pasaron a la real. Todo lo que depende de ellos **desaparece solo**
cuando están vacíos, así que no se nota ningún hueco.

Se ven en el admin del producto, al final, en **Metacampos** (no están fijados: puede que haya que
abrir «Ver todos»).

| Clave | Nombre en el admin | Tipo | Dónde sale |
|---|---|---|---|
| `etiqueta` | Etiqueta | texto | Sello sobre el título de la ficha y sobre la foto de la tarjeta |
| `etiqueta_eco` | Etiqueta ecológica | sí/no | Pinta ese sello en verde |
| `tipo_prenda` | Tipo de prenda | texto | Línea bajo el título en la tarjeta («Camiseta · unisex y mujer») |
| `impacto_corto` | Impacto (banda) | texto | Banda crema bajo la foto de la tarjeta («= 1 semana de pienso») |
| `impacto_icono` | Impacto (icono) | texto | Emoji de la caja de impacto |
| `impacto_frase` | Impacto (frase) | texto largo | Caja granate de la ficha; lo que va entre `**dobles asteriscos**` sale en dorado |
| `claim` | Claim | texto | Cursiva bajo el título de la ficha |
| `eco_badge` | Sello de la galería | texto | Sello verde sobre la foto grande |
| `historia_fina` | Historia · entradilla | texto | Entradilla de la sección de historia |
| `historia_titulo` | Historia · título | texto | Título grande de esa sección |
| `historia_a` | Historia · texto | texto largo | Párrafos (línea en blanco = párrafo nuevo) |
| `historia_destacada` | Historia · frase destacada | texto largo | Frase grande en cursiva |
| `historia_b` | Historia · cierre | texto largo | Párrafos de cierre |
| `historia_firma` | Historia · firma | texto | Firma |
| `ficha` | Ficha técnica | lista de textos | **Sustituye** los puntos de «El producto» |
| `certificaciones` | Certificaciones | lista de textos | Píldoras verdes en «El producto» |

**De colección:** `custom.fina` (Entradilla) = la cursiva sobre el título. Vacía en todas.

Los de impacto (`impacto_*`) **no conviene rellenarlos** mientras no se sepa qué parte de cada
pedido llega a la protectora: dirían «esta camiseta paga una semana de pienso» sin base.

---

## 7. Dar de alta un producto nuevo (Carla o Alex)

Para una prenda nueva de Pris. (Si no es ropa, no es un producto: es una tarjeta de «Otros
productos», ver §5.)

1. **Productos → Añadir producto.**
2. **Título** como sus hermanos: «Camiseta | Nombre del diseño», «Sudadera | …», «… | Totebag».
   La URL se saca del título **la primera vez que se guarda** y después ya no cambia sola: si luego
   se corrige el título, la URL se queda con el viejo (así nacieron las `copia-de-…`).
3. **Descripción**: la historia del diseño en uno o dos párrafos y, al final, el cierre común
   (§9). No se ve en la ficha, pero es lo que lee Google y lo que sale al compartir.
4. **Fotos**: la primera es la de la tarjeta y la de compartir. Cuadradas si se puede.
5. **Precio**: el de Pris (no se ve en la web, pero queda apuntado).
6. **Variantes**: las opciones como sus hermanos (*Modelo*, *Talla*, *Color*). No se ven en la web
   —la talla se dice por mensaje—, pero sirven si un día se vende online. Una sola variante también vale.
7. **Organización**:
   - **Tipo**: Camiseta / Sudadera / Totebag. **Proveedor**: BCN, como los demás.
   - **Etiquetas**: la que decide la colección (`camiseta`, `sudadera`, `Totebag` o `Infantil`) y,
     si es de una línea existente, la del diseño (`jaulavida`, `mestizos`, `stopleyppp`,
     `elamornosecompra`, `mandagato`, `adoptaresvida`…). **No hace falta `novedades`**: ya no se enlaza.
8. **Estado: Activo** y **canales**: Tienda online (y Buy Button y Shop, como sus hermanos). Sin
   el canal Tienda online no sale en la web aunque esté activo.
9. **Metacampos**: opcionales (§6). Si se quiere, `tipo_prenda` y la historia (`historia_*`): con
   `historia_a` relleno aparece la sección de historia en su ficha.
10. Comprobar en la web: que sale en su colección y en «Tienda solidaria», y que la ficha se ve bien.

**Para retirar un producto**: pasarlo a **Borrador**, no borrarlo. Conserva fotos, textos y
variantes, y se reactiva con un clic. Así están los 22 borradores de hoy.

---

## 8. Los productos hoy (22-10-2026)

**26 activos y 22 en borrador.** De los activos, 25 están en la Tienda online; el otro es
**«Cambio de producto»** (3,90 €, sin foto), un producto interno que solo está en Buy Button, Meta y
Copilot y no se ve en la web.

| Colección | Activos |
|---|---|
| Camisetas | 10 |
| Sudaderas | 10 |
| Totebags | 3 |
| Niños | 2 |

**En borrador** (retirados, no borrados): las camisetas y sudaderas «Sorpresa» y «Giving Tuesday»
(solo para campañas de stock), las dos «De la jaula a la vida | Diseño delantero y trasero» (diseño
retirado), las dos «Adoptar es vida 2022 Aniversario» (el dibujo con silueta, `SILUETAADOPTAR`), las
cuatro de la «Colección Gris» y la tarjeta regalo.

Cosas que se saben y no se han tocado (las decide Carla):

- **«Mestizos - Diseño trasero.»** lleva un guion y un punto que sus hermanos no llevan. Es el
  título del admin; mejor que lo corrija ella.
- **Dos precios distintos**: la camiseta `mestizos` a 17,90 € y la `sudadera-mestizos` a 27,90 €,
  cuando las demás van a 15 y 25. Hoy no se ve (precios ocultos).
- **Tres URLs `copia-de-…`** que no corresponden al título (`/products/copia-de-sudadera-love-animals`
  es «Sudadera: Stop Ley PPP»). Cambiar el handle cambia la URL.
- **No usar `adoptaresvida` y `SILUETAADOPTAR` como si fueran lo mismo**: el primero es la frase
  sola (los dos productos nuevos, a la venta); el segundo, el diseño de 2022 con silueta (retirado).

---

## 9. Textos de Carla vigentes

Todos están en el editor de temas salvo el cierre de las descripciones, que está en cada producto.
Van tal cual los escribió ella, **mayúsculas incluidas**.

**Franja de la colección** (`donde`):
> **Los pedidos se hacen por Instagram o WhatsApp, lo que prefieras**
> Estos diseños los prepara **El Armario de Pris**. Elige lo que te guste, escríbele por Instagram o
> por WhatsApp diciéndole qué producto quieres y ella se encarga del resto. Parte de los beneficios
> se donan a la asociación **De la jaula a la vida**.
> Todos los pedidos y productos pueden PERSONALIZARSE: elige tu TALLA, el COLOR de la prenda, el
> DISEÑO que más te guste e, incluso, podemos poner tus FOTOS favoritas en llaveros, tazas, fundas
> de móvil…
> **@el_armario_de_pris** · **674 58 36 89** — botón «Compra aquí».

**Ficha, «Cómo conseguirlo»**: «Este diseño lo prepara **El Armario de Pris**: escríbele por
Instagram o por WhatsApp (674 58 36 89) diciéndole qué quieres y en qué talla, y ella se encarga del
resto. Parte de cada pedido vuelve a la protectora.» Nota: «Los pedidos se hacen por mensaje
directo, no desde esta web.»

**Ficha, garantías**: «Cada pedido deja algo para **veterinario, pienso y residencias**.» · «Hecho
a mano y **100 % personalizable**.» · «Envío a toda España · gastos de envío aparte.»

**Ficha, «El producto»**:
- Artesanal: todo está hecho a mano
- 100 % personalizable a tu gusto
- Estampación duradera, apta para lavadora
- Ropa de algodón y poliéster, según proveedor
- Velas y jabones veganos y cruelty free, SIEMPRE

**Ficha, «Envíos»**:
- Envíos a toda España
- Plazo: 15 días
- Todo lo hace a mano @el_armario_de_pris: por eso, pedimos paciencia
- Valora el comercio artesanal, solidario y de proximidad
- ¿Dudas con la talla o devoluciones? ¡Escríbenos y lo resolvemos!

**Otros productos**: entrada con «TODOS LOS PRODUCTOS SON PERSONALIZABLES con el diseño, frase o foto
que quieras»; recuadro final con PERSONALIZARSE / COLOR / DISEÑO / FOTOS, Instagram y WhatsApp. Líneas
de tarjeta suyas: bolígrafos «con huellitas y muchas más figuritas», llaveros «de muchas formas y
colores», cuadro «la ficha de tu adoptado, en formato digital», «Detalles para bodas y celebraciones»
«personalizados para cada evento, con o sin tarjeta», jabones «para el día a día».

**Cifras**: «artesana» (no «chica») lo prepara todo a mano.

**Cierre común de las descripciones** (23 productos):
> Lo prepara a mano **El Armario de Pris** y es **100 % personalizable**: eliges la talla, el color
> de la prenda y el diseño. La estampación es duradera y apta para lavadora, y el tejido es de
> algodón y poliéster, según proveedor.
> Los pedidos se hacen por Instagram o por WhatsApp (674 58 36 89), lo que prefieras. Parte de cada
> pedido vuelve a la protectora.

En las tres totebags dice «eliges el color y el diseño» y «la tela». Las dos «Adoptar es vida» tienen
su propio texto (otro color aunque la foto sea blanca; «no admiten devolución»).

**Lo que ya no se dice en ningún sitio**: «algodón orgánico», «certificado PETA, Fair Wear,
Oeko-Tex», «Novedades», el nombre de la empresa de la plataforma anterior. Si alguien lo ve
reaparecer, viene de un texto viejo.

---

## 10. Histórico

| Fecha | Qué |
|---|---|
| 03-08-2026 | Tienda montada al diseño en la tienda de pruebas: colección, ficha, bloques y metacampos. El mismo día, **modo escaparate**: se enseña y se pide por Instagram a Pris |
| 06-08-2026 | Grupos con ajustes de móvil (ancho, altura, «Dónde se ve») |
| 02-09-2026 | Menús de la tienda real: «Tienda solidaria» con Novedades, Camisetas, Sudaderas, Totebags y Niños |
| 03-09-2026 | **Siete prendas retiradas** a borrador (sorpresas, Día de la madre 2022, jaula delantero y trasero, Adoptar es vida 2022). **Galería de fotos** de la tienda (28 fotos) |
| 06-09-2026 | Las píldoras: de ocho, seis apuntaban a colecciones que no existían. Pasan a Todo · Novedades · Camisetas · Sudaderas · Totebags · Niños, y aceptan enlace suelto. Párrafo de **personalizar** en la franja. Alta de **Camiseta y Sudadera «Adoptar es vida»** (solo en blanco); la sudadera de 2022, a borrador |
| 12-09-2026 | Repaso a fondo: las migas de producto iban a una colección que no existía, ahora a `/collections/all`; «dános» → «danos» |
| 04-10-2026 | **Otros productos**: página, 12 tarjetas, entrada del submenú y píldora. Fuera de los textos legales la empresa de la plataforma anterior. Retoques de Carla a Otros productos |
| 05-10-2026 | Título y descripción propios de la portada (ajustes del tema) |
| 18-10-2026 | **Se publica el tema** `loveanimalsbcn/main`. La tienda sigue con contraseña |
| 22-10-2026 | Cuarta ronda de Carla: **pedidos por Instagram o WhatsApp** en franja, ficha, Otros productos y descripciones; «chica» → «artesana»; **fuera «Novedades» y «Todo»**; listas nuevas de «El producto» y «Envíos»; garantías sin certificaciones; **23 descripciones limpiadas** (sin algodón orgánico, PETA/Fair Wear/Oeko Tex ni logos de la tienda vieja). Otros productos: en el móvil, dos columnas iguales y sin desbordar |

El detalle de cada ronda está en [`PAGINAS.md`](PAGINAS.md).

---

## 11. Diferencias conscientes con el diseño

- **La franja «cómo se pide» va antes de la rejilla**, no intercalada tras la primera fila: la
  rejilla de Horizon no admite contenido entre tarjetas sin reescribirla.
- **El botón de la tarjeta dice «Ver el diseño»** y lleva a la ficha: no hay compra en la web.
- **No hay guía de tallas**: las tallas se resuelven por mensaje con Pris.
- **Los números y destacados sobre granate** usan `color8` (#E3C08D, dorado claro) en vez del dorado
  normal: el dorado oscuro sobre granate no llega al contraste mínimo.
- El bloque **«Ahorro»** («Ahorras 4,90 €») existe pero no está puesto: sin precios no tiene sentido.
