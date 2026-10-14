# Potros Construction: rediseño

Rediseño del sitio de Potros Construction (Winchester, VA).

## Contenido

| Ruta | Qué es |
|---|---|
| `site/` | **Versión 1** del home. HTML/CSS/JS estático, **sin dependencias**: hero 3D en WebGL propio, scroll horizontal, mapa de servicio, etc. |
| `docs/seo-audit/` | Auditoría SEO del sitio actual: `.pdf`, `.html`, `.md`, `.csv` y datos crudos `.json` (respaldo) |

## Ver el sitio

```bash
cd site && python3 -m http.server 8080   # abrir http://localhost:8080
```

Para publicarlo como enlace (GitHub Pages / Vercel / Netlify) apuntar al directorio `site/`.
Parámetros de prueba: `?noload` omite el preloader.

## Estado de v1

- Home completo con animaciones: preloader, hero 3D con vuelo de cámara al hacer scroll, manifiesto palabra a palabra,
  servicios en scroll horizontal, contadores, proceso con dibujo isométrico, video (YouTube con carga diferida), mapa de zona de servicio.
- Las 14 páginas internas son *stubs* (`noindex`) con las mismas URLs del sitio actual; se construyen en la siguiente fase.
- `index.html` lleva `noindex,nofollow` mientras sea una vista previa. **Quitarlo al lanzar.**

## Pendientes / por confirmar con el cliente

- Cuál de los 3 videos de YouTube es el del hero actual (`MiFIxfJCo3g` es un provisional).
- Renders y videos de las carpetas de Drive (Renders II, Images II, Project, Best Potros Content): comprimir (WebP/AVIF, MP4/WebM) e integrar.
- Las cifras de "Anatomy of one backyard" vienen del documento *Measurements* del Drive: confirmar que se pueden publicar.
- Reseñas reales, FAQ y textos finales por página.
- Colores: se tomó el rojo del logo; confirmar la paleta de marca.
