# Páginas y menús

Los menús y las páginas **no son theme**: viven en el admin de Shopify (Contenido → Páginas y
Navegación → Menús). El theme solo pone la plantilla con la que se pintan.

## Estado de la tienda real (05-08-2026)

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

`templates/page.sobre-nosotras.json` — se pinta clonando secciones que ya existían, sin código nuevo:
el molde de «Acoger» para los bloques narrativos, el de los tres pasos para «nuestra labor», la
**Barra de cifras** de la colección y el muro de **Finales felices**.

Orden: intro · cifras · labor · equipo · realidad · solidaria · compitruenos · finales felices · cierre.

El texto sale literal de la página `/pages/sobre-nosotras` de la tienda real (el que escribieron
Amanda, Carla y Lara). Como la plantilla no lleva la sección `main-page`, **el cuerpo que haya en el
admin no se pinta**: para cambiar el texto se toca la plantilla, igual que en la home.

Para verla hay que tener una página con handle `sobre-nosotras` y plantilla `sobre-nosotras`:
- **Tienda de pruebas:** ya creada → `/pages/sobre-nosotras`
- **Tienda real:** la página existe pero sin plantilla asignada. Cuando se publique el theme, hay que
  ponerle la plantilla «sobre-nosotras» desde el admin.

## Menús de la tienda real

- `main-menu` («CATALOGO»): Novedades · Colecciones · Productos · ¿Quiénes somos? · Adopta · Contacto
- `footer-1` («Más información»): Envíos · Cambios y devoluciones · Legal · Cookies · Contacto

Los menús de la tienda de pruebas (`main-menu`, `footer-adopcion`, `footer-colabora`, `footer-legal`)
son los que espera el theme nuevo. **En la tienda real todavía no existen**: hay que crearlos allí
antes de publicar el theme, o el pie saldrá con tres columnas vacías.
