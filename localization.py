"""Build localized HTML without translating identifiers or application state."""
from html import escape
from html.parser import HTMLParser
import json
from urllib.parse import urlsplit, urlunsplit


class LocalizedPage(HTMLParser):
    def __init__(self, translate, mapping, origin, language):
        super().__init__(convert_charrefs=True)
        self.translate, self.mapping = translate, mapping
        self.origin, self.language = origin, language
        self.out, self.script, self.json_script = [], False, False

    def url(self, value):
        u = urlsplit(value)
        if u.netloc and u.netloc != urlsplit(self.origin).netloc:
            return value
        name = u.path.lstrip('/')
        for source, target in self.mapping.items():
            if name in (source, source.removesuffix('.html')):
                path = target if name.endswith('.html') or not source.endswith('.html') else target.removesuffix('.html')
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
                return self.translate(node)
            if key == 'inLanguage':
                return self.language
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
            attrs['lang'] = self.language
        if tag == 'script':
            self.script = True
            self.json_script = attrs.get('type') == 'application/ld+json'
        for name,value in list(attrs.items()):
            if value is None:
                continue
            if name in ('alt','aria-label','placeholder','data-search'):
                attrs[name] = self.translate(value)
            elif name == 'href' and not language_link and not alternate:
                attrs[name] = self.url(value)
            elif tag == 'meta' and name == 'content':
                if attrs.get('name') == 'description' or attrs.get('property') in ('og:title','og:description'):
                    attrs[name] = self.translate(value)
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
            self.out.append(escape(self.translate(data),quote=False))
