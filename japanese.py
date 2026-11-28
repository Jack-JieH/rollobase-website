"""Add Japanese equivalents to the completed catalog, preserving form values and links."""
import csv
from html import escape
import json
from pathlib import Path
import re
from shutil import copyfile
from urllib.parse import urlsplit

from localization import LocalizedPage

HERE = Path(__file__).parent
COPY = json.loads((HERE / 'japanese.json').read_text(encoding='utf-8'))
COLD = 'guia-bopp-botellas-refrigeradas'
COLD_JA = 'cold-bopp-ja'
JAPANESE_PATHS = {
    'en': 'ja', 'about': 'about-ja', 'products': 'products-ja',
    'self-adhesive-labelstock-jumbo-rolls': 'materials-ja', 'quote-sample': 'request-ja',
    'sourcing': 'sourcing-ja', 'quality-traceability': 'quality-ja',
    'printing-compatibility': 'printing-ja', 'uncoated-woodfree': 'woodfree-ja',
    'semi-gloss-coated-paper': 'coated-ja', 'direct-thermal-paper': 'thermal-ja',
    'bopp-film': 'bopp-ja', 'pe-film': 'pe-ja', 'pet-film': 'pet-ja', COLD: COLD_JA,
}
JA_BRIEF = 'brief-ja.txt'
JA_TRIAL = 'cold-bopp-trial-ja.csv'
FILES = {'brief-en.txt': JA_BRIEF, 'brief-es-419.txt': JA_BRIEF,
         'registro-prueba-bopp-refrigeracion.csv': JA_TRIAL}
ALTERNATE = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">')
PICKER = re.compile(r'<details class="languages language-picker">.*?</details>', re.S)
SCHEMA = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def translated(text):
    term = text.strip()
    if not term:
        return text
    if term in COPY:
        return text.replace(term, COPY[term], 1)
    # Native language names in the language menu, symbols, dates and measurements.
    if term in ('Русский', '繁體中文', '简体中文', '日本語') or not re.search(r'[a-zA-ZÀ-ÿ]', term):
        return text
    raise ValueError(f'Missing Japanese translation for {term!r}')


def japanese_path(english):
    if english in JAPANESE_PATHS:
        return JAPANESE_PATHS[english]
    if english.endswith('-en'):
        return english[:-3] + '-ja'
    raise ValueError(f'Japanese route required for {english!r}')


def page_slug(url):
    return urlsplit(url).path.strip('/').removesuffix('.html') or 'index'


class JapanesePage(LocalizedPage):
    def url(self, value):
        url = urlsplit(value)
        if url.scheme not in ('', 'https', 'http') or (url.netloc and url.netloc != urlsplit(self.origin).netloc):
            return value
        if not url.path and not url.netloc:
            return value
        name = url.path.strip('/')
        target = FILES.get(name) or self.mapping.get(page_slug(value))
        if target:
            return url._replace(path='/' + target).geturl()
        return value

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('data-keywords', 'data-contact', 'data-format', 'data-message', 'title'):
            if key in attrs and attrs[key]:
                attrs[key] = translated(attrs[key])
        super().handle_starttag(tag, attrs.items())

    def schema(self, node, key=None):
        if isinstance(node, dict) and node.get('@type') in ('WebSite', 'Organization'):
            # These entities and their identifiers are shared by every locale.
            return node
        if isinstance(node, str):
            if key in ('headline', 'articleSection'):
                return translated(node)
            if key == 'mainEntityOfPage':
                return self.url(node)
            if key == '@id' and urlsplit(node).fragment in ('website', 'organization'):
                return node
        return super().schema(node, key)


def update_site_languages(html):
    def update(match):
        graph = json.loads(match[2])
        changed = False
        for node in graph.get('@graph', [graph]):
            if node.get('@type') == 'WebSite':
                langs = node.get('inLanguage')
                if isinstance(langs, list) and 'ja' not in langs:
                    langs.append('ja')
                    changed = True
        if not changed:
            return match[0]
        return match[1] + json.dumps(graph, ensure_ascii=False).replace('</', '<\\/') + match[3]
    return SCHEMA.sub(update, html)


def connect_language(html, japanese, origin, active=False, cold=False):
    path = '/' + japanese
    # The site may be rebuilt into an existing preview directory.
    rebuilt_alternates = {'ja', 'es-419', 'x-default'} if cold else {'ja'}
    html = ALTERNATE.sub(lambda m: '' if m[1] in rebuilt_alternates else m[0], html)
    ja_link = f'<link rel="alternate" hreflang="ja" href="{origin}{path}">'
    if cold:
        es = f'{origin}/{COLD}'
        ja_link += f'<link rel="alternate" hreflang="es-419" href="{es}"><link rel="alternate" hreflang="x-default" href="{es}">'
    html = html.replace('</head>', ja_link + '</head>', 1)

    def update_picker(match):
        menu = match[0]
        menu = re.sub(r'<a\b[^>]*\blang="ja"[^>]*>.*?</a>', '', menu, flags=re.S)
        if active:
            menu = menu.replace(' aria-current="page"', '')
            menu = re.sub(r'<summary[^>]*>.*?</summary>', '<summary aria-label="言語：日本語（JA）">'
                          '<img class="language-flag" src="/flags/jp.png" width="28" height="21" alt="">'
                          '<span>JA</span><span class="language-chevron" aria-hidden="true"></span></summary>', menu, count=1, flags=re.S)
        if cold:
            # Only Spanish and Japanese have this guide; other languages keep catalog exits.
            menu = re.sub(r'<a href="[^"]+" lang="(es(?:-419)?)"', rf'<a href="/{COLD}" lang="\1"', menu, count=1)
        current = ' aria-current="page"' if active else ''
        option = (f'<a href="{path}" lang="ja" hreflang="ja" aria-label="日本語"{current}>'
                  '<img class="language-flag" src="/flags/jp.png" width="28" height="21" alt=""><span>日本語</span></a>')
        return menu.replace('</div></details>', option + '</div></details>', 1)

    html, n = PICKER.subn(update_picker, html, count=1)
    if n != 1:
        raise ValueError(f'Missing language picker for {path}')
    return update_site_languages(html)


def link_cold_guide(html, page):
    # The English source has no translated cold guide. Surface the Japanese
    # equivalent in the same buying journeys served by the Spanish guide.
    if page not in ('ja', 'materials-ja', 'products-ja', 'bopp-ja', 'news-ja', 'news-bopp-vs-pe-ja'):
        return html
    card = ('<section class="record-callout"><h2>冷蔵ボトル用のBOPPラベル</h2>'
            '<p>白色と透明の仕上がりを比較し、乾いたボトルと結露したボトルで貼付条件を確かめます。</p>'
            f'<a href="/{COLD_JA}">冷蔵ボトルの選定・試験ガイドを見る →</a></section>')
    return html.replace('</main>', card + '</main>', 1)


def write_downloads(dist):
    fields = ['ラベルの用途', '容器・使用条件', '貼付温度・使用温度（°C）', '表面基材・粘着剤・剥離ライナー',
              '印刷機・インキまたはリボン', '有効幅（mm）・長さ（m）', '紙管内径・最大ロール外径（mm）',
              '数量（m²）・仕向地', '試験方法・合否基準']
    (dist / JA_BRIEF).write_text('粘着ラベル原反のサンプル・見積もり依頼\n\n' +
                                '\n\n'.join(f'{label} ___________________' for label in fields) + '\n', encoding='utf-8-sig')
    headers = ['日付', 'ボトルID', 'ボトルの材質・表面仕上げ', 'サンプル品番・ロット', '表面基材', '粘着剤', '剥離ライナー',
               '絵柄・白インキ下刷り', '貼付時の表面状態', '貼付時のボトル温度（°C）', '貼付から冷蔵までの時間',
               '冷蔵温度（°C）', '冷蔵時間', '追加の暴露条件', '観察時点', '透明性・気泡', '浮き・しわ',
               'コントラスト・コードの読み取り', 'センサー検知・打ち抜き・繰り出し', '写真・ファイル', '合否基準', '結果', '備考']
    with (dist / JA_TRIAL).open('w', newline='', encoding='utf-8-sig') as target:
        csv.writer(target).writerow(headers)
    copyfile(HERE / 'flag-jp.png', dist / 'flags' / 'jp.png')


def add_japanese(dist, origin):
    dist, origin = Path(dist), origin.rstrip('/')
    originals = {}
    targets, sources = {}, {}
    for page in sorted(dist.glob('*.html')):
        html = page.read_text(encoding='utf-8')
        lang = re.search(r'<html lang="([^"]+)"', html)[1]
        if lang == 'ja':
            continue
        originals[page.stem] = html
        alternates = dict(ALTERNATE.findall(html))
        english = page_slug(alternates['en']) if 'en' in alternates else page.stem
        target = japanese_path(english)
        targets[page.stem] = target
        if lang == 'en' or page.stem == COLD:
            sources[target] = page.stem
    if set(targets.values()) != set(sources):
        raise ValueError('Every language group needs a Japanese translation source')

    for source, html in originals.items():
        target = targets[source]
        (dist / (source + '.html')).write_text(connect_language(html, target, origin, cold=source == COLD), encoding='utf-8')
    for target, source in sources.items():
        page = JapanesePage(translated, targets, origin, 'ja')
        page.feed(originals[source])
        page.close()
        result = connect_language(''.join(page.out), target, origin, active=True, cold=source == COLD)
        result = result.replace('</head>', '<meta property="og:locale" content="ja_JP"></head>', 1)
        result = link_cold_guide(result, target)
        (dist / (target + '.html')).write_text(result, encoding='utf-8')

    # Preserve existing sitemap metadata and use the translation's actual introduction date.
    sitemap = dist / 'sitemap.xml'
    xml = sitemap.read_text(encoding='utf-8')
    existing = {page_slug(url) for url in re.findall(r'<loc>([^<]+)</loc>', xml)}
    entries = ''.join(f'<url><loc>{escape(origin)}/{target}</loc><lastmod>2026-11-28</lastmod></url>'
                      for target in sorted(sources.keys() - existing))
    sitemap.write_text(xml.replace('</urlset>', entries + '</urlset>'), encoding='utf-8')
    write_downloads(dist)
