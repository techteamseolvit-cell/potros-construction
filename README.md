# Potros Construction: rediseño

Rediseño del sitio de Potros Construction (Winchester, VA).

## Contenido

| Ruta | Qué es |
|---|---|
| `docs/` | **Versión 1** del home. HTML/CSS/JS estático, **sin dependencias**: hero 3D en WebGL propio, scroll horizontal, mapa de servicio, etc. |
| `docs/seo-audit/` | Auditoría SEO del sitio actual: `.pdf`, `.html`, `.md`, `.csv` y datos crudos `.json` (respaldo) |

## Ver el sitio

```bash
cd docs && python3 -m http.server 8080   # abrir http://localhost:8080
```

Para publicarlo como enlace (GitHub Pages / Vercel / Netlify) apuntar al directorio `docs/`.
Parámetros de prueba: `?noload` omite el preloader.

## Publicación (GitHub Pages)

El sitio vive en `docs/` y hay un `index.html` en la raíz que redirige a `docs/`, así que funciona con la fuente de Pages en
`/docs` o en la raíz de la rama. URL: `https://<usuario>.github.io/potros-construction/`.

## Medios del sitio (ya integrados)

| Archivo | Origen | Uso |
|---|---|---|
| `docs/assets/video/hero.mp4` (+ `hero-poster.webp`) | *Video 1.mp4* (carpeta Project) | Hero del home, en bucle |
| `docs/assets/video/reveal.mp4` (+ poster) | *Clip 1.mp4* (carpeta Images II) | Sección "See it before we build it": el video avanza con el scroll |
| `docs/assets/work/work-01…06.webp` | Fotos de "Best Potros Content" | Galería "Built work, up close" |
| `docs/assets/cards/*.webp` | Fotos de "Best Potros Content" | Tarjetas de servicios |

Los originales (170-316 MB) **no** se suben al repo: se comprimen (MP4 H.264 720p / WebP) y solo se guardan las versiones web.
Si falla la reproducción del video, el hero cae a la escena 3D de WebGL (`js/hero3d.js`).

## Estado de v1

- Home con animaciones: preloader, hero con video 3D real (y escena WebGL de respaldo), manifiesto palabra a palabra, servicios en scroll horizontal,
  video con scroll-scrub, galería de fotos reales con parallax y lightbox, proceso con dibujo isométrico y mapa de zona de servicio.
- Paleta = logo de Potros: rojo, blanco y negro.
- Las 14 páginas internas son *stubs* (`noindex`) con las mismas URLs del sitio actual; se construyen en la siguiente fase.
- Todo lleva `noindex,nofollow` mientras sea una vista previa. **Quitarlo al lanzar.**
- No se usa ningún video de YouTube del sitio actual; solo fotos y videos nuevos del cliente.

## Pendientes

- Otros clips de *Images II* / *Project* y más fotos de *Best Potros Content*: pendientes de elegir. (*Renders II* no se usa.)
- Reseñas reales, FAQ y textos finales por página.
