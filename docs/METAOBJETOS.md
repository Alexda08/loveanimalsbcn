# Sistema de álbumes y fichas de animales — metaobjetos

El theme ya tiene todo el código. Lo único que hay que hacer en el **admin de Shopify**
es crear las dos definiciones de metaobjetos, activar sus web pages y dar de alta el contenido.

> **Estado (30-07-2026): HECHO por Admin API en la dev store.** Definiciones `animal` y
> `album` creadas y con web pages activas; 11 álbumes (los 10 de Carla + **GATOS**, que
> existe en la web actual) y **135 animales reales** scrapeados del blog de
> loveanimalsbcn.com: nombres, edades, álbum(es) de cada uno, PPP sí/no y fechas de
> entrada (21 reales del artículo "Los más veteranos", 20 estimadas por "N años en una
> jaula", el resto placeholder `2025-01-01`). Las 8 imágenes del CDN están subidas a
> Archivos (portadas de álbum + galería de Thor, Ciclone, Tuco, Johnny y Rocky).
> **Pendiente:** fotos del resto (los animales viven en embeds de Instagram — hace falta
> navegador o descarga manual), historias y carácter por animal, y las fechas reales de Carla.

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
| Tamaño | `tamano` | Texto de una línea | pequeño / mediano / grande — **key sin ñ** |
| Sexo | `sexo` | Texto de una línea | macho / hembra ("hembra" activa "Adoptada" en el muro) |
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

Los animales viven hoy como artículos del blog (Ciclone, Tuco, Rocky, Jhonny, Woody, Thor, gatos…).

1. Crear una entrada de metaobjeto `animal` por cada uno **reutilizando las imágenes ya
   subidas** (están en Contenido → Archivos si se subieron ahí; si solo están en los
   artículos, re-subirlas a Archivos desde el CDN).
2. Pedir a Carla las **fechas de entrada reales** (las de los mockups son estimaciones,
   salvo Thor/Rocky ≈ 2021).
3. Crear los álbumes y arrastrar cada animal a los suyos (el urgente arriba).
4. **No borrar los artículos antiguos** hasta validar todo con Carla.
5. Después: redirects 301 (Navegación → Redirecciones de URL) de cada URL de blog antigua
   a la nueva URL del metaobjeto.

## 5. Límites conocidos

- `shop.metaobjects.X.values` devuelve **máximo 50 entradas** por tipo. Con el volumen
  actual sobra; si algún día hay +50 animales, el muro de finales felices y el fallback
  del grid de álbumes habría que paginarlos de otra forma (los álbumes en sí no se ven
  afectados: iteran su propia lista).
- Los importes de la licencia PPP del snippet son genéricos a propósito — pendientes
  los reales de Carla.

## 6. Pendiente de Carla

- Email / WhatsApp de contacto (settings de la sección Ficha de animal)
- Fechas de entrada reales de cada animal
- Importes reales de la licencia PPP
- Logo vectorial oficial (hay wordmark SVG provisional: `logo-loveanimalsbcn.svg` / `-blanco.svg`)
