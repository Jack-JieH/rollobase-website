"""Turn the existing product catalog into a searchable five-language finder."""

from html import escape, unescape
from pathlib import Path
import re
from shutil import copyfile

from cold_bopp import GUIDE_FILE


ROOT = Path(__file__).parent
LOCALES = ('es-419', 'en', 'zh-Hant', 'ru', 'zh-Hans')
PRODUCTS = (
    ('coated', 'coated', 'paper', 'print'),
    ('thermal', 'thermal', 'paper', 'logistics'),
    ('bopp', 'bopp', 'film', 'rigid'),
    ('pe', 'pe', 'film', 'squeeze'),
    ('pet', 'pet', 'film', 'equipment'),
    ('woodfree', 'wood', 'paper', 'a_d'),
)
FAMILIES = ('all', 'paper', 'film')
APPLICATIONS = ('all', 'print', 'logistics', 'rigid', 'squeeze', 'equipment', 'a_d')
CATALOG = re.compile(
    r'<section>(<h1>[^<]*</h1>(?:<p>.*?</p>)*)<label class="search">.*?id="lookup"></label>'
    r'<div class="appgrid">(.*?)</div><p hidden id="no-results">.*?</p></section>',
    re.S,
)
CARD = re.compile(
    r'<a class="appcard" data-search="([^"]*)" href="([^"]*)"><span>(.*?)</span>'
    r'<h3>(.*?)</h3><p>(.*?)</p></a>',
    re.S,
)


def catalog_section(match, copy, sample_path, product_paths):
    labels = copy['labels']

    def label(key):
        return escape(labels[key])

    def options(keys):
        return ''.join(f'<option value="{key}">{label(key)}</option>' for key in keys)

    originals = {}
    for original in CARD.finditer(match[2]):
        target = original[2].partition('#')[0].lstrip('/').removesuffix('.html')
        originals[target] = original
    if len(originals) != len(PRODUCTS) or set(originals) != set(product_paths.values()):
        raise ValueError('Expected the six configured products in the catalog')

    cards = []
    for route, code, family, use in PRODUCTS:
        search, href, caption, title, description = originals[product_paths[route]].groups()
        detail = href.partition('#')[0]
        keywords = escape(unescape(search) + ' ' + copy['products'][code]['keywords'], quote=True)
        if route == 'woodfree':
            action = label('a_d')
            link = detail + '#compare'
            note = f'<p class="finder-wood-note">{label("wood_note")}</p>'
        else:
            action = label('sample')
            link = escape(f'{sample_path}?material={code}&mode=sample', quote=True)
            note = ''
        accessible_title = escape(unescape(re.sub(r'<[^>]+>', '', title)), quote=True)
        cards.append(
            f'<article class="finder-card" data-product="{code}" data-family="{family}" '
            f'data-use="{use}" data-keywords="{keywords}">'
            f'<p class="finder-caption">{label(family)} · {caption}</p>'
            f'<h2>{title}</h2><p>{description}</p>{note}'
            f'<div class="finder-actions"><a href="{detail}" aria-label="{label("view")} · {accessible_title}">{label("view")}</a>'
            f'<a href="{link}" aria-label="{action} · {accessible_title}">{action}</a></div></article>'
        )

    status = escape(labels['rows_status'].format(count=len(cards)))
    return (
        f'<section id="product-finder" data-product-finder>{match[1]}'
        f'<form class="finder-toolbar" role="search" hidden><p class="finder-intro">{label("intro")}</p>'
        f'<label class="finder-query">{label("search_label")}'
        f'<input name="q" type="search" placeholder="{label("placeholder")}" autocomplete="off"></label>'
        f'<label>{label("family_label")}<select name="family">{options(FAMILIES)}</select></label>'
        f'<label>{label("application_label")}<select name="use">{options(APPLICATIONS)}</select></label>'
        f'<div class="finder-meta"><p role="status" data-result-status data-format="{label("rows_status")}">'
        f'{status}</p><button type="reset">{label("reset")}</button></div></form>'
        '<div class="finder-cards">' + ''.join(cards) + '</div>'
        f'<p class="finder-empty" data-empty hidden>{label("none")}</p></section>'
    )


def apply_product_catalog(dist, groups, labels):
    """Add the finder, retain each catalog H1, and label the five-language entry points."""
    for asset in ('product-finder.css', 'product-finder.js'):
        copyfile(ROOT / asset, dist / asset)

    for i, language in enumerate(LOCALES):
        copy = labels[language]
        nav_label = escape(copy['labels']['nav'])
        catalog = groups['catalog'][i]
        sample_path = '/' + groups['request'][i].removesuffix('.html')
        product_paths = {route: groups[route][i].removesuffix('.html') for route, *_ in PRODUCTS}
        catalog_slug = re.escape(catalog.removesuffix('.html'))
        catalog_link = re.compile(r'(<a\b[^>]*?\shref="/?' + catalog_slug + r'(?:\.html)?"[^>]*>)[^<]*(</a>)')

        def relabel(match):
            return catalog_link.sub(lambda link: link[1] + nav_label + link[2], match[0])

        pages = [paths[i] for paths in groups.values()]
        if i == 0 and (dist / GUIDE_FILE).is_file():
            pages.append(GUIDE_FILE)
        for filename in pages:
            path = dist / filename
            html = path.read_text(encoding='utf-8')
            revised = re.sub(r'<nav>.*?</nav>', relabel, html, count=1, flags=re.S)
            if filename == groups['home'][i]:
                revised = re.sub(r'<div class="hero-actions">.*?</div>', relabel, revised, count=1, flags=re.S)
            if filename == catalog:
                revised, count = CATALOG.subn(lambda match: catalog_section(match, copy, sample_path, product_paths), revised, count=1)
                if count != 1:
                    raise ValueError('Could not locate product catalog in ' + filename)
                assets = '<link rel="stylesheet" href="/product-finder.css"><script defer src="/product-finder.js"></script>'
                revised = revised.replace('</head>', assets + '</head>', 1)
            if revised != html:
                path.write_text(revised, encoding='utf-8')
