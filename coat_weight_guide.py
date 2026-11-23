"""Add practical sampling guidance beside the existing woodfree A–D table."""

from html import escape

from design_update import replace_once


LANGUAGES = ('es-419', 'en', 'zh-Hant', 'ru', 'zh-Hans')
FINAT_METHODS = 'https://www.finat.com/documents/540/technical-handbook-2019-folder-low.pdf#page=3'
RECORD = {
    'es-419': (
        'Registro de la prueba',
        'Anote la opción A–D, la referencia del adhesivo y el gramaje aplicado (g/m²).',
        'Registre por separado el envase, la presión, la temperatura y el tiempo de reposo, junto con el agarre inicial y los bordes levantados.',
        'Métodos FINAT de gramaje, tack y adhesión',
    ),
    'en': (
        'Sample trial record',
        'Record the A–D option, adhesive grade and coat weight (g/m²).',
        'Record the package, pressure, temperature and dwell time separately from the initial tack and any edge lift observed.',
        'FINAT coat weight, tack and adhesion methods',
    ),
    'zh-Hant': (
        '試樣紀錄',
        '記下 A～D 組合、膠黏劑料號及塗膠量（g/m²）。',
        '另記包材、貼標壓力、溫度及靜置時間，再填入初黏、貼合與翹邊的觀察結果。',
        'FINAT 塗膠量、初黏與黏著測試方法',
    ),
    'ru': (
        'Запись испытания образца',
        'Укажите вариант A–D, марку клея и массу клеевого покрытия (г/м²).',
        'Отдельно запишите упаковку, давление, температуру и время выдержки. Зафиксируйте начальную липкость и отслоение краёв.',
        'Методы FINAT для массы покрытия, липкости и адгезии',
    ),
    'zh-Hans': (
        '试样记录',
        '记录 A～D 组合、胶黏剂料号和涂胶量（g/m²）。',
        '另记包材、贴标压力、温度和静置时间，再填写初粘、贴合及翘边的观察结果。',
        'FINAT 涂胶量、初粘与粘接测试方法',
    ),
}


def add_coat_weight_guides(dist, groups, copy):
    changed = set()
    for index, locale in enumerate(LANGUAGES):
        filename = groups['woodfree'][index]
        labels = copy[locale]['labels']
        record_title, construction, observations, reference = map(escape, RECORD[locale])
        choices = ''.join(
            f'<article><h3>{escape(labels[f"coat_{key}_title"])}</h3>'
            f'<p>{escape(labels[f"coat_{key}"])}</p></article>'
            for key in ('smooth', 'rough', 'special')
        )
        guide = escape(groups['guide'][index] + '#adhesives', quote=True)
        section = (
            '<section class="coat-guide" id="coat-weight">'
            f'<h2>{escape(labels["coat_title"])}</h2><p>{escape(labels["coat_intro"])}</p>'
            f'<div class="coat-choices">{choices}</div>'
            f'<div class="coat-record"><h3>{record_title}</h3>'
            f'<p>{construction}</p><p>{observations}</p></div>'
            f'<div class="toc"><a href="{guide}">{escape(labels["adhesive_guide"])}</a>'
            f'<a href="{FINAT_METHODS}">{reference}</a></div></section>'
        )
        path = dist / filename
        html = path.read_text(encoding='utf-8')
        html = replace_once(
            r'(<section id="compare"[^>]*>.*?</section>)',
            lambda match: match[1] + section,
            html,
        )
        css = '<link rel="stylesheet" href="/product-finder.css">'
        path.write_text(html.replace('</head>', css + '</head>', 1), encoding='utf-8')
        changed.add(filename)
    return changed
