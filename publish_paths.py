"""Publish one clean path per page and provide matching Render routes."""
import json
import re
from pathlib import Path
from shutil import copyfile
from urllib.parse import urlsplit

from professional_update import CATALOG_URLS
from seo_update import canonical_path

# Match only URL-valued attributes in HTML, never external references or prose.
URL_ATTRIBUTE = re.compile(r'''(\s(?:href|src|action|content)=)(["'])([^"']*)\2''')
SCHEMA = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def normalize_urls(dist, origin):
    pages = sorted(dist.glob('*.html'))
    targets = {page.name: canonical_path(page.name) for page in pages}
    targets.update({old + '.html': '/' + new for old, new in CATALOG_URLS.items()})

    def clean(value):
        if '.html' not in value:
            return value
        url = urlsplit(value)
        if url.scheme or url.netloc:
            if (url.scheme, url.netloc) != (urlsplit(origin).scheme, urlsplit(origin).netloc):
                return value
        path = url.path.removeprefix('./').removeprefix('/')
        if path not in targets:
            return value
        return url._replace(path=targets[path]).geturl()

    def json_urls(node):
        if isinstance(node, str):
            return clean(node)
        if isinstance(node, dict):
            return {key: json_urls(value) for key, value in node.items()}
        if isinstance(node, list):
            return [json_urls(value) for value in node]
        return node

    for page in pages:
        source = page.read_text(encoding='utf-8')
        source = URL_ATTRIBUTE.sub(lambda m: m[1] + m[2] + clean(m[3]) + m[2], source)
        source = SCHEMA.sub(lambda m: m[1] + json.dumps(json_urls(json.loads(m[2])), ensure_ascii=False).replace('</', '<\\/') + m[3], source)
        page.write_text(source, encoding='utf-8')
    sitemap = dist / 'sitemap.xml'
    xml = re.sub(r'(<loc>)([^<]+)(</loc>)', lambda m: m[1] + clean(m[2]) + m[3], sitemap.read_text(encoding='utf-8'))
    sitemap.write_text(xml, encoding='utf-8')
    return pages


def render_routes(pages):
    redirects = {'/index': '/'}
    redirects.update({'/' + page.name: canonical_path(page.name) for page in pages})
    for old, new in CATALOG_URLS.items():
        redirects['/' + old] = redirects['/' + old + '.html'] = '/' + new
    return [
        {'type': 'redirect', 'source': src, 'destination': dest}
        for src, dest in sorted(redirects.items())
    ] + [
        {'type': 'rewrite', 'source': '/', 'destination': '/_pages/index.htm'},
        {'type': 'rewrite', 'source': '/:page', 'destination': '/_pages/:page.htm'},
    ]


def publish_pages(dist, origin):
    pages = normalize_urls(dist, origin)
    config = json.loads(Path(__file__).with_name('render.yaml').read_text(encoding='utf-8'))
    if config['services'][0]['routes'] != render_routes(pages):
        raise ValueError('Update render.yaml routes to match the generated pages (python3 publish_paths.py).')
    backing = dist / '_pages'
    backing.mkdir(exist_ok=True)
    for page in pages:
        copyfile(page, backing / (page.stem + '.htm'))
    return len(pages)


if __name__ == '__main__':
    root = Path(__file__).parent
    config = root / 'render.yaml'
    data = json.loads(config.read_text())
    pages = list((root / 'dist').glob('*.html'))
    if not pages:
        raise SystemExit('Build the site before refreshing its routes.')
    data['services'][0]['routes'] = render_routes(pages)
    config.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
