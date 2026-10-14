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

## Cómo agregar los renders y videos reales

| Qué | Dónde | Formato |
|---|---|---|
| Galería "Our work" (hasta 6) | `docs/assets/work/work-01.webp` … `work-06.webp` | WebP, ~1800 px de ancho, <400 KB |
| Video del hero (opcional) | `docs/assets/video/hero.mp4` | MP4 H.264, 1080p, sin audio, <8 MB, en bucle |

Si `hero.mp4` existe reemplaza la escena 3D; si no, se ve la escena 3D de WebGL. Los renders faltantes muestran un marcador discreto.

## Estado de v1

- Home con animaciones: preloader, hero 3D con vuelo de cámara al hacer scroll, manifiesto palabra a palabra, servicios en scroll horizontal,
  galería de renders con parallax y lightbox, proceso con dibujo isométrico y mapa de zona de servicio.
- Paleta = logo de Potros: rojo, blanco y negro.
- Las 14 páginas internas son *stubs* (`noindex`) con las mismas URLs del sitio actual; se construyen en la siguiente fase.
- Todo lleva `noindex,nofollow` mientras sea una vista previa. **Quitarlo al lanzar.**
- No se usa ningún video de YouTube del sitio actual; solo renders e imágenes nuevas.

## Pendientes

- Renders y videos de las carpetas de Drive (Renders II, Images II, Project, Best Potros Content): comprimir e integrar.
- Reseñas reales, FAQ y textos finales por página.
