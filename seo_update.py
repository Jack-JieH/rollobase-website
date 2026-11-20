"""Publish reviewed buyer guidance and independent Chinese language versions."""
from html import escape, unescape
import json
from pathlib import Path
import re
from design_update import apply_design, replace_once
from knowledge import VisibleFAQ, UPDATED
from localization import LocalizedPage
from russian import RU_ROUTES

ROOT = Path(__file__).parent
LANGUAGES = ['es', 'en', 'zh-Hant', 'ru', 'zh-Hans']
LABELS = ['ES', 'EN', '繁中', 'RU', '简中']
FULL_LABELS = ['Español', 'English', '繁體中文', 'Русский', '简体中文']
SC_ROUTES = {k:('zh-cn.html' if k=='home' else k+'-zh-cn.html') for k in RU_ROUTES}
CONTENT = json.loads((ROOT/'seo-content.json').read_text())

SPANISH_SEARCH = {
    'catalog': {
        'title': 'Catálogo de material autoadhesivo en bobina madre',
        'description': 'Compare papel y película autoadhesiva en bobinas jumbo sin imprimir para fabricar etiquetas. Elija material, adhesivo y liner antes de solicitar una muestra.',
        'heading': 'Catálogo de material autoadhesivo en bobina madre',
        'lead': 'Compare papeles y películas en bobinas jumbo sin imprimir para fabricar etiquetas. Elija el material según la aplicación y confirme el frontal, el adhesivo y el soporte de liberación (liner) antes de pedir una muestra.',
    },
    'bopp': {
        'title': 'BOPP autoadhesivo blanco y transparente en bobina jumbo',
        'description': 'Elija BOPP autoadhesivo blanco o transparente en bobina jumbo. Compare cobertura, claridad, tinta y adhesivo con una muestra en el envase real.',
        'heading': 'BOPP autoadhesivo en bobina jumbo',
        'lead': 'Película de polipropileno biorientado (BOPP) sin imprimir para fabricar etiquetas de envases. Compare el BOPP blanco y el transparente sobre el envase real y confirme el espesor, el adhesivo y el liner por referencia.',
    },
    'coated': {
        'title': 'Papel semibrillante autoadhesivo en bobina jumbo',
        'description': 'Papel semibrillo (semigloss) autoadhesivo en bobina jumbo para etiquetas a color. Confirme gramaje, adhesivo, soporte y prueba de impresión.',
        'heading': 'Papel semibrillante autoadhesivo en bobina jumbo',
        'lead': 'Papel estucado semibrillo (semigloss) sin imprimir para etiquetas a color en cajas y frascos. Si el proveedor usa el término couché, confirme el acabado y la ficha técnica de la referencia antes de comparar muestras.',
    },
    'woodfree': {
        'title': 'Papel autoadhesivo sin estucar en bobina madre: A–D',
        'description': 'Compare las opciones A–D de papel autoadhesivo sin estucar en bobina madre: frontal, adhesivo hot melt y glassine. Elija una opción para pedir una muestra.',
        'heading': 'Papel autoadhesivo sin estucar en bobina madre',
        'lead': 'Compare las opciones A–D para fabricar etiquetas de papel sin estucar. Revise el gramaje del frontal, el adhesivo hot melt y el soporte glassine, y elija una combinación para preparar su solicitud de muestra.',
    },
}


def traditional(text):
    for old, new in [('不乾膠','自黏'),('平方米','平方公尺'),('半光澤銅版紙','半光銅版紙')]:
        text = text.replace(old,new)
    return text


def update_schema(html, language, title, description):
    faq = VisibleFAQ()
    faq.feed(html.split('<main>',1)[1].split('</main>',1)[0])
    def replace(match):
        data = json.loads(match[1])
        graph = data['@graph']
        original = [(q['name'], q['acceptedAnswer']['text']) for n in graph if n['@type']=='FAQPage' for q in n['mainEntity']]
        pairs = list(dict.fromkeys(original+faq.pairs))
        page = next(n for n in graph if n['@type']=='WebPage')
        page.update(name=title, description=description, inLanguage=language, dateModified=UPDATED)
        for node in graph:
            if node['@type']=='WebSite':
                node['inLanguage'] = LANGUAGES
            if node['@type']=='BreadcrumbList':
                node['itemListElement'][-1]['name'] = title.removesuffix(' | RolloBase')
        graph[:] = [n for n in graph if n['@type']!='FAQPage']
        if pairs:
            faq_id = page['url']+'#questions'
            graph.append({'@type':'FAQPage','@id':faq_id,'inLanguage':language,'mainEntity':[
                {'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in pairs]})
            page['hasPart'] = {'@id':faq_id}
        return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>',replace,html,flags=re.S)


def apply_editorial(dist, groups, origin):
    for key, paths in groups.items():
        for i, path in enumerate(paths):
            html = (dist/path).read_text()
            if i==2:
                parser = LocalizedPage(traditional, {}, origin, 'zh-Hant')
                parser.feed(html)
                html = ''.join(parser.out)
            spanish_search = SPANISH_SEARCH.get(key) if i == 0 else None
            title = (spanish_search['title'] if spanish_search else CONTENT['titles'][key][i])+' | RolloBase'
            description = spanish_search['description'] if spanish_search else CONTENT.get('descriptions',{}).get(key,[None]*4)[i]
            if not description:
                description = unescape(re.search(r'<meta name="description" content="([^"]*)"',html)[1])
            html = re.sub(r'<title>.*?</title>',lambda m:'<title>'+escape(title)+'</title>',html)
            for selector,value in [('name="description"',description),('property="og:title"',title),('property="og:description"',description)]:
                html = re.sub(r'<meta '+selector+r' content="[^"]*">',lambda m,s=selector,v=value:'<meta '+s+' content="'+escape(v,quote=True)+'">',html)
            if key=='home':
                html = re.sub(r'<h1>.*?</h1>',lambda m:'<h1>'+escape(CONTENT['headings'][i])+'</h1>',html,count=1)
            rows = [row for row in CONTENT['questions'] if row['page']==key]
            if rows:
                section = '<section class="questions procurement-questions" id="procurement"><h2>'+escape(CONTENT['section'][i])+'</h2><div>'
                for row in rows:
                    section += '<details><summary>'+escape(row['q'][i])+'</summary><p>'+escape(row['a'][i])+'</p></details>'
                section += '</div></section>'
                html = html.replace('<p class="updated">',section+'<p class="updated">',1)
            if key in ('guide','quality','printing'):
                note = '<p class="technical-reference"><a href="https://www.finat.com/documents/540/technical-handbook-2019-folder-low.pdf">FINAT · '+escape(CONTENT['methods'][i])+'</a></p>'
                html = html.replace('<p class="updated">',note+'<p class="updated">',1)
            html = html.replace('style.css?v=20261116-ru','style.css?v=20261119-five')
            html = update_schema(html,LANGUAGES[i],title,description)
            (dist/path).write_text(html)


def apply_spanish_search(dist, groups):
    for key, copy in SPANISH_SEARCH.items():
        path = dist / groups[key][0]
        html = path.read_text()
        lead = '<h1>'+escape(copy['heading'])+'</h1><p>'+escape(copy['lead'])+'</p>'
        html = replace_once(r'<h1>[^<]*</h1><p>[^<]*</p>', lead, html)
        if key == 'catalog':
            for product, label, search_term in [
                ('bopp', 'BOPP autoadhesivo blanco y transparente', 'autoadhesivo'),
                ('coated', 'Papel autoadhesivo semibrillo', 'semigloss'),
                ('woodfree', 'Papel sin estucar · Opciones A–D', 'autoadhesivo'),
            ]:
                target = groups[product][0]
                href = target+'#compare' if product == 'woodfree' else target
                pattern = r'(<a class="appcard" data-search="[^"]*)" href="'+re.escape(target)+r'">(<span>[^<]*</span>)<h3>[^<]*</h3>'
                html = replace_once(pattern, lambda m: m[1]+' '+search_term+'" href="'+href+'">'+m[2]+'<h3>'+label+'</h3>', html)
        elif key in ('bopp', 'coated'):
            trial = {
                'bopp': (
                    '<p><strong>BOPP blanco:</strong> compruebe la cobertura y el contraste sobre el envase lleno. '
                    'Revise la legibilidad del diseño después de exponer la muestra a la condensación prevista.</p>'
                    '<p><strong>BOPP transparente:</strong> compruebe la claridad del conjunto, las burbujas y el blanqueamiento '
                    'del adhesivo antes y después de la exposición. Si el diseño lleva tinta blanca de fondo, evalúe '
                    'el contraste con la tinta prevista. En ambas opciones, verifique la adherencia de la tinta.</p>'
                ),
                'coated': (
                    '<p>Imprima en el equipo previsto una muestra con texto fino, un área de color sólido y el código de barras '
                    'si forma parte del diseño. Tras el secado o curado, revise definición, uniformidad, legibilidad y transferencia '
                    'de tinta por roce. Repita la revisión tras la exposición a la humedad de uso y pruebe el troquelado con el liner '
                    'de la referencia propuesta.</p>'
                ),
            }[key]
            html = replace_once(r'(<section class="questions"><h2>Prueba recomendada para esta aplicación</h2><div>)<p>[^<]*</p>',
                                lambda m: m[1]+trial, html)
        elif key == 'woodfree':
            test_note = (
                '<p>Compare A con B o C con D si desea estudiar el cambio de 14 a 20 g/m². Confirme que la formulación '
                'del adhesivo sea la misma dentro de cada par. Use el mismo envase, presión, temperatura y tiempo de reposo. '
                'Registre el levantamiento en bordes y el resultado de pelado para cada muestra. Entre A y C también cambian '
                'el frontal y el glassine. El gramaje del adhesivo por sí solo no determina la adhesión al pelado.</p>'
            )
            html = replace_once(r'(<aside><h3>¿14 o 20 g/m² de adhesivo\?</h3>)<p>[^<]*</p>',
                                lambda m: m[1]+test_note, html)
        path.write_text(html)


def add_simplified(dist, groups, origin):
    copy = json.loads((ROOT/'simplified.json').read_text())
    def translate(text):
        if not re.search(r'[\u3400-\u9fff]',text):
            return text
        if text not in copy:
            raise ValueError('Missing reviewed Simplified Chinese copy: '+repr(text))
        return copy[text]
    mapping = {paths[2]:SC_ROUTES[key] for key,paths in groups.items()}
    mapping['brief-zh-Hant.txt'] = 'brief-zh-Hans.txt'
    for key,paths in groups.items():
        parser = LocalizedPage(translate,mapping,origin,'zh-Hans')
        parser.feed((dist/paths[2]).read_text())
        (dist/SC_ROUTES[key]).write_text(''.join(parser.out))
    brief = traditional((dist/'brief-zh-Hant.txt').read_text(encoding='utf-8-sig'))
    (dist/'brief-zh-Hant.txt').write_text(brief,encoding='utf-8-sig')
    (dist/'brief-zh-Hans.txt').write_text(translate(brief),encoding='utf-8-sig')


def finalize_languages(dist, groups, origin):
    def url(path):
        return origin+('/' if path=='index.html' else '/'+path.removesuffix('.html'))
    all_paths = []
    for paths in groups.values():
        for i,path in enumerate(paths):
            html = (dist/path).read_text()
            html = re.sub(r'<link rel="alternate"[^>]*>','',html)
            alternate = ''.join('<link rel="alternate" hreflang="'+lang+'" href="'+url(p)+'">' for lang,p in zip(LANGUAGES+['x-default'],paths+[paths[0]]))
            html = html.replace('</head>',alternate+'</head>')
            nav = '<div class="languages">'+''.join('<a href="'+p+'" lang="'+lang+'" hreflang="'+lang+'" aria-label="'+full+'"'+(' aria-current="page"' if j==i else '')+'>'+label+'</a>' for j,(p,lang,label,full) in enumerate(zip(paths,LANGUAGES,LABELS,FULL_LABELS)))+'</div>'
            html = re.sub(r'<div class="languages">.*?</div>',lambda m:nav,html,count=1)
            (dist/path).write_text(html)
            all_paths.append(path)
    entries = ''.join('<url><loc>'+url(p)+'</loc><lastmod>'+UPDATED+'</lastmod></url>' for p in all_paths)
    (dist/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+entries+'</urlset>')
    return all_paths


def publish_update(dist, original_groups, origin):
    groups = {key:paths+[RU_ROUTES[key]] for key,paths in original_groups.items()}
    apply_editorial(dist,groups,origin)
    add_simplified(dist,groups,origin)
    complete_groups = {key:paths+[SC_ROUTES[key]] for key,paths in groups.items()}
    apply_design(dist,complete_groups)
    apply_spanish_search(dist,complete_groups)
    return finalize_languages(dist,complete_groups,origin)
