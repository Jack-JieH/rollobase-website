"""Render the licensed application photographs after text localization."""

from html import escape
import json
from pathlib import Path
import re
from shutil import copyfile

from cold_bopp import GUIDE_FILE
from design_update import replace_once
from product_catalog import LOCALES, PRODUCTS


ROOT = Path(__file__).parent
CARD_PHOTOS = {
    'coated': 'jumbo-coated', 'thermal': 'jumbo-thermal', 'bopp': 'jumbo-bopp',
    'pe': 'squeeze', 'pet': 'jumbo-pet', 'wood': 'roll',
}


def photo_html(key, media, copy):
    photo = media[key]
    file = escape(photo['file'])
    src = f'/{file}' if key == 'pack' else f'/photos/{file}'
    width, height = photo['size']
    caption = escape(copy[f'photo_{key}'])
    style = f' site-photo-{key}'
    if photo.get('authorized_cutout'):
        return (
            f'<figure class="site-photo site-photo-cutout{style}">'
            f'<img src="{src}" width="{width}" height="{height}" alt="{caption}" loading="lazy" decoding="async">'
            f'<figcaption>{escape(copy["display_only"])} · {caption}'
            f'<small><a href="{escape(photo["page"])}">{escape(copy["edited_credit"])}</a></small>'
            '</figcaption></figure>'
        )
    cropped = f' · {escape(copy["cropped"])}' if photo.get('cropped') else ''
    return (
        f'<figure class="site-photo{style}"><img src="{src}" width="{width}" height="{height}" '
        f'alt="{caption}" loading="lazy" decoding="async">'
        f'<figcaption>{escape(copy["display_only"])} · {caption}'
        f'<small>{escape(copy["source"])} <a href="{escape(photo["page"])}">{escape(photo["author"])}</a> · '
        f'<a href="{escape(photo["license_url"])}">{escape(photo["license"])}</a>{cropped}</small>'
        '</figcaption></figure>'
    )


def add_site_photos(dist, groups):
    content = json.loads((ROOT / 'site-photos.json').read_text(encoding='utf-8'))
    media = content['photos']
    copyfile(ROOT / 'site-photos.css', dist / 'site-photos.css')

    for index, locale in enumerate(LOCALES):
        copy = content['copy'][locale]

        def photo(key):
            return photo_html(key, media, copy)

        def pair(first, second):
            return '<div class="site-photo-pair">' + photo(first) + photo(second) + '</div>'

        def gallery(title, section_id, photo_keys):
            figures = ''.join(photo(key) for key in photo_keys)
            return (
                f'<section id="{section_id}"><h2>{escape(copy[title])}</h2>'
                f'<div class="site-photo-gallery">{figures}</div></section>'
            )

        def home_cards(section):
            html = section[0]
            for product, code, _, _ in PRODUCTS:
                target = re.escape(groups[product][index]) + ('#compare' if code == 'wood' else '')
                html = replace_once(
                    r'<a class="appcard" href="' + target + r'">.*?</a>',
                    lambda link: f'<article class="site-photo-card photo-accent-{code}">'
                    + photo(CARD_PHOTOS[code]) + link[0] + '</article>',
                    html,
                )
            return html

        home = dist / groups['home'][index]
        html = replace_once(r'<section id="materials">.*?</section>', home_cards, home.read_text(encoding='utf-8'))
        html = replace_once(r'<figure data-paper-photo(?:="")?></figure>', photo('roll'), html)
        write_photos(home, html)

        catalog = dist / groups['catalog'][index]
        html = catalog.read_text(encoding='utf-8')
        for code, key in CARD_PHOTOS.items():
            html = replace_once(
                fr'<article class="finder-card" data-product="{code}"[^>]*>',
                lambda card: card[0].replace('class="finder-card"', f'class="finder-card photo-accent-{code}"') + photo(key),
                html,
            )
        write_photos(catalog, html)

        wood = dist / groups['woodfree'][index]
        html = replace_once(
            r'(<section class="coat-guide" id="coat-weight">.*?)</section>',
            lambda section: section[1] + pair('parcel', 'roll') + '</section>',
            wood.read_text(encoding='utf-8'),
        )
        write_photos(wood, html)

        for page, first, second in (
            ('about', 'roll', 'press'), ('sourcing', 'press', 'pack'),
            ('bopp', 'jumbo-bopp', 'bottle'), ('coated', 'jumbo-coated', 'pack'),
            ('thermal', 'jumbo-thermal', 'parcel'), ('pet', 'jumbo-pet', 'press'),
        ):
            path = dist / groups[page][index]
            html = replace_once(
                r'</section>', '</section>' + pair(first, second), path.read_text(encoding='utf-8'),
            )
            write_photos(path, html)

        photo_galleries = (
            ('guide', 'materials_gallery', 'material-photo-reference',
             ('jumbo-color-thermal', 'jumbo-color-coated', 'jumbo-synthetic', 'release-liner')),
            ('printing', 'printing_gallery', 'ribbons-equipment',
             ('ribbon-wax', 'ribbon-wax-resin', 'ribbon-resin', 'label-applicator')),
        )
        for page, title, section_id, keys in photo_galleries:
            path = dist / groups[page][index]
            html = replace_once(
                r'<p class="updated">', lambda marker: gallery(title, section_id, keys) + marker[0],
                path.read_text(encoding='utf-8'),
            )
            write_photos(path, html)

    guide = dist / GUIDE_FILE
    html = replace_once(
        r'(<section id="comparar"[^>]*>.*?</section>)',
        lambda section: section[1] + pair('bottle', 'rigid'),
        guide.read_text(encoding='utf-8'),
    )
    write_photos(guide, html)


def write_photos(path, html):
    css = '<link rel="stylesheet" href="/site-photos.css">'
    path.write_text(html.replace('</head>', css + '</head>', 1), encoding='utf-8')
