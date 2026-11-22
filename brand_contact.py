"""Public RolloBase brand and sales contact pages."""

from html import escape
import json
import re

from design_update import DISPLAY_PHONE, PHONE, replace_once


BRAND_DATE = '2026-11-22'
BRAND_FILES = ('empresa.html', 'about.html', 'about-zh.html', 'about-ru.html', 'about-zh-cn.html')
LANGUAGES = ('es-419', 'en', 'zh-Hant', 'ru', 'zh-Hans')

COPY = (
    {
        'title': 'Sobre RolloBase y contacto comercial',
        'navigation': 'Sobre RolloBase y contacto',
        'description': 'Conozca RolloBase, consulte opciones de material autoadhesivo en bobina y contacte al área comercial para coordinar muestras y cotizaciones.',
        'intro': 'RolloBase reúne información para elegir y probar material autoadhesivo sin imprimir. El catálogo y las guías ayudan a impresores, convertidores y distribuidores a comparar el frontal, el adhesivo y el liner de una bobina.',
        'contact': 'Contacto comercial',
        'call': 'Llamar al',
        'details': 'Indique el material, el uso de la etiqueta, las medidas de bobina y el país de destino. Descargue el resumen de su solicitud y llame para coordinar cómo compartirlo y confirmar las condiciones de la muestra o cotización.',
        'request': 'Preparar solicitud de muestra o cotización',
    },
    {
        'title': 'About RolloBase and sales contact',
        'navigation': 'About and contact',
        'description': 'Learn about RolloBase, compare self-adhesive labelstock in rolls and contact sales to discuss samples or a quote.',
        'intro': 'RolloBase provides information for choosing and testing unprinted self-adhesive labelstock. The catalogue and guides help printers, converters and distributors compare a roll’s facestock, adhesive and liner.',
        'contact': 'Sales contact',
        'call': 'Call',
        'details': 'Have your material, label application, roll dimensions and destination country ready. Download your request brief and call to arrange how to share it and confirm sample or quote details.',
        'request': 'Prepare a sample or quote request',
    },
    {
        'title': '關於 RolloBase 與業務聯絡',
        'navigation': '關於與聯絡',
        'description': '認識 RolloBase，查看自黏標籤母卷的選材與試樣資訊，透過業務電話確認索樣或報價需求。',
        'intro': 'RolloBase 提供未印刷自黏標籤卷材的選材與試樣資訊。印刷廠、加工廠及經銷商可透過材料目錄與技術指南，比較母卷的面材、膠黏劑與離型底材。',
        'contact': '業務聯絡',
        'call': '撥打',
        'details': '請準備材料、標籤用途、母卷尺寸與目的國。下載需求單後，可來電確認資料交付方式及索樣或報價條件。',
        'request': '準備索樣或詢價需求',
    },
    {
        'title': 'О RolloBase и контакты отдела продаж',
        'navigation': 'О RolloBase и контакты',
        'description': 'Узнайте о RolloBase, сравните самоклеящиеся материалы в рулонах и свяжитесь с отделом продаж по поводу образцов или цены.',
        'intro': 'RolloBase публикует информацию о выборе и испытании самоклеящихся материалов без печати. Каталог и руководство помогают типографиям, переработчикам и дистрибьюторам сравнивать лицевой материал, клей и подложку рулона.',
        'contact': 'Отдел продаж',
        'call': 'Позвонить по номеру',
        'details': 'Подготовьте данные о материале, применении этикетки, размерах рулона и стране назначения. Скачайте запрос и позвоните, чтобы согласовать способ передачи и уточнить условия получения образца или расчёта цены.',
        'request': 'Подготовить запрос образца или цены',
    },
    {
        'title': '关于 RolloBase 与业务联系',
        'navigation': '关于与联系',
        'description': '了解 RolloBase，查看不干胶标签母卷的选材和试样信息，通过业务电话确认索样或报价需求。',
        'intro': 'RolloBase 提供未印刷不干胶标签卷材的选材和试样信息。印刷厂、加工厂及经销商可通过材料目录和技术指南，对比母卷的面材、胶粘剂和离型底材。',
        'contact': '业务联系',
        'call': '拨打',
        'details': '请准备材料、标签用途、母卷尺寸和目的国家。下载需求单后，可致电确认资料交付方式及索样或报价条件。',
        'request': '准备索样或询价需求',
    },
)


def organization_node(origin):
    return {
        '@type': 'Organization', '@id': origin + '/#organization',
        'name': 'RolloBase', 'url': origin + '/', 'telephone': PHONE,
    }


def attach_organization(html, organization):
    def update_schema(match):
        schema = json.loads(match[1])
        graph = schema['@graph']
        site = next(node for node in graph if node['@type'] == 'WebSite')
        site['publisher'] = {'@id': organization['@id']}
        graph.append(organization)
        return '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>'

    return replace_once(r'<script type="application/ld\+json">(.*?)</script>', update_schema, html)


def add_brand_pages(dist, groups, origin):
    """Add the contact links and return the localized page names in site-language order."""
    origin = origin.rstrip('/')
    organization = organization_node(origin)
    for paths in groups.values():
        for index, filename in enumerate(paths):
            path = dist / filename
            html = path.read_text(encoding='utf-8')
            about = '/' + BRAND_FILES[index].removesuffix('.html')
            link = f'<a href="{about}">{escape(COPY[index]["navigation"])}</a>'
            html = replace_once(r'(<div class="footer-contact">.*?)</div>',
                                lambda match: match[1] + link + '</div>', html)
            if filename == groups['home'][index]:
                html = attach_organization(html, organization)
            path.write_text(html, encoding='utf-8')

    for index, filename in enumerate(BRAND_FILES):
        strings = COPY[index]
        path = dist / filename
        home = (dist / groups['home'][index]).read_text(encoding='utf-8')
        header = home.split('<body>', 1)[1].split('<main>', 1)[0]
        footer = home.split('</main>', 1)[1]
        stylesheet = re.search(r'<link rel="stylesheet"[^>]*>', home)[0]
        request = '/' + groups['request'][index].removesuffix('.html')
        url = origin + '/' + filename.removesuffix('.html')
        title = strings['title'] + ' | RolloBase'
        description = strings['description']
        website = {'@type': 'WebSite', '@id': origin + '/#website', 'name': 'RolloBase', 'url': origin + '/'}
        website['publisher'] = {'@id': organization['@id']}
        page = {
            '@type': 'WebPage', '@id': url + '#webpage', 'url': url,
            'name': title, 'description': description, 'inLanguage': LANGUAGES[index],
            'dateModified': BRAND_DATE, 'isPartOf': {'@id': website['@id']},
            'about': {'@id': organization['@id']},
        }
        schema = json.dumps({'@context': 'https://schema.org', '@graph': [website, page, organization]}, ensure_ascii=False)
        html = f"""<!doctype html><html lang="{LANGUAGES[index]}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description)}">
<link rel="canonical" href="{escape(url)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="RolloBase">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{escape(url)}">{stylesheet}
<script type="application/ld+json">{schema}</script></head><body>{header}<main>
<section><h1>{escape(strings['title'])}</h1><p>{escape(strings['intro'])}</p></section>
<section class="record-callout"><h2>{escape(strings['contact'])}</h2><p>{escape(strings['details'])}</p>
<div class="toc"><a href="tel:{PHONE}">{escape(strings['call'])} {DISPLAY_PHONE}</a>
<a href="{request}">{escape(strings['request'])}</a></div></section>
</main>{footer}"""
        path.write_text(html, encoding='utf-8')
    return list(BRAND_FILES)
