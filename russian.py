"""Build Russian pages with shared markup and explicit translated copy."""
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit

RU_ROUTES = {
    'home':'ru.html', 'guide':'products-ru.html', 'catalog':'materials-ru.html',
    'request':'request-ru.html', 'sourcing':'sourcing-ru.html',
    'quality':'quality-ru.html', 'printing':'printing-ru.html',
    'woodfree':'woodfree-ru.html', 'coated':'coated-ru.html',
    'thermal':'thermal-ru.html', 'bopp':'bopp-ru.html',
    'pe':'pe-ru.html', 'pet':'pet-ru.html',
}
COPY = json.loads(Path(__file__).with_name('russian.json').read_text())

def translate(text):
    value = text.strip()
    if not value or re.fullmatch(r'[\d\s./–—→↓²µμ°%+-]+', value):
        return text
    if value in COPY:
        result = COPY[value]
    elif value + ' | RolloBase' in COPY:
        result = COPY[value + ' | RolloBase'].removesuffix(' | RolloBase')
    elif '/ ' + value in COPY:
        result = COPY['/ ' + value].removeprefix('/ ')
    else:
        raise ValueError(f'Missing Russian copy: {value!r}')
    return text[:len(text)-len(text.lstrip())] + result + text[len(text.rstrip()):]

class RussianPage(HTMLParser):
    def __init__(self, mapping, origin):
        super().__init__(convert_charrefs=True)
        self.mapping, self.origin = mapping, origin
        self.out, self.script, self.json_script = [], False, False

    def url(self, value):
        u = urlsplit(value)
        if u.netloc and u.netloc != urlsplit(self.origin).netloc:
            return value
        name = u.path.lstrip('/')
        for source, target in self.mapping.items():
            if name in (source, source.removesuffix('.html')):
                path = target if name.endswith('.html') else target.removesuffix('.html')
                if u.path.startswith('/'):
                    path = '/' + path
                return urlunsplit((u.scheme, u.netloc, path, u.query, u.fragment))
        return value

    def schema(self, node, key=None):
        if isinstance(node, dict):
            return {k:self.schema(v,k) for k,v in node.items()}
        if isinstance(node, list):
            return node if key == 'inLanguage' else [self.schema(v) for v in node]
        if isinstance(node, str):
            if key in ('name','description','text'):
                return translate(node)
            if key == 'inLanguage':
                return 'ru'
            if key in ('url','@id','item'):
                return self.url(node)
        return node

    def handle_decl(self, data):
        self.out.append('<!'+data+'>')

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        language_link = tag == 'a' and 'lang' in attrs
        alternate = tag == 'link' and attrs.get('rel') == 'alternate'
        if tag == 'html':
            attrs['lang'] = 'ru'
        if language_link:
            attrs.pop('aria-current', None)
            if attrs['lang'] == 'ru':
                attrs['aria-current'] = 'page'
        if tag == 'script':
            self.script = True
            self.json_script = attrs.get('type') == 'application/ld+json'
        for name,value in list(attrs.items()):
            if value is None:
                continue
            if name in ('alt','aria-label','placeholder'):
                attrs[name] = translate(value)
            elif name == 'href' and not language_link and not alternate:
                attrs[name] = self.url(value)
            elif tag == 'meta' and name == 'content':
                if attrs.get('name') == 'description' or attrs.get('property') in ('og:title','og:description'):
                    attrs[name] = translate(value)
                elif attrs.get('property') == 'og:url':
                    attrs[name] = self.url(value)
        serialized = ''.join(' '+k if v is None else f' {k}="{escape(v,quote=True)}"' for k,v in attrs.items())
        self.out.append('<'+tag+serialized+'>')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)

    def handle_endtag(self, tag):
        self.out.append('</'+tag+'>')
        if tag == 'script':
            self.script = self.json_script = False

    def handle_data(self, data):
        if self.json_script:
            self.out.append(json.dumps(self.schema(json.loads(data)),ensure_ascii=False))
        elif self.script:
            self.out.append(data)
        else:
            self.out.append(escape(translate(data),quote=False))

def add_russian(dist, groups, origin):
    mapping = {paths[1]:RU_ROUTES[key] for key,paths in groups.items()}
    mapping['brief-en.txt'] = 'brief-ru.txt'
    for key, paths in groups.items():
        ru = RU_ROUTES[key]
        for path in paths:
            source = (dist/path).read_text()
            source = source.replace('</head>', f'<link rel="alternate" hreflang="ru" href="{origin}/{ru.removesuffix(".html")}"></head>')
            source = re.sub(r'(<div class="languages">.*?)(</div>)', rf'\1<a href="{ru}" lang="ru">RU</a>\2', source, count=1)
            source = source.replace('"inLanguage": ["es", "en", "zh-Hant"]','"inLanguage": ["es", "en", "zh-Hant", "ru"]')
            (dist/path).write_text(source)
        parser = RussianPage(mapping,origin)
        parser.feed((dist/paths[1]).read_text())
        (dist/ru).write_text(''.join(parser.out))
    brief = (dist/'brief-en.txt').read_text(encoding='utf-8-sig')
    (dist/'brief-ru.txt').write_text('\n'.join(translate(line.removesuffix(' ___________________')) + (' ___________________' if line.endswith(' ___________________') else '') for line in brief.split('\n')),encoding='utf-8-sig')
    return list(RU_ROUTES.values())
