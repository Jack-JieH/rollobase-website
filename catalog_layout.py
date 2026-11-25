from pathlib import Path
import shutil,re,sys
from html import escape as e
from catalog_expansion import COMPANY_PARAGRAPHS
paths=['materiales.html','materials.html','catalog-zh.html','materials-ru.html','catalog-zh-cn.html']
homes=['index.html','en.html','zh.html','ru.html','zh-cn.html']
abouts=['empresa','about','about-zh','about-ru','about-zh-cn']
requests=['cotizacion-muestras','quote-sample','request-zh','request-ru','request-zh-cn']
guides=['productos','products','products-zh','products-ru','guide-zh-cn']
wood=['papel-no-estucado','uncoated-woodfree','woodfree-zh','woodfree-ru','woodfree-zh-cn']
printing=['pruebas-impresion','printing-compatibility','printing-zh','printing-ru','printing-zh-cn']
langs=['es-419','en','zh-Hant','ru','zh-Hans']
labels=[
 ['Vista previa · Diseño sin publicar','Inicio','Empresa','Productos','Guía técnica','Muestras y contacto','Materiales autoadhesivos en bobinas madre','Categorías de productos','Todos los materiales','Papeles autoadhesivos','Películas autoadhesivas','Papel siliconado','Ribbons y equipos','Opciones A–D','Conozca nuestra gama','Leer más sobre RolloBase','Ver menos','Materiales disponibles','Seleccione un material y consulte sus aplicaciones antes de pedir una muestra.','¿No sabe por dónde empezar?','Cuéntenos qué etiqueta necesita y sobre qué superficie se aplicará.','Preparar una muestra','Buscar material','También puede consultar','Contacto comercial'],
 ['Layout preview · Not published','Home','About us','Products','Technical guide','Samples & contact','Self-adhesive master-roll materials','Product categories','All materials','Paper labelstock','Film labelstock','Release paper','Ribbons & equipment','A–D options','Explore our range','Read more about RolloBase','Read less','Available materials','Choose a material and review its applications before requesting a sample.','Need help choosing?','Tell us what you are labelling and the surface it will stick to.','Prepare a sample request','Search materials','Also available','Sales contact'],
 ['版型預覽 · 尚未發布','首頁','公司介紹','產品目錄','材料技術','索樣與聯絡','不乾膠母卷材料','產品分類','全部材料','紙類不乾膠','薄膜不乾膠','離型紙','碳帶與設備','模造紙 A～D','從材料開始，找到適合的標籤組合','展開公司介紹','收起介紹','母卷產品','先看用途與材料介紹，再選擇需要試樣的產品。','還沒確定用哪一種？','告訴我們標籤的用途、被貼物與印刷方式，一起確認材料。','準備索樣需求','搜尋材料','其他材料與規格','業務聯絡'],
 ['Предпросмотр · Не опубликовано','Главная','О компании','Продукция','Техническое руководство','Образцы и контакты','Самоклеящиеся материалы в джамбо-рулонах','Категории продукции','Все материалы','Бумажные материалы','Плёночные материалы','Антиадгезионная бумага','Риббоны и оборудование','Варианты A–D','Подберите материал для этикетки','Подробнее о RolloBase','Свернуть','Материалы в ассортименте','Выберите материал и изучите применение перед запросом образца.','Нужна помощь с выбором?','Расскажите о назначении этикетки и поверхности нанесения.','Запросить образец','Поиск материалов','Другие материалы','Отдел продаж'],
 ['版式预览 · 尚未发布','首页','公司介绍','产品目录','材料技术','索样与联系','不干胶母卷材料','产品分类','全部材料','纸类不干胶','薄膜不干胶','离型纸','碳带与设备','书写纸 A～D','从材料开始，找到适合的标签组合','展开公司介绍','收起介绍','母卷产品','先看用途和材料介绍，再选择需要试样的产品。','还没确定用哪一种？','告诉我们标签的用途、被贴物和印刷方式，一起确认材料。','准备索样需求','搜索材料','其他材料与规格','业务联系']]
def apply_catalog_layout(out):
 out=Path(out)
 for i,file in enumerate(paths):
  s=(out/file).read_text();L=labels[i]
  cards=re.findall(r'<article class="finder-card[^"]*".*?</article>',s,re.S)
  assert len(cards)==10
  bycode={re.search(r'data-product="([^"]+)"',c)[1]:c for c in cards}
  keys=['coated','thermal','bopp','pe','pet','wood','color-thermal','color-coated','synthetic-paper','release-paper']
  cards=[bycode[k] for k in keys]
  sidebar=''.join(f'<a href="'+re.search(r'<div class="finder-actions"><a href="([^"]+)"',bycode[k])[1]+'">'+re.sub('<[^>]+>','',re.search(r'<h2>(.*?)</h2>',bycode[k],re.S)[1])+'</a>' for k in keys)
  original_form=re.search(r'<form class="finder-toolbar".*?</form>',s,re.S)[0]
  original_form=original_form.replace('<form class="finder-toolbar"','<form class="finder-toolbar"')
  empty=re.search(r'<p class="finder-empty".*?</p>',s,re.S)[0]
  tail=s.split(empty+'</section>',1)[1].split('</main>',1)[0]
  head=re.search(r'<head>(.*?)</head>',s,re.S)[1]
  head=re.sub(r'<link rel="stylesheet"[^>]*>','',head)
  head=re.sub(r'<script[^>]*src="[^"]*buyer.js[^"]*"[^>]*></script>','',head)
  head += '<link rel="stylesheet" href="/catalog-layout.css?v=20261124">'
  nav=''.join(f'<a href="/{p}">{e(t)}</a>' for p,t in [(homes[i],L[1]),(abouts[i],L[2]),(file,L[3]),(guides[i],L[4]),(requests[i],L[5])])
  switch=''.join(f'<a href="/{p}" lang="{lang}"'+(' aria-current="page"' if j==i else '')+'>'+name+'</a>' for j,(p,lang,name) in enumerate(zip(paths,langs,['ES','EN','繁中','RU','简中'])))
  intro='<p>'+e(COMPANY_PARAGRAPHS[i][0])+'</p><details class="intro-more"><summary>'+e(L[15])+' <span>＋</span></summary>'+''.join('<p>'+e(p)+'</p>' for p in COMPANY_PARAGRAPHS[i][1:])+'</details>'
  html=f'''<!doctype html><html lang="{langs[i]}"><head>{head}</head><body>
 <header><div class="topline wrap"><a class="brand" href="/{homes[i]}"><span class="brand-symbol">◎</span> RolloBase</a><p>{e(L[24])} <a href="tel:+8618588600270">+86 185 8860 0270</a></p><div class="languages">{switch}</div></div><div class="nav-band"><nav class="wrap">{nav}</nav></div></header>
 <div class="wrap breadcrumb"><a href="/{homes[i]}">{e(L[1])}</a><span> / </span>{e(L[3])}<span> / </span>{e(L[6])}</div>
 <div class="wrap layout"><aside class="sidebar"><details class="category-menu" open><summary>{e(L[7])}<span>⌄</span></summary><a class="all active" href="/{file}">{e(L[8])} <span>10</span></a><details open><summary>{e(L[6])}</summary><div class="category-links">{sidebar}</div></details><a href="/{wood[i]}#compare">{e(L[13])} →</a><a href="/{printing[i]}#ribbons-equipment">{e(L[12])} →</a></details><div class="sidebar-contact"><span class="tiny">ROLLOBASE</span><h3>{e(L[19])}</h3><p>{e(L[20])}</p><a class="button" href="/{requests[i]}?mode=sample">{e(L[21])} →</a></div></aside>
 <main><section class="intro"><div class="eyebrow">ROLLOBASE / LABEL MATERIALS</div><h1>{e(L[6])}</h1>{intro}</section><section class="products" data-product-finder><div class="section-heading"><div><h2>{e(L[17])}</h2><p>{e(L[18])}</p></div><span class="product-count">10</span></div>{original_form}<div class="finder-cards">{''.join(cards)}</div>{empty}</section><div class="catalog-guidance">{tail}</div><section class="closing"><h2>{e(L[19])}</h2><p>{e(L[20])}</p><a class="button" href="/{requests[i]}?mode=sample">{e(L[21])} →</a></section></main></div>
 <footer><div class="wrap footer-grid"><div class="footer-brand"><b>RolloBase</b><p>{e(COMPANY_PARAGRAPHS[i][0])}</p></div><div><h3>{e(L[3])}</h3><a href="/{file}">{e(L[8])}</a><a href="/{wood[i]}#compare">{e(L[13])}</a><a href="/{guides[i]}">{e(L[4])}</a></div><div><h3>{e(L[24])}</h3><a href="tel:+8618588600270">+86 185 8860 0270</a><a href="/{requests[i]}">{e(L[21])} →</a></div></div></footer><script>if(matchMedia('(max-width:760px)').matches)document.querySelector('.category-menu').open=false;</script></body></html>'''
  html=re.sub(r'href="/([^"?#]+)\.html"',lambda m:'href="'+('/' if m[1]=='index' else '/'+m[1])+'"' if (m[1]+'.html') in paths+homes else m[0],html)
  (out/file).write_text(html)
 shutil.copyfile(Path(__file__).with_name('catalog-layout.css'),out/'catalog-layout.css')
