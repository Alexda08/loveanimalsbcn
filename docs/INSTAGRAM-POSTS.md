# Enlaces de Instagram por ficha — informe (22-10-2026)

> Foto fija del día en que se cargaron los botones «Su post en Insta». Después de este informe,
> **Chiquitita y Katsuki ya tienen ficha** (con su post), así que la tienda tiene 208 fichas.
> Los datos aplicados están en `herramientas/datos/insta_posts.json` y cómo se rehace todo, en
> [`herramientas/README.md`](../herramientas/README.md#instagram).


Fuente: `excel_nuevo.xlsx` (hoja «Animales», datos desde la fila 3) + `tienda_fichas.json`. Resultado: `insta_posts.json`.

## Cifras

- Filas de datos en el Excel: **219**
- Casadas con una ficha: **206** (todas por nombre + fecha de entrada; ninguna ha necesitado el plan B de «solo nombre»). Cada ficha casa con una sola fila.
- No casadas: **13**
- Fichas en la tienda: 206 (203 publicadas, 3 en borrador). Todas tienen fila en el Excel.
- Animales con enlaces (entran en el JSON): **163**, con **273** enlaces en total (210 posts, 63 reels)

| Enlaces por animal | Animales |
|---|---|
| 0 | 43 |
| 1 | 105 |
| 2 | 35 |
| 3 o más | 23 |

Máximo: 10 enlaces (tyson).

## Filas del Excel que no casan con ninguna ficha

Ninguna tiene una ficha con ese nombre en la tienda (ni parecido). No son errores de casado: son animales que no se subieron.

| Fila | Nombre | Fecha entrada | Notas | Comentario |
|---|---|---|---|---|
| 104 | Carmela NO PONER | 2024-07-19 | NO PONERLA | marcado «NO PONER» |
| 138 | Loki | 2021-10-27 | NO PONERLO | marcado «NO PONER» |
| 159 | Andrés | 2025-03-18 | — | sin ficha en la tienda |
| 160 | Chiquitita | 2025-07-02 | https://www.instagram.com/p/DQxASBViKH0 | **Tiene enlace de Insta pero no ficha** |
| 174 | Kaur | 2025-12-05 | — | sin ficha en la tienda |
| 178 | Muso | — | — | sin fecha de entrada |
| 179 | Rusty | 2026-03-19 | — | sin ficha en la tienda |
| 203 | Ramen | 2026-05-12 | NO PONERLO | marcado «NO PONER» |
| 206 | Kenia | 2026-06-18 | NO PONERLO | marcado «NO PONER» |
| 207 | Liona | 2026-07-14 | NO PONERLO | marcado «NO PONER» |
| 210 | Negrita | 2026-08-07 | NO PONERLO | marcado «NO PONER» |
| 217 | Katsuki | 2022-09-09 | https://www.instagram.com/p/CoeZt85ILVB/?igsh=MTFqOTA1eGdnNzV1Ng== | **Tiene enlace de Insta pero no ficha** |
| 219 | Sakura NO PONER | — | NO PONERLO | marcado «NO PONER» |

## Fichas publicadas que se quedan sin ningún enlace

43 fichas publicadas. Su fila de «Notas» no trae ningún enlace de post/reel.

| Handle | Nombre | Fila Excel | Notas |
|---|---|---|---|
| tim-curry | Tim curry | 106 | — |
| lyle | Lyle | 107 | — |
| balder-2 | Balder | 124 | — |
| crowley | Crowley | 126 | — |
| alexia | Alexia | 130 | — |
| pingu | Pingu | 132 | — |
| sal | Sal | 134 | — |
| kika | Kika | 135 | — |
| boni | Boni | 136 | — |
| dorotea | Dorotea | 139 | — |
| silvy | Silvy | 142 | — |
| betty | Betty | 144 | — |
| atun | Atún | 145 | — |
| nuren | Nuren | 147 | — |
| laura | Laura | 148 | — |
| extreme | Extreme | 149 | — |
| dagzs | Dagzs | 150 | — |
| nata | Nata | 151 | — |
| pirulo | Pirulo | 152 | — |
| siri | Siri | 153 | — |
| adam | Adam | 155 | — |
| dennis | Dennis | 156 | — |
| fiona | Fiona | 157 | — |
| hugo | Hugo | 158 | — |
| lola | Lola | 165 | — |
| seimus | Seimus | 172 | — |
| bulma | Bulma | 173 | — |
| runrun | Runrun | 176 | — |
| xip | Xip | 177 | — |
| pepinillos | Pepinillos | 189 | — |
| pitu | Pitu | 197 | — |
| patu | Patu | 198 | — |
| ninu | Ninu | 199 | — |
| felipe | Felipe | 201 | — |
| reina | Reina | 202 | — |
| neko | Neko | 204 | — |
| aixa | Aixa | 205 | — |
| flipi | Flipi | 208 | — |
| laks | Laks | 209 | — |
| tracy | Tracy | 211 | — |
| bibi-sepi | Bibi & Sepi | 218 | NO PONERLO |
| mister-jack | Mister Jack | 220 | — |
| noi | Noi | 221 | — |

Las 3 fichas en borrador (bony, dustin, xulo) sí tienen enlace y van en el JSON por si se publican.

## URLs descartadas o raras

- **Descartadas: ninguna.** No hay enlaces a perfiles ni códigos con caracteres raros; los 273 códigos tienen 11 caracteres válidos.
- Normalizadas (no descartadas):
  - Fila 85 (y fila 101): usan `instagram.com/reels/<código>` (con «s»); se han pasado a `/reel/<código>/`.
  - Fila 29 (Tom): el mismo post dos veces (una con `https`, otra con `http`, ambas con `?igsh=`); queda uno.
  - Fila 38 (Tyson): 13 enlaces en la nota, 3 repetidos; quedan 10. Uno viene cortado (`://www.instagram.com/p/DVbnRS-jAWz)`, sin «https»): el código es válido y además se repite completo más adelante, así que se ha aprovechado.
  - Parámetros `?igsh=…`, paréntesis y espacios quitados en todos.
- Avisos de «NO PONER» en filas que **sí** tienen ficha publicada (no he tocado nada, para que lo decida Carla):
  - Fila 5 «Simba "abuelo" ADOPTADO» → `simba-abuelo`: notas «NO PONERLO  (https://www.instagram.com/p/DKUbRn8Mgh9) (https://www.instagram.com/reel/DbbTqseNw21/)» (2 enlace(s) en el JSON).
  - Fila 58 «Fabrizzio ADOPTADO» → `fabrizzio`: notas «(https://www.instagram.com/p/C2kmi7MMU-T) - NO PONERLO, SE VA ADOPTADO» (1 enlace(s) en el JSON).
  - Fila 218 «Bibi & Sepi ADOPTADAS» → `bibi-sepi`: notas «NO PONERLO» (0 enlace(s) en el JSON).

## Mismo post en varios animales

Probablemente correcto (parejas, camadas o posts de grupo). No se ha corregido.

| Post | Animales |
|---|---|
| `DM2YjQnMNpx` | gordo (Gordo), rex (Rex), kimera (Kimera), airon (Airon) |
| `COi4cW_Hooa` | kiko (Kiko), tomas (Tomás) |
| `DSkHGlsDNPl` | kiko (Kiko), tomas (Tomás) |
| `DSBAtcZDeGn` | kiko (Kiko), tomas (Tomás) |
| `DLF7GgPs4CG` | chula (Chula), gilda (Gilda) |
| `DDMsEJmCknU` | chula (Chula), gilda (Gilda) |
| `DLDSdM4MfUU` | chula (Chula), gilda (Gilda) |
| `DabBfeWN-x_` | chula (Chula), satin (Satín) |
| `DMzym4UM-qI` | pumba (Pumba), fox (Fox), rocky-marron (Rocky marrón), lou-reed (Lou Reed) |
| `DBQ-uitCpcp` | bonnie (Bonnie), clyde (Clyde) |
| `C-m5sLYie3h` | simba-mali (Simba Mali), melon (Melón) |
| `DU3yK_0DY7v` | simba-mali (Simba Mali), melon (Melón) |
| `Db_HgOhCI_3` | red (Red), mimi (Mimi), morty (Morty), roy (Roy), fran (Fran) |
| `Db6a2yuDvaB` | canica (Canica), mix-max (Mix & Max), ron-harry-hermione (Ron, Harry & Hermione) |
| `DbEaZGijnK-` | charlie (Charlie), ninu-siames (Ninu (siamés)), atari (Atari), bulma-cachorra (Bulma (cachorra)) |
| `DaD--1BjmNm` | xulo (Xulo), huran (Huran), enzo (Enzo) |
