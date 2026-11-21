"""Spanish selection and trial guide for refrigerated beverage labels."""
from csv import writer
from html import escape
import json

from design_update import replace_once
from knowledge import structured_data


GUIDE_SLUG = 'guia-bopp-botellas-refrigeradas'
GUIDE_FILE = GUIDE_SLUG + '.html'
GUIDE_DATE = '2026-11-21'
RECORD = 'registro-prueba-bopp-refrigeracion.csv'
TITLE = 'BOPP blanco o transparente para botellas refrigeradas'
DESCRIPTION = ('Compare BOPP blanco y transparente para etiquetas de bebidas refrigeradas. '
               'Pruebe el adhesivo en su botella y descargue una ficha para registrar los resultados.')
SAMPLE = '/cotizacion-muestras?material=bopp&amp;mode=sample'
SOURCE = ('https://label.averydennison.com/content/dam/averydennison/lpm-responsive/na/doc/'
          'technical-bulletins/product/sustainable-solutions/to-ad-cleanflake-pet.pdf')

BODY = f"""
<p class="crumb"><a href="/">Inicio</a> / <a href="/pelicula-bopp">BOPP autoadhesivo</a> / Botellas refrigeradas</p>
<section class="buy-head"><div>
  <h1>{TITLE}</h1>
  <p>Pruebe BOPP blanco si necesita cubrir el color del envase y mantener legibles los textos. Pruebe BOPP transparente si quiere que se vean la botella o la bebida. En ambos casos, valide la combinación de frontal, adhesivo y liner sobre su botella y en la línea de etiquetado.</p>
</div><div><a class="buy-link" href="{SAMPLE}">Preparar una solicitud de muestra BOPP →</a></div></section>
<div class="toc"><a href="#comparar">Comparar frontales</a><a href="#prueba">Probar en su botella</a><a href="#registro">Descargar ficha</a></div>

<section id="comparar" class="product-specs">
  <h2>Qué construcción probar primero</h2>
  <table class="trial-comparison">
    <caption>Opciones de BOPP según el resultado visual y el proceso de etiquetado</caption>
    <thead><tr><th scope="col">Opción</th><th scope="col">Cuándo probarla</th><th scope="col">Qué comprobar</th></tr></thead>
    <tbody>
      <tr><th scope="row">BOPP blanco</th><td>Botella oscura, bebida de color intenso o diseño que necesita un fondo uniforme.</td><td>Cobertura, contraste, fidelidad de color y lectura del código.</td></tr>
      <tr><th scope="row">BOPP transparente</th><td>Botella o bebida visible a través de la etiqueta.</td><td>Claridad, burbujas, zonas lechosas y detección de la etiqueta en la línea.</td></tr>
      <tr><th scope="row">BOPP transparente con blanco de fondo</th><td>Ventana transparente con textos o gráficos que necesitan contraste.</td><td>Registro y cobertura de la tinta blanca, transparencia de la ventana y lectura del código.</td></tr>
    </tbody>
  </table>
  <p>Confirme en la ficha técnica la temperatura mínima de aplicación y el rango de servicio de la referencia candidata. Distinga entre etiquetar una botella seca antes de refrigerarla y etiquetar una botella ya fría con condensación. Si el segundo escenario forma parte de su línea, solicite una referencia para esa condición y pruébela por separado.</p>
</section>

<section id="prueba" class="trial-steps">
  <h2>Prueba comparativa en la botella real</h2>
  <ol>
    <li><strong>Prepare muestras comparables.</strong> Use botellas iguales del material, forma y acabado de producción. Registre el código y lote de cada muestra, con la referencia de frontal, adhesivo y liner, el diseño de impresión y el ajuste del sensor.</li>
    <li><strong>Etiquete un grupo de control seco.</strong> Anote la temperatura de la botella al aplicar, si se etiquetó antes o después del llenado y el tiempo previsto entre el etiquetado y el ingreso a refrigeración. Si la línea etiqueta botellas frías con condensación, prepare otro grupo con esa condición real y mantenga separados los resultados.</li>
    <li><strong>Reproduzca la cadena de frío.</strong> Registre temperatura y duración en frío. Revise cada botella al aplicar, al sacarla de refrigeración y tras el secado exterior. Si el uso incluye agua, hielo o ciclos de frío, incorpórelos al ensayo y anote la exposición.</li>
    <li><strong>Registre defectos y compruebe la línea.</strong> Fotografíe cada muestra desde el mismo ángulo e iluminación. Revise legibilidad, levantamiento de bordes, deslizamiento, arrugas y aspecto óptico. En transparente, retire con cuidado las gotas exteriores para observar si quedan burbujas o áreas lechosas bajo la película. Registre el defecto observado y, si aparece, confirme su origen con un ensayo adicional. En la línea, compruebe el sensor, el troquelado y la dispensación antes de aprobar.</li>
    <li><strong>Decida con criterios acordados.</strong> Defina antes del ensayo qué defectos se aceptan, cuándo inspeccionar y cuántas botellas revisar por condición. Apruebe la combinación que cumpla esos criterios y vincule su código de muestra con la referencia de producción.</li>
  </ol>
  <p class="refs">Referencia sobre condiciones de aplicación en PET · <a href="{SOURCE}">Guía de aplicación AD CleanFlake para envases PET</a></p>
</section>

<section id="registro" class="record-callout">
  <h2>Ficha para registrar la prueba de frío</h2>
  <p>Use una fila por botella y momento de inspección. Adjunte fotos y acuerde los criterios de aceptación con su equipo antes de comparar las muestras.</p>
  <div class="toc">
    <a href="/{RECORD}" download>Descargar ficha de prueba (.csv) ↓</a>
    <a href="/calidad-trazabilidad">Ver TDS, COA y trazabilidad →</a>
  </div>
  <p>Para pedir una muestra, indique si necesita BOPP blanco o transparente, el material y la forma de la botella, el estado de la superficie al etiquetar, las temperaturas de aplicación y servicio y las medidas de su bobina. Si necesita comparar ambas opciones, anótelo en la solicitud.</p>
  <a class="button" href="{SAMPLE}">Preparar solicitud de muestra BOPP →</a>
  <p><a href="/pelicula-bopp">Volver a la ficha de BOPP autoadhesivo →</a></p>
</section>
<p class="updated">Contenido revisado · <time datetime="{GUIDE_DATE}">{GUIDE_DATE}</time></p>
"""


def add_cold_bopp_guide(dist, spanish_bopp, spanish_technical_guide, origin):
    """Reuse the Spanish product page's header, footer and language navigation."""
    bopp = dist / spanish_bopp
    technical_guide = dist / spanish_technical_guide
    source_html = bopp.read_text(encoding='utf-8')
    header = source_html.split('<body>', 1)[1].split('<main>', 1)[0]
    footer = source_html.split('</main>', 1)[1]
    header = replace_once(
        r'<div class="languages">',
        '<div class="languages" role="group" aria-label="Ficha de BOPP por idioma"><span>BOPP</span>',
        header,
    ).replace(' aria-current="page"', '', 1)
    url = f'{origin}/{GUIDE_SLUG}'
    title = f'{TITLE} | RolloBase'
    data = json.loads(structured_data('cold-bopp', 0, title, DESCRIPTION, url, origin, origin + '/', BODY))
    page = data['@graph'][1]
    page['dateModified'] = GUIDE_DATE
    data['@graph'][0]['inLanguage'] = ['es', 'en', 'zh-Hant', 'ru', 'zh-Hans']
    breadcrumb = data['@graph'][2]['itemListElement']
    breadcrumb[-1]['position'] = 3
    breadcrumb.insert(
        1, {'@type': 'ListItem', 'position': 2, 'name': 'BOPP autoadhesivo', 'item': origin + '/pelicula-bopp'},
    )
    data['@graph'].append({
        '@type': 'Article', '@id': url + '#article', 'headline': TITLE,
        'description': DESCRIPTION, 'inLanguage': 'es-419',
        'datePublished': GUIDE_DATE, 'dateModified': GUIDE_DATE,
        'author': {'@type': 'Organization', 'name': 'RolloBase', 'url': origin + '/'},
        'mainEntityOfPage': {'@id': url + '#webpage'},
    })
    schema = json.dumps(data, ensure_ascii=False)
    head = f"""<!doctype html><html lang="es-419"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(DESCRIPTION)}">
<link rel="canonical" href="{escape(url)}">
<meta property="og:type" content="article"><meta property="og:site_name" content="RolloBase">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(DESCRIPTION)}">
<meta property="og:url" content="{escape(url)}">
<link rel="stylesheet" href="/style.css?v=20261119-five">
<script type="application/ld+json">{schema}</script></head><body>"""
    (dist / GUIDE_FILE).write_text(head + header + '<main>' + BODY + '</main>' + footer, encoding='utf-8')

    with (dist / RECORD).open('w', encoding='utf-8-sig', newline='') as handle:
        writer(handle).writerow([
            'Fecha', 'ID de botella', 'Material y acabado de la botella', 'Referencia y lote de la muestra',
            'Frontal', 'Adhesivo', 'Liner', 'Diseño o blanco de fondo', 'Condición de superficie al aplicar',
            'Temperatura de botella al aplicar (°C)', 'Tiempo entre aplicación y refrigeración',
            'Temperatura de refrigeración (°C)', 'Tiempo en refrigeración', 'Exposición adicional',
            'Momento de inspección', 'Claridad y burbujas', 'Levantamiento y arrugas', 'Contraste y lectura del código',
            'Sensor, troquelado y dispensación', 'Foto o archivo', 'Criterio de aceptación', 'Resultado', 'Observaciones',
        ])

    callout = (
        '<section class="record-callout"><h2>Etiquetas para botellas refrigeradas</h2>'
        '<p>Compare BOPP blanco y transparente y registre el resultado del ensayo en su envase real.</p>'
        f'<a href="/{GUIDE_SLUG}">Ver la guía de selección y prueba en frío →</a></section>'
    )
    bopp.write_text(replace_once(r'<section class="product-specs">', callout + '<section class="product-specs">', source_html),
                    encoding='utf-8')
    guide_html = technical_guide.read_text(encoding='utf-8')
    technical_guide.write_text(replace_once(r'<section id="faq" class="questions">',
                                            callout + '<section id="faq" class="questions">', guide_html),
                               encoding='utf-8')
