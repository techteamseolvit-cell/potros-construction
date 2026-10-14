# Auditoría SEO — potrosconstruction.com

*Fecha: 14 oct 2026 · Alcance: 15 URLs del sitemap actual · Método: rastreo directo del HTML público.*

> Línea base antes del rediseño. Sirve como respaldo y como checklist para no perder tráfico orgánico.

## 1. Resumen ejecutivo

- Sitio WordPress (tema YOOtheme) con **15 URLs indexables**: 1 home, 6 servicios, 6 institucionales, 1 blog + 1 post y 1 categoría.
- Todas responden **200 OK**, con canonical, Open Graph y viewport. HTML liviano (≈110 KB en servicios) y respuesta rápida (0.25–0.46 s). **La base técnica es sana**.
- Se detectaron **7 incidencias (por página) de prioridad alta, 47 medios y 1 bajos**.
- El mayor riesgo para el rediseño no es técnico: es **perder las URLs y el contenido que ya posicionan**. El mayor potencial es **expandir páginas por servicio × ciudad**.

## 2. Inventario de URLs y métricas

| URL | Title (car.) | Meta (car.) | H1 | Palabras | Img sin alt | Schema |
|---|---|---|---|---|---|---|
| `/` | 72 | 149 | ✓ | 812 | 3/31 | LocalBusiness, Organization, WebSite |
| `/hardscapes-winchester-va/` | 69 | 138 | ✓ | 1050 | 3/31 | — |
| `/patios-winchester-va/` | 58 | 141 | ✓ | 1039 | 3/31 | — |
| `/decks-winchester-va/` | 71 | 153 | ✓ | 1028 | 3/31 | — |
| `/porches-winchester-va/` | 68 | 130 | ✓ | 1044 | 3/31 | — |
| `/fireplaces-winchester-va/` | 71 | 144 | ✓ | 1065 | 3/31 | — |
| `/landscaping-winchester-va/` | 67 | 148 | ✓ | 1012 | 3/31 | — |
| `/about-us/` | 67 | 145 | ✓ | 170 | 3/3 | — |
| `/reviews/` | 56 | 127 | ✓ | 42 | 3/3 | — |
| `/service-area/` | 54 | 146 | ✓ | 94 | 3/22 | — |
| `/faq/` | 56 | 125 | ✓ | 181 | 3/3 | — |
| `/contact-us/` | 62 | 140 | ✓ | 54 | 3/3 | — |
| `/blog/` | 68 | 137 | ✗ | 75 | 4/4 | LocalBusiness, WebSite |
| `/hardscapes-winchester-va-guide/` | 60 | 163 | ✓ | 1200 | 6/6 | — |
| `/category/uncategorized/` | 35 | 0 | ✗ | 1182 | 4/5 | — |

## 3. Hallazgos priorizados

### [Alto] Las 6 páginas de servicio comparten ~1.000 palabras casi idénticas

Los 6 servicios repiten la misma plantilla (31 imágenes, 11 H2; 5 H2 idénticos en las 6 páginas, además de los mismos bloques de proceso, reseñas, FAQ y blog). Google puede tratarlo como contenido duplicado y no distinguir qué página responde a cada búsqueda.

**Acción:** Reescribir cada servicio con contenido único: materiales, proceso, precios orientativos, galería propia, FAQ propio y proyectos reales.

### [Alto] Páginas clave con contenido casi vacío

Reviews (42 palabras), Contact (54), Blog (75), Service Area (94) y About (170) no ofrecen texto indexable suficiente. Reviews no tiene reseñas visibles.

**Acción:** Mostrar reseñas reales con schema Review/AggregateRating, enriquecer About con historia y equipo, y dar a Service Area un contenido por ciudad.

### [Alto] Blog sin H1 y con un solo artículo

/blog/ no tiene H1 y solo existe 1 post (hardscapes-winchester-va-guide). El blog es la principal palanca de tráfico informacional.

**Acción:** Añadir H1 y un calendario editorial (precios, permisos, materiales, comparativas, ideas por estación).

### [Alto] Cobertura geográfica sin páginas propias

Declaran servicio en ~25 ciudades (Winchester, Front Royal, Strasburg, Berryville, Martinsburg, Charles Town, Leesburg, Ashburn, Purcellville, Manassas…) pero solo hay páginas para Winchester, enlistando el resto en texto.

**Acción:** Crear páginas servicio × ciudad con contenido local único, como mayor oportunidad de crecimiento orgánico (ver estrategia).

### [Medio] Schema incompleto y genérico

Solo el home tiene WebSite/Organization/LocalBusiness, y el LocalBusiness trae solo nombre. Faltan dirección, teléfono, horarios, coordenadas, areaServed, logo, sameAs y valoración. Ninguna página de servicio tiene Service, FAQPage o BreadcrumbList.

**Acción:** Implementar JSON-LD completo: HomeAndConstructionBusiness/GeneralContractor, Service por página, FAQPage, BreadcrumbList, Review/AggregateRating y Article.

### [Medio] Imágenes sin texto alternativo

Todas las páginas tienen imágenes sin alt (3–6 por página). Los archivos tienen nombres con errores como "Consctructions".

**Acción:** Alt descriptivos con servicio y ciudad, nombres de archivo limpios, WebP/AVIF y dimensiones explícitas.

### [Medio] Errores de texto visibles en 7 páginas

"Next Lever" (por Level) y "Checkout Out Blog" aparecen en el home y en las 6 páginas de servicio.

**Acción:** Corregir en el rediseño.

### [Medio] Mensaje cruzado entre servicios

La página de porches y otras mezclan texto de hardscapes en hero e intro, y el pie describe al negocio como "deck builder".

**Acción:** Cada página con un H1 y una intención de búsqueda únicos.

### [Medio] Titles largos

9 de 15 titles superan 60 caracteres y se truncan en resultados.

**Acción:** Reescribir titles ≤60 caracteres con servicio + ciudad + marca.

### [Medio] Categoría "uncategorized" indexable

La URL /category/uncategorized/ está en el sitemap, sin meta description y sin H1, y duplica contenido del blog.

**Acción:** Excluir del sitemap y marcar noindex (o eliminar con 301 a /blog/).

### [Bajo] Tres videos de YouTube embebidos en cada servicio

Cada página de servicio carga 3 iframes de YouTube, lo que añade peso y JavaScript de terceros.

**Acción:** Cargar con facade (lazy) y añadir VideoObject schema; en el rediseño el video principal se conserva.

### [Bajo] Enlaces CTA inconsistentes

/contact-us/ y /contact-us (con y sin slash final) y varios textos de CTA diferentes.

**Acción:** Un único patrón de URL y CTAs consistentes.

### [Info] robots.txt con Crawl-delay: 10

Googlebot ignora Crawl-delay, pero otros rastreadores pueden ralentizarse.

**Acción:** Eliminar la directiva; mantener la referencia al sitemap.

## 4. Plan para no perder tráfico en el rediseño

1. **Mantener las 15 URLs actuales** con el mismo slug. Cualquier cambio de URL lleva redirección 301 uno a uno.
2. **Migrar títulos, H1 y textos que ya posicionan** (los 6 servicios + guía de hardscapes) antes de mejorarlos.
3. **Render en servidor / HTML estático**: contenido y enlaces en el HTML, no solo en JavaScript.
4. **Core Web Vitals en verde**: video y 3D con carga diferida, poster, `prefers-reduced-motion`, imágenes WebP/AVIF.
5. **Schema completo** (GeneralContractor, Service, FAQPage, Review, BreadcrumbList, VideoObject).
6. **Sitemap y robots** nuevos, envío a Search Console y monitoreo semanal de rankings durante 90 días.
7. **Lanzamiento en ventana de bajo tráfico** con checklist de redirecciones validado en staging.

## 5. Oportunidad: páginas servicio × ciudad

Hoy existen 6 páginas (todas Winchester). Con 6 servicios × 19 ciudades de su zona de servicio hay **114 combinaciones posibles**; se recomienda priorizar por volumen en Search Console y Ahrefs, empezando por Winchester, Front Royal, Martinsburg, Leesburg y Ashburn.

**Regla:** cada página debe tener contenido local único (proyectos, materiales, normas del condado, FAQ propio). Las páginas plantilla duplicadas perjudican, no ayudan.

## 6. Pendientes de datos (necesitan acceso)

- Google Search Console: consultas, clics y posiciones actuales (para definir qué URLs proteger primero).
- Google Analytics: páginas con más tráfico y conversiones.
- Ahrefs/Similarweb: backlinks y competidores (conectores bloqueados en este entorno).
- PageSpeed / Core Web Vitals reales del sitio actual.
- Ficha de Google Business Profile y reseñas.

## 7. Metodología y límites

Rastreo del HTML servido por el sitio. No incluye rankings, backlinks ni Core Web Vitals de campo, que requieren Search Console y herramientas externas. Los conteos de palabras excluyen scripts, estilos, navegación y pie.