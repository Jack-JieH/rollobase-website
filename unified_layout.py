"""One shared catalogue shell for every locale and page."""
from pathlib import Path
from html import escape as e
from shutil import copyfile
import re
from catalog_layout import paths,langs,guides,homes

LANGUAGE_OPTIONS = {
    'es-419': ('es', 'ES', 'Español', 'Idioma'),
    'en': ('us', 'EN', 'English', 'Language'),
    'zh-Hant': ('tw', '繁中', '繁體中文', '語言'),
    'ru': ('ru', 'RU', 'Русский', 'Язык'),
    'zh-Hans': ('cn', '简中', '简体中文', '语言'),
}
LANGUAGE_LINK = re.compile(r'<a\b([^>]*)>.*?</a>', re.S)
LANGUAGE_BLOCK = re.compile(r'<div class="languages">.*?</div>', re.S)
LANGUAGE_DISMISS = """<script>
const languagePicker = document.querySelector('.language-picker');
document.addEventListener('click', (event) => {
    if (languagePicker.open && !languagePicker.contains(event.target)) {
        languagePicker.open = false;
    }
});
languagePicker.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && languagePicker.open) {
        languagePicker.open = false;
        languagePicker.querySelector('summary').focus();
    }
});
</script>"""

def language_flag(region):
    return f'<img class="language-flag" src="/flags/{region}.png" width="28" height="21" alt="">'

def language_picker(links, active_lang):
    def label_link(link):
        attributes = link[1]
        lang = re.search(r'\blang="([^"]+)"', attributes)[1]
        lang = 'es-419' if lang == 'es' else lang
        region, _, name, _ = LANGUAGE_OPTIONS[lang]
        return f'<a{attributes}>{language_flag(region)}<span>{e(name)}</span></a>'

    region, code, name, label = LANGUAGE_OPTIONS[active_lang]
    options = ''.join(label_link(link) for link in LANGUAGE_LINK.finditer(links))
    return (
        '<details class="languages language-picker">'
        f'<summary aria-label="{e(label)}: {e(name)} ({e(code)})">'
        f'{language_flag(region)}<span>{e(code)}</span>'
        '<span class="language-chevron" aria-hidden="true"></span></summary>'
        f'<div class="language-options">{options}</div></details>'
    )

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
  original_langs=LANGUAGE_BLOCK.search(s) or LANGUAGE_BLOCK.search(header)
  header=LANGUAGE_BLOCK.sub(lambda _:language_picker(original_langs[0],lang),header,count=1)
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
  s=s.replace('</head>','<link rel="stylesheet" href="/catalog-layout.css"><link rel="stylesheet" href="/unified-layout.css?v=20261128"></head>')
  if path.name not in paths:s=s.replace('</body>',"<script>if(matchMedia('(max-width:760px)').matches)document.querySelector('.category-menu').open=false;</script></body>")
  phone_labels=['Llamar a RolloBase','Call RolloBase','電話聯絡 RolloBase','Позвонить в RolloBase','电话联系 RolloBase']
  wa_labels=['Contactar por WhatsApp','Contact on WhatsApp','透過 WhatsApp 聯絡','Связаться через WhatsApp','通过 WhatsApp 联系']
  phone_icon='<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 3H4a1 1 0 0 0-1 1c0 9.4 7.6 17 17 17a1 1 0 0 0 1-1v-3l-5-2-2 2a15 15 0 0 1-7-7l2-2-2-5Z"/></svg>'
  wa_icon='<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M20.5 11.7a8.5 8.5 0 0 1-12.6 7.5L3 20.5l1.3-4.8A8.5 8.5 0 1 1 20.5 11.7Z"/><path d="m8.1 7.4-1 .6c-.7.5.4 3.4 2.5 5.4 2 2 4.5 2.9 5.2 2.2l.7-1.3-2.5-1.2-.8 1c-1.5-.6-2.7-1.8-3.3-3.3l.8-.8-1.6-2.6Z"/></svg>'
  dock='<div class="contact-icons" role="group" aria-label="'+e(['Contacto','Contact','聯絡方式','Контакты','联系方式'][i])+'"><a class="contact-whatsapp" href="https://wa.me/8618588600270" target="_blank" rel="noopener noreferrer" aria-label="'+wa_labels[i]+'" title="'+wa_labels[i]+'">'+wa_icon+'</a><a class="contact-phone" href="tel:+8618588600270" aria-label="'+phone_labels[i]+'" title="'+phone_labels[i]+'">'+phone_icon+'</a></div>'
  s=s.replace('</body>',dock+LANGUAGE_DISMISS+'</body>')
  (dist/path.name).write_text(s)
 (dist/'unified-layout.css').write_text(Path(__file__).with_name('unified-layout.css').read_text())
 flags=dist/'flags'
 flags.mkdir(exist_ok=True)
 # Country flag images from https://flagcdn.com/.
 for region, _, _, _ in LANGUAGE_OPTIONS.values():
  copyfile(Path(__file__).with_name(f'flag-{region}.png'), flags/f'{region}.png')
