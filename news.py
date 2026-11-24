"""Publish original, localized buyer guides without changing existing product bodies."""
from pathlib import Path
from html import escape as e
import json,re
from catalog_layout import paths,homes,requests,langs,labels,abouts
SUFFIX=['es','en','zh','ru','zh-cn']
SLUGS=['choose-labelstock','bopp-vs-pe','thermal-vs-semigloss','woodfree-a-d','label-adhesion-troubleshooting','master-roll-quotation']
UI=[
['Noticias y guías','Guías prácticas de selección, pruebas y compra de materiales autoadhesivos.','Selección','Qué comprobar en la prueba','¿Qué información debo enviar?','Productos relacionados','Solicitar muestras','Seguir leyendo','Referencias técnicas','Publicado','RolloBase · Guías de materiales'],
['News & guides','Practical guides to selecting, testing and buying self-adhesive label materials.','Selection points','What to check in a trial','What information should I send?','Related products','Request samples','Further reading','Technical references','Published','RolloBase · Material guides'],
['News・選材指南','從選材、試樣到詢價，整理不乾膠母卷採購時常遇到的問題。','選材重點','試樣時檢查什麼','需要提供哪些資料？','相關產品','申請樣品','延伸閱讀','技術參考','發布日期','RolloBase・材料指南'],
['Новости и руководства','Практические руководства по выбору, испытаниям и закупке самоклеящихся материалов.','Выбор материала','Что проверить при испытании','Какие данные предоставить?','Связанные материалы','Запросить образцы','Другие статьи','Технические источники','Опубликовано','RolloBase · Руководства по материалам'],
['News・选材指南','从选材、试样到询价，整理不干胶母卷采购时常遇到的问题。','选材重点','试样时检查什么','需要提供哪些资料？','相关产品','申请样品','延伸阅读','技术参考','发布日期','RolloBase・材料指南']]
REFS={0:[('Avery Dennison — Adhesive Technologies','https://label.averydennison.com/content/dam/averydennison/lpm-responsive/europe/english/documents/product-overviews/product/adhesives/lpm-eu-technical%20guide-adhesive%20technologies-2020-web.pdf')],1:[('UPM — Film label materials','https://www.adhesivematerials.upm.com/label-solutions/label-types/film-label-materials/')],2:[('Zebra — Direct thermal and thermal transfer','https://www.zebra.com/us/en/resource-library/faq/difference-between-direct-thermal-and-thermal-transfer-printing.html')]}
REFS[4]=REFS[0]
RELATED=[['coated','bopp'],['bopp','pe'],['thermal','coated'],['wood'],['bopp','pe'],['thermal','coated','wood']]
PHOTOS=['jumbo-coated','jumbo-bopp','jumbo-thermal',None,None,'jumbo-coated']
CSS='''.news-main{padding:42px 0 64px}.news-main h1{max-width:900px}.news-lead{font-size:19px;max-width:850px}.news-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px;margin:36px 0}.news-card{border:1px solid var(--line);padding:24px}.news-card h2{font-size:22px;line-height:1.4}.news-card p{color:var(--muted)}.news-card a:hover{text-decoration:underline}.news-article{max-width:800px;margin:auto}.news-article p{font-size:17px;line-height:1.9}.news-article h2{font-size:25px;margin-top:38px}.news-meta{color:var(--muted);font-size:13px!important}.news-photo{max-width:100%;width:520px;height:auto;display:block;margin:28px auto}.news-related{padding:22px;background:#f1f5e9;margin:28px 0}.news-related a{display:inline-block;margin:6px 18px 6px 0;text-decoration:underline}.news-faq{padding:22px;border:1px solid var(--line)}.news-faq summary{font-weight:bold;cursor:pointer}.news-links li{margin:12px 0}.news-links a{text-decoration:underline}.news-main table{border-collapse:collapse;width:100%}.news-main th,.news-main td{padding:12px;border:1px solid var(--line);text-align:left}.news-main nav{flex-wrap:wrap;gap:15px}.news-main a:focus-visible{outline:3px solid #bd4a2a}@media(max-width:760px){.news-grid{grid-template-columns:1fr}.news-main{padding-top:24px}.news-article p{font-size:16px}.news-main h1{font-size:28px}.news-lead{font-size:17px}.news-card{padding:20px}}'''
def apply_news(dist,origin):
 dist=Path(dist); data=json.loads(Path(__file__).with_name('news-content.json').read_text())
 all_new=[]
 for i,lang in enumerate(langs):
  u=UI[i]; rows=data[lang]; hub=f'news-{SUFFIX[i]}.html'
  catalog=(dist/paths[i]).read_text()
  header=re.search(r'<header>.*?</header>',catalog,re.S)[0]
  footer=re.search(r'<footer>.*?</footer>',catalog,re.S)[0]
  products={}
  for card in re.findall(r'<article class="finder-card.*?</article>',catalog,re.S):
   code=re.search(r'data-product="([^"]+)"',card)[1]
   products[code]=(re.search(r'<div class="finder-actions"><a href="([^"]+)"',card)[1],re.search(r'<h2>(.*?)</h2>',card,re.S)[1])
  def render(filename,title,description,body,article=None):
   alternate=[f'news-{s}.html' if article is None else f'news-{SLUGS[article]}-{s}.html' for s in SUFFIX]
   switch=''.join(f'<a href="/{f}" lang="{l}"'+(' aria-current="page"' if j==i else '')+'>'+n+'</a>' for j,(f,l,n) in enumerate(zip(alternate,langs,['ES','EN','繁中','RU','简中'])))
   h=re.sub(r'<div class="languages">.*?</div>',lambda m:'<div class="languages">'+switch+'</div>',header,flags=re.S)
   h=h.replace('</nav>',f'<a href="/{hub}">{e(u[0])}</a></nav>',1)
   url=origin+'/'+filename
   schema={'@context':'https://schema.org','@type':'CollectionPage' if article is None else 'Article','name':title,'headline':title,'description':description,'inLanguage':lang,'url':url,'publisher':{'@type':'Organization','name':'RolloBase','url':origin},'mainEntityOfPage':url}
   if article is not None:
    schema.update(datePublished='2026-11-24',dateModified='2026-11-24',author={'@type':'Organization','name':'RolloBase'},articleSection=u[0])
    if PHOTOS[article]:schema['image']=origin+'/photos/'+PHOTOS[article]+'.webp'
   head=f'<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} | RolloBase</title><meta name="description" content="{e(description)}"><link rel="canonical" href="{url}">'
   head+=''.join(f'<link rel="alternate" hreflang="{l}" href="{origin}/{f}">' for l,f in zip(langs+['x-default'],alternate+[alternate[0]]))
   head+=f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{url}"><meta property="og:type" content="'+('website' if article is None else 'article')+'"><link rel="stylesheet" href="/catalog-layout.css"><link rel="stylesheet" href="/news.css"><script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</','<\\/')+'</script>'
   (dist/filename).write_text(f'<!doctype html><html lang="{lang}"><head>{head}</head><body>{h}<main class="wrap news-main">{body}</main>{footer}</body></html>')
   all_new.append(filename)
  cards=''
  for n,row in enumerate(rows):
   name=f'news-{SLUGS[n]}-{SUFFIX[i]}.html';title,desc,p1,p2,p3=row
   cards+=f'<article class="news-card"><span class="news-meta">{e(u[10])}</span><h2><a href="/{name}">{e(title)}</a></h2><p>{e(desc)}</p></article>'
   body=f'<article class="news-article"><nav aria-label="Breadcrumb"><a href="/{hub}">{e(u[0])}</a></nav><h1>{e(title)}</h1><p class="news-meta">RolloBase · {e(u[9])} <time datetime="2026-11-24">2026-11-24</time></p><p class="news-lead">{e(desc)}</p>'
   if PHOTOS[n]:
    photo_name=products['bopp' if n==1 else 'thermal' if n==2 else 'coated'][1]
    body+=f'<img class="news-photo" src="/photos/{PHOTOS[n]}.webp" alt="{e(photo_name)}" width="880" height="660">'
   body+=f'<h2>{e(u[2])}</h2><p>{e(p1)}</p><h2>{e(u[3])}</h2><p>{e(p2)}</p><details class="news-faq" open><summary>{e(u[4])}</summary><p>{e(p3)}</p></details>'
   body+=f'<aside class="news-related"><h2>{e(u[5])}</h2>'+''.join(f'<a href="{products[k][0]}">{products[k][1]}</a>' for k in RELATED[n])+f'<p><a class="button" href="/{requests[i]}?mode=sample">{e(u[6])} →</a></p></aside>'
   if n in REFS:body+=f'<h2>{e(u[8])}</h2><ul class="news-links">'+''.join(f'<li><a href="{e(url)}" rel="noopener">{e(t)}</a></li>' for t,url in REFS[n])+'</ul>'
   body+=f'<h2>{e(u[7])}</h2><ul class="news-links">'+''.join(f'<li><a href="/news-{SLUGS[j]}-{SUFFIX[i]}.html">{e(rows[j][0])}</a></li>' for j in range(6) if j!=n)+'</ul></article>'
   render(name,title,desc,body,n)
  render(hub,u[0],u[1],f'<h1>{e(u[0])}</h1><p class="news-lead">{e(u[1])}</p><div class="news-grid">{cards}</div>')
 # Add discoverable links to existing navigation without replacing any page content.
 for path in dist.glob('*.html'):
  if path.name in all_new:continue
  s=path.read_text(); match=re.search(r'<html lang="([^"]+)"',s)
  if not match or match[1] not in langs:continue
  i=langs.index(match[1]);link=f'<a class="news-nav-link" href="/news-{SUFFIX[i]}.html">{e(UI[i][0])}</a>'
  if 'class="news-nav-link"' not in s:s=s.replace('</nav>',link+'</nav>',1)
  path.write_text(s)
 (dist/'news.css').write_text(CSS)
 sitemap=dist/'sitemap.xml';s=sitemap.read_text()
 for name in all_new:
  url=origin+'/'+name
  if '<loc>'+url+'</loc>' not in s:s=s.replace('</urlset>',f'<url><loc>{url}</loc><lastmod>2026-11-24</lastmod></url></urlset>')
 sitemap.write_text(s)
