"""One shared catalogue shell for every locale and page."""
from pathlib import Path
from html import escape as e
import re
from catalog_layout import paths,langs,guides,homes
EXTRA=[['Compras e inspección','Documentación de calidad','Pruebas de impresión'],['Sourcing & inspection','Quality documents','Printing trials'],['採購與驗貨','品質文件','印刷試驗'],['Закупки и проверка','Документы качества','Печатные испытания'],['采购与验货','质量文件','印刷试验']]
ROUTES=[['abastecimiento','sourcing','sourcing-zh','sourcing-ru','sourcing-zh-cn'],['calidad-trazabilidad','quality-traceability','quality-zh','quality-ru','quality-zh-cn'],['pruebas-impresion','printing-compatibility','printing-zh','printing-ru','printing-zh-cn']]
def apply_unified_layout(dist):
 dist=Path(dist); templates=[]
 for name in paths:
  s=(dist/name).read_text()
  templates.append(tuple(re.search(pattern,s,re.S)[0] for pattern in [r'<header>.*?</header>',r'<aside class="sidebar">.*?</aside>',r'<footer>.*?</footer>']))
 for path in dist.glob('*.html'):
  s=path.read_text();lang=re.search(r'<html lang="([^"]+)"',s)[1];i=langs.index(lang)
  header,sidebar,footer=templates[i]
  original_langs=re.search(r'<div class="languages">.*?</div>',s,re.S)
  if original_langs:header=re.sub(r'<div class="languages">.*?</div>',lambda m:original_langs[0],header,flags=re.S)
  # Resolve technical subnavigation from existing pages rather than inventing routes.
  technical=[]
  for j,route in enumerate(ROUTES):
   target=dist/(route[i]+'.html')
   if target.exists():technical.append(f'<a href="/{route[i]}">{e(EXTRA[i][j])}</a>')
  if path.name == guides[i]+'.html':
   s=s.replace('</main>', '<section class="shared-tech-main"><h2>'+['Más guías','More guides','延伸技術指南','Другие руководства','延伸技术指南'][i]+'</h2><div class="toc">'+''.join(technical)+'</div></section></main>',1)
  sidebar=sidebar.replace('</aside>','<div class="shared-tech"><h3>'+['Guía técnica','Technical guide','材料技術','Техническое руководство','材料技术'][i]+'</h3>'+''.join(technical)+'</div></aside>')
  if path.name not in paths:
   body=re.search(r'<main\b[^>]*>(.*?)</main>',s,re.S)[1]
   s=re.sub(r'<main\b[^>]*>.*?</main>',lambda m:'<div class="wrap layout unified-layout">'+sidebar+'<main class="site-main">'+body+'</main></div>',s,count=1,flags=re.S)
  else:s=re.sub(r'<aside class="sidebar">.*?</aside>',lambda m:sidebar,s,count=1,flags=re.S)
  s=re.sub(r'<header>.*?</header>',lambda m:header,s,count=1,flags=re.S)
  s=re.sub(r'<footer>.*?</footer>',lambda m:footer,s,count=1,flags=re.S)
  s=s.replace('<body>','<body class="unified-site">',1)
  s=re.sub(r'<link rel="stylesheet" href="/catalog-layout.css[^\"]*">','',s)
  s=s.replace('</head>','<link rel="stylesheet" href="/catalog-layout.css"><link rel="stylesheet" href="/unified-layout.css"></head>')
  if path.name not in paths:s=s.replace('</body>',"<script>if(matchMedia('(max-width:760px)').matches)document.querySelector('.category-menu').open=false;</script></body>")
  (dist/path.name).write_text(s)
 (dist/'unified-layout.css').write_text(Path(__file__).with_name('unified-layout.css').read_text())
