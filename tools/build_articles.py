"""Regenera las páginas de noticias y créditos. Solo requiere Python estándar."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
index = (ROOT / 'index.html').read_text(encoding='utf-8')
header = re.search(r'<header class="site-header">.*?</header>', index, re.S).group()
footer = re.search(r'<footer class="site-footer">.*?</footer>', index, re.S).group()

def shell(title, description, content, nested=False):
    prefix = '../' if nested else ''
    page_header = header.replace('href="#', f'href="{prefix}index.html#').replace('src="assets/', f'src="{prefix}assets/')
    page_header = page_header.replace(' class="active" aria-current="location"', '')
    page_footer = footer.replace('href="#', f'href="{prefix}index.html#').replace('href="creditos.html"', f'href="{prefix}creditos.html"')
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Bitora</title><meta name="description" content="{description}"><meta name="theme-color" content="#050713">
<link rel="icon" href="{prefix}assets/logo.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/styles.css"><link rel="stylesheet" href="{prefix}assets/theme.css"><script src="{prefix}assets/app.js" defer></script></head>
<body><a class="skip" href="#contenido">Saltar al contenido</a>{page_header}
<main class="wrap" id="contenido">{content}</main>{page_footer}</body></html>'''

articles = [
    {
        'slug': 'apple', 'title': 'Apple presenta iPhone 18 Pro, iPhone Duo y nuevos accesorios',
        'summary': 'Un iPhone que se despliega, una nueva generación Pro y novedades para tus oídos y tu muñeca. Estas son las claves del anuncio de Apple.',
        'category': 'Lanzamientos', 'tag': '', 'date': '2026-09-09', 'date_label': '9 de septiembre de 2026', 'minutes': 3,
        'alt': 'Composición ilustrativa de teléfonos iPhone',
        'caption': 'Composición ilustrativa de iPhone incorporada al proyecto. No es una fotografía oficial de los dispositivos anunciados.',
        'body': '''<p>Apple presentó el 9 de septiembre una renovación de su catálogo que incluye iPhone 18 Pro y Pro Max, el plegable iPhone Duo, AirPods 5 y nuevos Apple Watch. El anuncio reúne propuestas para quienes buscan un celular, audífonos o un reloj conectado.</p>
<h2>El cambio de formato: iPhone Duo</h2>
<p>La novedad más visible es el primer iPhone plegable de Apple. El Duo combina una pantalla exterior de 5,4 pulgadas con otra interior de 7,6 pulgadas. Al abrirlo, ofrece más superficie para leer, jugar o utilizar aplicaciones.</p>
<p>Apple anuncia el chip A20 Pro y una experiencia de iOS 27 adaptada al formato, con funciones de Apple Intelligence. Su disponibilidad puede depender del idioma, la región y la función concreta.</p>
<div class="takeaway"><strong>Presentado no significa disponible</strong><p>Para el iPhone Duo, Apple anuncia reservas desde el 16 de octubre y disponibilidad desde el 23 de octubre. Consulta el sitio de Apple de tu país antes de planear una compra.</p></div>
<h2>AirPods y Apple Watch también se renuevan</h2>
<p>Los AirPods 5 incorporan cancelación activa de ruido en un diseño abierto. En relojes, Apple anunció el Series 12 con un nuevo sistema de sensores de salud y el Ultra 4. Son lanzamientos distintos, con características y calendarios propios: no forman un único paquete con el teléfono.</p>
<h2 id="comparacion">Primera mirada: iPhone 18 Pro frente a iPhone Duo</h2>
<p><strong>Análisis de especificaciones anunciadas, sin pruebas de uso.</strong> La diferencia que define la elección es el formato. El Pro conserva una pantalla principal convencional; el Duo añade una pantalla interior que se despliega.</p>
<p>Desde una perspectiva de uso, el formato tradicional evita tener que abrir el dispositivo para acceder a su pantalla principal. El plegable propone más superficie cuando interesa leer o distribuir contenido. Esa ventaja debe valorarse junto al tamaño, el precio y la comodidad personal.</p>
<p>Bitora no ha probado estos equipos. No asignamos puntuaciones de batería, cámara o resistencia: una comparación de anuncios no sustituye una evaluación independiente.</p>''',
        'sources': [
            ('Apple: anuncio de iPhone 18 Pro y Pro Max', 'https://www.apple.com/uk/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/'),
            ('Apple: anuncio y disponibilidad de iPhone Duo', 'https://www.apple.com/uk/newsroom/2026/09/apple-unveils-iphone-duo/'),
            ('Apple: AirPods 5', 'https://www.apple.com/uk/newsroom/2026/09/apple-introduces-airpods-5-with-best-in-class-open-ear-active-noise-cancellation/'),
            ('Apple: Apple Watch Series 12', 'https://www.apple.com/uk/newsroom/2026/09/introducing-apple-watch-series-12-with-the-all-new-health-sensing-system/'),
            ('Apple: Apple Watch Ultra 4', 'https://www.apple.com/uk/newsroom/2026/09/apple-unveils-apple-watch-ultra-4/'),
        ],
    },
    {
        'slug': 'tesla', 'title': 'Tesla lleva el Cybercab a las calles de Austin, Estados Unidos',
        'summary': 'El vehículo diseñado para viajes autónomos inicia su despliegue comercial. Su llegada también abre preguntas sobre certificación y alcance del servicio.',
        'category': 'Innovación', 'tag': 'purple', 'date': '2026-09-04', 'date_label': '4 de septiembre de 2026', 'minutes': 3,
        'alt': 'Automóvil Tesla blanco en una carretera junto a montañas; no es un Cybercab',
        'caption': 'Fotografía ilustrativa de otro modelo Tesla; no muestra un Cybercab ni una operación de robotaxis. Imagen de Unsplash.',
        'body': '''<p>El lugar es Austin, Texas, en Estados Unidos. Según la documentación de la Administración Nacional de Seguridad del Tráfico en las Carreteras (NHTSA), Tesla comenzó el despliegue comercial de un pequeño número de Cybercab el 3 de septiembre de 2026.</p>
<h2>Cybercab y Robotaxi no son lo mismo</h2>
<p>Robotaxi es el servicio de viajes de Tesla. Cybercab es uno de los vehículos que lo integran. La página de soporte de la compañía identifica una flota con Model Y y Cybercab; no todos los viajes de Robotaxi se realizan en el nuevo vehículo.</p>
<p>La diferencia más llamativa del Cybercab es la ausencia de controles manuales convencionales permanentemente instalados, como volante y pedales. Su propuesta está centrada en transportar pasajeros mediante conducción automatizada.</p>
<h2>¿Dónde se puede usar?</h2>
<p>Tesla informa que Robotaxi opera en zonas limitadas de Austin, Dallas, Houston, Miami, Orlando y Tampa. Esa lista describe el servicio general; no confirma que el Cybercab esté disponible en cada una de esas ciudades.</p>
<p>La solicitud se hace en la aplicación Robotaxi, que muestra el área de cobertura, la estimación de tarifa y la espera. La asignación de un Model Y o un Cybercab depende de los vehículos disponibles y del número de pasajeros.</p>
<div class="takeaway"><strong>La clave está en el alcance</strong><p>El inicio en Austin no equivale a una disponibilidad nacional ni a un servicio anunciado para Colombia.</p></div>
<h2>La certificación está bajo revisión</h2>
<p>La NHTSA abrió la investigación AQ26002 para examinar el proceso y los datos técnicos en los que Tesla se apoyó al certificar el Cybercab. El documento menciona su diseño sin los controles habituales y el cumplimiento de las normas federales de seguridad aplicables.</p>
<p>Una investigación abierta no es una conclusión sobre su resultado. Para entender este lanzamiento conviene seguir tanto la evolución del servicio como los documentos del regulador.</p>''',
        'sources': [
            ('NHTSA: apertura de la investigación AQ26002, 3 de septiembre de 2026 (PDF)', 'https://static.nhtsa.gov/odi/inv/2026/INOA-AQ26002-17078.pdf'),
            ('Tesla: funcionamiento, flota y cobertura de Robotaxi', 'https://www.tesla.com/support/robotaxi'),
            ('electrive: inicio de los viajes del Cybercab', 'https://www.electrive.com/2026/09/04/tesla-debuts-cybercab-autonomous-rides/'),
        ],
    },
    {
        'slug': 'nvidia', 'title': 'NVIDIA lleva nuevas mejoras gráficas con IA a los videojuegos',
        'summary': 'Las novedades de DLSS conectan inteligencia artificial y gaming. PUBG está entre los juegos que reciben nuevas opciones gráficas esta semana.',
        'category': 'Gaming', 'tag': 'green', 'date': '2026-09-09', 'date_label': '9 de septiembre de 2026', 'minutes': 2,
        'alt': 'Persona jugando en un computador durante un evento de videojuegos',
        'caption': 'Fotografía ilustrativa de gaming en PC; no es una captura de PUBG ni una comparación de DLSS. Imagen de Unsplash.',
        'body': '''<p>NVIDIA anunció el 9 de septiembre nuevas incorporaciones a su catálogo de juegos con DLSS. La actualización incluye títulos como Honeycomb: The World Beyond, WARDOGS y PUBG: BATTLEGROUNDS, con funciones que varían según cada juego.</p>
<h2 id="pubg">Lo que llega a PUBG</h2>
<p>La compañía anunció soporte para DLSS Super Resolution en PUBG a partir del 10 de septiembre. Esta técnica busca mejorar el equilibrio entre calidad de imagen y rendimiento. Las opciones concretas dependen del hardware, los controladores y la versión del juego.</p>
<h2 id="dlss">DLSS, explicado sin complicaciones</h2>
<p>DLSS significa <em>Deep Learning Super Sampling</em>. Una de sus aplicaciones consiste en reconstruir una imagen de mayor resolución a partir de una base de menor resolución, utilizando un modelo de inteligencia artificial.</p>
<p>Imagina que un juego necesita dibujar muchos elementos en cada instante. Reducir parte del trabajo de renderizado y reconstruir después la imagen permite buscar un equilibrio distinto entre fluidez y detalle. El resultado no es idéntico en todos los equipos ni en todas las escenas.</p>
<h2>No todas las funciones son iguales</h2>
<p>El anuncio también menciona DLSS 5 y su renderizado neuronal guiado en 3D, además de tecnologías presentes en otros lanzamientos. Eso no significa que PUBG reciba todas ellas: su novedad anunciada es Super Resolution.</p>
<div class="takeaway"><strong>Antes de activar una mejora</strong><p>Comprueba la compatibilidad de tu tarjeta gráfica y del juego. Compara la calidad de imagen y la respuesta del control, además de los fotogramas por segundo.</p></div>
<p>La noticia importa porque muestra una aplicación de la IA que puede experimentarse al jugar. El criterio final sigue siendo la experiencia en tu propio computador, no una cifra aislada de una demostración.</p>''',
        'sources': [
            ('NVIDIA: novedades de DLSS, WARDOGS, Honeycomb y PUBG, 9 de septiembre de 2026', 'https://www.nvidia.com/en-eu/geforce/news/wardogs-pubg-battlegrounds-honeycomb-dlss/'),
        ],
    },
]

for article in articles:
    source_list = ''.join(f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{label} <span class="sr-only">(abre en otra pestaña)</span></a></li>' for label, url in article['sources'])
    related = ''.join(f'<a href="{other["slug"]}.html">{other["title"]} <span aria-hidden="true">↗</span></a>' for other in articles if other != article)
    content = f'''<div class="article-top"><a class="back-link" href="../index.html#noticias">← Volver a noticias</a></div>
<article><header class="article-heading"><span class="tag {article['tag']}">{article['category']}</span><h1>{article['title']}</h1><p>{article['summary']}</p><div class="meta"><span>Redacción Bitora</span><time datetime="{article['date']}">{article['date_label']}</time><span>{article['minutes']} min de lectura</span></div></header>
<figure class="article-figure"><img src="../assets/images/{('apple.png' if (ROOT / 'assets/images/apple.png').exists() else 'apple.jpg') if article['slug'] == 'apple' else article['slug'] + '.jpg' if article['slug'] != 'nvidia' else 'gaming.jpg'}" alt="{article['alt']}" width="1200" height="800"><figcaption>{article['caption']} <a href="../creditos.html">Ver créditos</a></figcaption></figure>
<div class="article-body">{article['body']}<section class="article-sources" aria-label="Fuentes del artículo"><h2>Fuentes para seguir explorando</h2><p>Información revisada el 10 de septiembre de 2026. Contenido editorial de Bitora basado en las fuentes enlazadas.</p><ul>{source_list}</ul></section></div></article>
<aside class="related"><h2>También en Bitora</h2>{related}<a class="text-link" href="../index.html#noticias">← Volver a noticias</a></aside>'''
    target = ROOT / 'noticias' / (article['slug'] + '.html')
    target.parent.mkdir(exist_ok=True)
    target.write_text(shell(article['title'], article['summary'], content, True), encoding='utf-8')
    print('Created', target.name)

sources = ''.join(f'<h2>{a["title"]}</h2><ul>' + ''.join(f'<li><a href="{url}">{label}</a></li>' for label, url in a['sources']) + '</ul>' for a in articles)
credits = f'''<div class="credits"><a class="back-link" href="index.html">← Volver al inicio</a><h1>Fuentes y créditos</h1><p>Bitora es un proyecto académico de noticias tecnológicas. Fecha de revisión editorial: 10 de septiembre de 2026. Los artículos son resúmenes propios; los anuncios y documentos originales se enlazan para consultar sus detalles.</p>
<h2>Identidad visual</h2><p>El logo SVG de Bitora es una adaptación vectorial del diseño aportado por el autor del proyecto: una B con píxeles y una órbita en cian, azul y violeta. Los teléfonos con perspectiva de la portada y los esquemas de Reviews son representaciones ilustrativas creadas con HTML y CSS; no son imágenes oficiales de los nuevos iPhone.</p>
<h2>Fotografías</h2><p>Las fotografías de Tesla y gaming se descargaron de Unsplash y se incluyen localmente bajo la <a href="https://unsplash.com/license">licencia de Unsplash</a>. Son imágenes ilustrativas: no representan los nuevos dispositivos, el Cybercab ni una prueba de rendimiento.</p><ul>
<li>Composición ilustrativa de iPhone: imagen local incorporada al proyecto. Archivo: assets/images/apple.png. Su fuente original no está documentada en los archivos del proyecto.</li>
<li>Vehículo Tesla en una carretera: <a href="https://images.unsplash.com/photo-1560958089-b8a1929cea89">fotografía original de Unsplash</a>. Archivo: assets/images/tesla.jpg.</li>
<li>Gaming en computador: <a href="https://images.unsplash.com/photo-1542751371-adc38448a05e">fotografía original de Unsplash</a>. Archivo: assets/images/gaming.jpg.</li></ul>
<h2>Tipografías</h2><p>Space Grotesk y Source Sans 3, distribuidas mediante Google Fonts bajo SIL Open Font License 1.1. Se incluyen localmente con sus licencias: <a href="assets/fonts/space-grotesk-LICENSE.txt">Space Grotesk</a> y <a href="assets/fonts/source-sans-3-LICENSE.txt">Source Sans 3</a>.</p>
<h2>Contacto de ejemplo</h2><p>contacto@bitora.example es un dato de demostración y no recibe mensajes. El sitio no envía formularios, no usa analítica y no requiere cuentas.</p>{sources}</div>'''
(ROOT / 'creditos.html').write_text(shell('Fuentes y créditos', 'Fuentes periodísticas, fotografías y licencias de Bitora.', credits), encoding='utf-8')
print('Created creditos.html')
