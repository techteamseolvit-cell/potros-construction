# Revisión SEO del rediseño (preview) y guía de integración

*Fecha: 8 nov 2026. Compara el rediseño con la línea base del 14 oct (`potros-seo-audit.md`).*

## 1. Estado del rediseño frente al sitio actual

| Página | Estado | Title / Meta | H1 | Schema | Observación |
|---|---|---|---|---|---|
| `/` | Rediseñada | 57 / 150 | 1 | GeneralContractor + Service | Title acortado (antes 72) |
| `/hardscapes-winchester-va/` | Rediseñada | 49 / 152 | 1 | Service, FAQPage, Breadcrumb | Conserva H2 y FAQ originales |
| `/about-us/` | Rediseñada | 45 / 145 | 1 | AboutPage, Breadcrumb | Pasa de 170 a ~500 palabras |
| `/contact-us/` | Rediseñada | 47 / 131 | 1 | ContactPage, Breadcrumb | Formulario sin backend (mailto) |
| `/patios-`, `/decks-`, `/porches-`, `/landscaping-winchester-va/` | Rediseñadas | título y meta originales | 1 | Service, FAQPage, Breadcrumb, VideoObject | Texto y H2 originales conservados; sin “Top” en el H1 |
| `/fireplaces-winchester-va/` | **Pendiente** | — | — | — | Faltan fotos de chimeneas / fire pits |
| service-area, faq, reviews, blog, guía de hardscapes | **Pendiente** | — | — | — | Hoy son páginas “Next phase” noindex |

Mejoras ya incluidas frente al sitio actual: alt en todas las imágenes, un solo H1 por página, BreadcrumbList, FAQPage, schema con dirección/teléfono/horario, titles ≤60 caracteres, CTA con una sola URL (`/contact-us/`), sin errores de texto (“Next Lever”, “Checkout Out Blog”).

## 2. Si borras o cambias contenido, ¿afecta al SEO?

Depende de qué se toque. Regla práctica:

| Cambio | Riesgo | Por qué |
|---|---|---|
| Cambiar diseño, colores, imágenes, animaciones | Bajo | Google lee el HTML, no el estilo. Mantén alt y tamaños. |
| Cambiar la **URL** (slug) de una página | **Alto** | Pierde el posicionamiento acumulado si no hay redirección 301. |
| Borrar el **texto** de una página que posiciona | **Alto** | Los H1/H2/párrafos con “servicio + Winchester VA” son lo que Google usa para ubicar la página. |
| Cambiar/eliminar **title, meta description o H1** | Medio-alto | Cambia lo que se muestra y lo que se interpreta en los resultados. Mejorar la redacción es válido; vaciarlos no. |
| Borrar una página sin 301 | **Alto** | Genera 404 y se pierden enlaces entrantes. |
| Quitar schema (JSON-LD) | Medio | Se pierden resultados enriquecidos (FAQ, negocio local). |
| Dejar `noindex` al publicar | **Crítico** | La página desaparece de Google. Todas las páginas del preview lo tienen a propósito. |
| Quitar enlaces internos (menú, footer, tarjetas) | Medio | Se debilita el rastreo y la autoridad entre páginas. |
| Páginas con casi nada de texto (reviews 42 palabras, contact 54) | Ya es un problema | Poco que indexar; conviene enriquecerlas, no vaciarlas más. |

Resumen: se puede cambiar el diseño con libertad; **no** se deben cambiar slugs, borrar el texto principal ni dejar `noindex`. Si se elimina contenido, que sea el duplicado o irrelevante (por ejemplo, el texto de hardscapes repetido en porches), no el específico de cada servicio.

## 3. Riesgos al integrar cada HTML en el sitio actual (WordPress)

1. **Mantener el mismo slug** que aparece en el sitemap, con barra final.
2. **Title, meta description, canonical y JSON-LD** van en el `<head>`: si el plugin SEO del sitio ya los gestiona, usar los de cada HTML y no duplicarlos (un solo title, un solo canonical).
3. **Quitar** `<meta name="robots" content="noindex,nofollow">` de cada página antes de publicar.
4. **Rutas de CSS, JS e imágenes**: los HTML usan rutas relativas (`../assets/`, `../css/`). Hay que subir esas carpetas al hosting y usar URLs absolutas, o integrar cada página con su CSS.
5. **Sitemap**: añadir las páginas nuevas, sacar `/category/uncategorized/` (noindex) y eliminar `Crawl-delay` de robots.txt.
6. **Después de publicar**: enviar el sitemap en Search Console y revisar cobertura, indexación y rankings durante 90 días.
7. **Formulario de contacto**: conectar un servicio real; hoy abre el correo del visitante.

## 4. Pendiente de esta revisión

- El rastreo del sitio en vivo hoy responde con un desafío de Cloudflare (“Attention Required”) a mis solicitudes automatizadas; la comparación usa la línea base del 14 oct.
- No hay datos de Search Console ni Analytics para saber qué páginas protegen más tráfico.
