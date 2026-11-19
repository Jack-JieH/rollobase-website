"""Publish reviewed buyer guidance and independent Chinese language versions."""
from html import escape, unescape
import json
from pathlib import Path
import re
from knowledge import VisibleFAQ, UPDATED
from localization import LocalizedPage
from russian import RU_ROUTES

ROOT = Path(__file__).parent
LANGUAGES = ['es', 'en', 'zh-Hant', 'ru', 'zh-Hans']
LABELS = ['ES', 'EN', '繁中', 'RU', '简中']
FULL_LABELS = ['Español', 'English', '繁體中文', 'Русский', '简体中文']
SC_ROUTES = {k:('zh-cn.html' if k=='home' else k+'-zh-cn.html') for k in RU_ROUTES}
CONTENT = json.loads((ROOT/'seo-content.json').read_text())


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
            title = CONTENT['titles'][key][i]+' | RolloBase'
            description = CONTENT.get('descriptions',{}).get(key,[None]*4)[i]
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
    return finalize_languages(dist,{key:paths+[SC_ROUTES[key]] for key,paths in groups.items()},origin)
