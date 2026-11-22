"""Spanish buying guidance for the catalog and priority product pages."""
from html import escape

from cold_bopp import GUIDE_SLUG
from design_update import replace_once


GUIDE_LINK = f'<a href="/{GUIDE_SLUG}">Consultar la guía de BOPP para botellas refrigeradas →</a>'

SPECS = {
    'bopp': {
        1: (
            'Indique BOPP blanco o transparente y el acabado requerido. Pida el espesor nominal en μm, '
            'su tolerancia y el tratamiento de la cara de impresión para la tinta prevista.'
        ),
        2: (
            'Indique el material del envase, si se etiqueta seco o con condensación y las temperaturas '
            'de aplicación y servicio. Confirme el tipo de adhesivo, la temperatura mínima de aplicación '
            'y el gramaje del recubrimiento cuando esté especificado.'
        ),
        3: (
            'Confirme si la referencia lleva glassine o liner PET, y pida su gramaje o espesor y su fuerza '
            'de desprendimiento con el método de ensayo. Compruebe troquelado y detección con el sensor de la línea.'
        ),
        5: (
            'Solicite la ficha técnica (TDS) vigente de la combinación de frontal, adhesivo y liner. '
            'Identifique el lote de prueba y registre cobertura o claridad, adherencia de la tinta y comportamiento '
            'en el envase con el llenado y la temperatura previstos.'
        ),
    },
    'coated': {
        1: (
            'Pida el gramaje del frontal en g/m², su tolerancia y el acabado semibrillo (semigloss). '
            'Indique si el diseño lleva texto fino, áreas de color sólido o datos variables añadidos después.'
        ),
        2: (
            'Indique la superficie real, por ejemplo cartón o un frasco rígido, y las condiciones de aplicación y uso. '
            'Confirme el tipo de adhesivo y, si está especificado, el gramaje del recubrimiento.'
        ),
        3: (
            'Confirme el tipo de liner, su gramaje o espesor y la fuerza de desprendimiento con el método de ensayo. '
            'Pruebe el troquelado y el retiro de la matriz en la línea que usará en producción.'
        ),
        5: (
            'Solicite la ficha técnica (TDS) vigente para la referencia completa. Registre lote, '
            'equipo, tinta y acabado final, y acuerde cómo evaluar definición, uniformidad y lectura del código.'
        ),
    },
}

FIRST_SAMPLE = {
    'bopp': (
        'Pida BOPP blanco si necesita un fondo uniforme para los colores. Pida transparente si el diseño deja ver '
        'el envase. Si la decisión depende del aspecto final, compare ambos sobre botellas iguales y bajo '
        'la misma luz. Identifique la combinación exacta de frontal, adhesivo y liner de cada muestra.'
    ),
    'coated': (
        'Empiece por una muestra de semigloss con el adhesivo propuesto para el envase real. Indique tinta, '
        'equipo y acabado al solicitarla. Si el diseño lleva códigos o datos variables, haga la prueba con '
        'la impresión y la sobreimpresión previstas antes de aprobar la referencia.'
    ),
}


def apply_buyer_content(dist, groups):
    """Update the existing Spanish pages and return the changed filenames."""
    changed = set()

    for key, anchor, callout in (
        (
            'home',
            r'(<section id="materials">.*?</section>)',
            '<section class="record-callout"><h2>BOPP para botellas refrigeradas</h2>'
            '<p>Compare película blanca y transparente y pruebe el adhesivo si hay condensación al etiquetar.</p>'
            + GUIDE_LINK + '</section>',
        ),
        (
            'catalog',
            r'(<p\b[^>]*\bid="no-results"[^>]*>[^<]*</p></section>)',
            '<section class="record-callout"><h2>Selección de BOPP para bebidas refrigeradas</h2>'
            '<p>Revise el aspecto del frontal sobre la botella, las condiciones de pegado y los resultados en frío.</p>'
            + GUIDE_LINK + '</section>',
        ),
    ):
        path = dist / groups[key][0]
        html = replace_once(anchor, lambda match: match[1] + callout, path.read_text(encoding='utf-8'))
        if key == 'catalog':
            html = replace_once(
                r'(<h1>[^<]*</h1><p>[^<]*</p>)',
                lambda match: match[1] + (
                    '<p>Si su orden de compra indica rollo jumbo autoadherible, confirme que se trate de material '
                    'sin imprimir ni troquelar. Indique el ancho útil y el metraje de la bobina.</p>'
                ),
                html,
            )
        path.write_text(html, encoding='utf-8')
        changed.add(path.name)

    for key, rows in SPECS.items():
        path = dist / groups[key][0]
        html = path.read_text(encoding='utf-8')
        for number, value in rows.items():
            html = replace_once(
                rf'(<dt><span class="spec-number">{number}</span>[^<]*</dt>)<dd>[^<]*</dd>',
                lambda match: match[1] + '<dd>' + escape(value) + '</dd>',
                html,
            )
        html = replace_once(
            r'(<section class="product-specs"><h2>[^<]*</h2><dl class="spec-table">.*?</dl>)',
            lambda match: match[1] + '<p><strong>Primera muestra.</strong> ' + escape(FIRST_SAMPLE[key]) + '</p>',
            html,
        )
        path.write_text(html, encoding='utf-8')
        changed.add(path.name)

    path = dist / groups['woodfree'][0]
    woodfree = replace_once(
        r'(<aside><h3>¿14 o 20 g/m² de adhesivo\?</h3><p>[^<]*</p>)(</aside>)',
        lambda match: match[1] + (
            '<p><strong>Primera muestra.</strong> Elija el par A y B si su referencia parte de un frontal de 60 g/m², '
            'o C y D si parte de 70 g/m². Si quiere comparar las dos construcciones con el mismo gramaje de adhesivo, '
            'pruebe A con C o B con D y confirme que la formulación coincida. Registre por separado impresión, '
            'troquelado y desprendimiento. Entre esos pares cambian tanto el frontal como el glassine.</p>'
        ) + match[2],
        path.read_text(encoding='utf-8'),
    )
    path.write_text(woodfree, encoding='utf-8')
    changed.add(path.name)
    return changed
