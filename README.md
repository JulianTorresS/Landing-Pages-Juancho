# Bitora

Portal académico de noticias tecnológicas en español. HTML, CSS y JavaScript sin frameworks ni servidor. Diseño inspirado en las referencias visuales aportadas: cabecera azul marino, portada con vistas móviles, áreas de lectura blancas y bloques alternados de fotografía y texto.

## Abrir

Haz doble clic en **index.html**. También puedes abrirlo con Chrome, Edge o Firefox. El sitio, las tres noticias, las fotografías y las fuentes funcionan sin conexión; los enlaces a fuentes externas requieren internet.

## Contenido

- Inicio, Noticias, Reviews, IA, Gaming, Sobre Bitora y Contacto.
- Tres noticias con fechas y fuentes, revisadas el 10 de septiembre de 2026.
- Búsqueda sin distinción de mayúsculas o tildes y filtros combinables con la búsqueda.
- Menú móvil, enlaces a artículos completos y adaptación a pantallas pequeñas.
- Logo SVG inspirado en la referencia proporcionada; dos fotografías ilustrativas de Unsplash y la composición local de iPhone, con créditos separados.
- Portada flotante, teléfonos con perspectiva CSS y respuesta al cursor; movimiento desactivado en pantallas táctiles y con movimiento reducido.
- El botón «Borrar búsqueda» conserva la categoría seleccionada; «Limpiar búsqueda» restablece tanto texto como filtros.
- Correo académico de ejemplo: `contacto@bitora.example`. No se simulan envíos.

## Editar

- **Textos y noticias de portada:** edita `index.html`. Cada tarjeta contiene `data-categories` y `data-keywords` para sus filtros y búsqueda. Mantén también actualizados los destacados.
- **Artículos y créditos:** edita el contenido en `tools/build_articles.py` y ejecuta `python tools/build_articles.py`. Este paso es únicamente para edición, no para abrir la web. El generador reutiliza el encabezado y pie de `index.html`.
- **Colores y diseño:** `assets/styles.css` contiene la estructura base; `assets/theme.css` define el diseño actual y se carga después. Ajusta colores, portada y secciones en `theme.css`.
- **Comportamiento:** `assets/app.js`.
- **Fotografías:** reemplaza las imágenes en `assets/images/`; revisa textos alternativos, etiquetas de imagen ilustrativa y créditos si cambian.
- **Contacto:** reemplaza el correo y la nota de ejemplo en la portada y en el generador de créditos. Si usas un correo real, puedes añadir un enlace `mailto:`.
- **Fecha de edición:** actualiza la fecha visible y las fechas editoriales cuando publiques nuevas noticias. No hay actualización automática ni contenido en vivo.

Los archivos HTML generados también se pueden editar directamente, pero volver a ejecutar el generador sobrescribirá esos cambios.

## Recursos y licencias

Ver `creditos.html` para las fuentes originales y créditos. Las fuentes locales incluyen sus licencias SIL OFL. Las fotografías de Tesla y gaming utilizan la licencia de Unsplash. La composición de Apple es el archivo local `apple.png` incorporado al proyecto. Las imágenes y los teléfonos dibujados en CSS son ilustrativos, no fotografías oficiales de los dispositivos recién anunciados.

## Sistema visual

`assets/theme.css` agrupa el marco y los componentes, seguidos de las adaptaciones para tableta, móvil, movimiento reducido e impresión. Variables compartidas:

| Variable | Uso |
| --- | --- |
| `--radius-page` | Esquinas del marco: 36 px en escritorio y 24 px en móvil. |
| `--radius-control` | Radio de los botones: 14 px. |
| `--shadow-soft` | Elevación tenue de buscador, tarjetas y paneles de identidad. |
| `--shadow-control` | Sombra de botones principales. |
| `--shadow-panel` | Profundidad de los bloques de fotografía y texto. |
| `--shadow-page` | Sombra del contenedor sobre el fondo lavanda. |
| `--motion` | Transiciones de interacción: 180 ms. |

Los filtros conservan `aria-pressed`, el buscador tiene una etiqueta asociada y los controles presentan foco visible. Los botones se elevan 2 px al pasar el cursor, vuelven a su posición al pulsar y respetan movimiento reducido. La inclinación de la portada se limita a ±4 grados y se restablece al retirar el cursor. El encabezado conserva las esquinas redondeadas del marco al tope de la página y se vuelve rectangular en cuanto comienza el desplazamiento. La capa decorativa se recorta por separado para permitir que los celulares sobresalgan sin cubrir la sección siguiente.

`tools/download_assets.py` conserva las URLs de los recursos. Es una utilidad opcional para recuperar recursos faltantes, requiere internet y omite archivos ya descargados.

## Entrega

Comparte la carpeta completa, conservando `assets/` y `noticias/` junto a `index.html`. No necesitas instalar dependencias. No incluye alojamiento, base de datos, administrador ni cuentas.

## Verificación realizada

Probado en Chrome con Playwright a 360, 768 y 1440 píxeles: cinco páginas en cada tamaño, sin desbordamiento horizontal, enlaces locales válidos, imágenes y fuentes cargadas. Búsqueda, filtros, estado sin resultados, menú móvil, tecla Escape y navegación entre artículos comprobados. Cero errores de JavaScript y cero solicitudes de recursos a internet.

La comprobación automatizada con axe-core no detectó infracciones WCAG 2 A/AA o 2.1 AA en las páginas revisadas. Esto complementa la revisión visual; no constituye una certificación de accesibilidad.

Para repetir las pruebas como desarrollador: `npm.cmd install --prefix .validation --no-audit --no-fund --ignore-scripts playwright @axe-core/playwright` y `node tools/validate.cjs`. El script usa Chrome instalado en su ubicación habitual de Windows. Los resultados y capturas quedan en `.validation/results/`. Estas herramientas no forman parte de la web ni se requieren para usarla.
