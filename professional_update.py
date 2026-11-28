"""Align buyer-facing wording and canonical catalog URLs across five languages."""
from pathlib import Path
import re

CATALOG_URLS = {
    'materiales': 'materiales-autoadhesivos-bobinas-madre',
    'materials': 'self-adhesive-labelstock-jumbo-rolls',
    'catalog-zh': 'labelstock-jumbo-rolls-zh',
    'materials-ru': 'labelstock-jumbo-rolls-ru',
    'catalog-zh-cn': 'labelstock-jumbo-rolls-zh-cn',
}

HOMES = ('index.html', 'en.html', 'zh.html', 'ru.html', 'zh-cn.html')
REQUESTS = ('cotizacion-muestras.html', 'quote-sample.html', 'request-zh.html', 'request-ru.html', 'request-zh-cn.html')
HERO = (
    'Papeles y películas autoadhesivas en bobinas madre',
    'Self-adhesive paper and film in jumbo rolls',
    '紙類與薄膜不乾膠母卷',
    'Самоклеящиеся бумага и плёнка в джамбо-рулонах',
    '纸类与薄膜不干胶母卷',
)
BUYER_INTRO = (
    'Una bobina madre combina frontal, adhesivo y liner. Compare diez materiales y confirme la misma construcción al pedir muestras, cotizar y recibir el pedido.',
    'A labelstock jumbo roll combines facestock, adhesive and release liner. Compare ten materials and confirm the same construction for samples, quotes and delivery.',
    '不乾膠母卷由面材、感壓膠與離型底材組成。比較十類材料，索樣、報價與到貨時核對同一材料組合。',
    'Самоклеящийся материал состоит из лицевого слоя, клея и антиадгезионной подложки. Сравните десять материалов и сверяйте состав при запросе образца, расчёте цены и получении заказа.',
    '不干胶母卷由面材、压敏胶与离型底材组成。比较十类材料，索样、报价与到货时核对同一材料组合。',
)
REQUEST_INTRO = (
    'Indique el material o la aplicación y prepare los datos de prueba. Abra WhatsApp con el mensaje ya rellenado y pulse Enviar para contactar con RolloBase. También puede descargar la solicitud como respaldo.',
    'Describe the material or application and add trial details. Open the prepared WhatsApp message and press Send to contact RolloBase. You can also download the request as a backup.',
    '說明材料或標籤用途並填寫試樣條件。點開已帶入資料的 WhatsApp 訊息，再按傳送即可聯絡 RolloBase；也可下載需求單留存。',
    'Укажите материал или назначение этикетки и условия испытания. Откройте готовое сообщение в WhatsApp и нажмите «Отправить», чтобы связаться с RolloBase. Запрос также можно скачать.',
    '说明材料或标签用途并填写试样条件。打开已带入资料的 WhatsApp 消息，再按发送即可联系 RolloBase；也可下载需求单留存。',
)
FIELD_LABELS = (
    ('Empresa / nombre', 'Contacto (teléfono o WhatsApp)', 'Aplicación de la etiqueta', 'Enviar por WhatsApp', 'Se abrirá WhatsApp con su solicitud. Revise el mensaje y pulse Enviar; abrirlo no envía datos automáticamente.'),
    ('Company / name', 'Contact (phone or WhatsApp)', 'Label application', 'Send via WhatsApp', 'WhatsApp opens with your request. Review the message and press Send; opening it does not submit anything.'),
    ('公司／姓名', '聯絡方式（電話或 WhatsApp）', '標籤用途', '透過 WhatsApp 傳送', 'WhatsApp 會開啟已填好的訊息；請核對內容並按傳送，開啟頁面本身不會送出資料。'),
    ('Компания / имя', 'Контакт (телефон или WhatsApp)', 'Применение этикетки', 'Отправить через WhatsApp', 'WhatsApp откроет заполненное сообщение. Проверьте его и нажмите «Отправить»; само открытие ничего не отправляет.'),
    ('公司／姓名', '联系方式（电话或 WhatsApp）', '标签用途', '通过 WhatsApp 发送', 'WhatsApp 会打开已填好的消息；请核对内容并按发送，打开页面本身不会提交资料。'),
)
REQUEST_STEPS = (
    '1. Elija material y combinación · 2. Complete los datos · 3. Envíe por WhatsApp o descargue el respaldo',
    '1. Choose material and construction · 2. Add requirements · 3. Send via WhatsApp or download a backup',
    '1. 選材料與組合　2. 填寫需求　3. 透過 WhatsApp 傳送或下載留存',
    '1. Выберите материал · 2. Заполните данные · 3. Отправьте через WhatsApp или скачайте копию',
    '1. 选材料与组合　2. 填写需求　3. 通过 WhatsApp 发送或下载留存',
)
PHONE_NOTES = (
    'Si WhatsApp no está disponible, llame para acordar cómo compartir la solicitud descargada.',
    'If WhatsApp is unavailable, call to arrange how to share the downloaded request.',
    '若無法使用 WhatsApp，可電話聯絡業務，確認如何提供已下載的需求單。',
    'Если WhatsApp недоступен, позвоните и согласуйте передачу скачанного запроса.',
    '如无法使用 WhatsApp，可致电业务，确认如何提供已下载的需求单。',
)
DOWNLOAD_NOTES = (
    'Solicitud descargada como respaldo. Aún no se ha enviado; use WhatsApp o llame para compartirla.',
    'Request downloaded as a backup. It has not been sent; use WhatsApp or call to share it.',
    '需求單已下載留存，尚未送出。請使用 WhatsApp 傳送，或電話聯絡業務。',
    'Запрос скачан для сохранения. Он ещё не отправлен; передайте его через WhatsApp или позвоните.',
    '需求单已下载留存，尚未发送。请使用 WhatsApp 发送，或致电业务。',
)

def reorder_home_cards(html):
    match = re.search(r'(<section id="materials">.*?<div class="appgrid">)(.*?)(</div>)', html, re.S)
    if not match:
        raise ValueError('Homepage material grid not found')
    inner = match.group(2)
    cards = []
    while inner:
        if inner.startswith('<article class="site-photo-card'):
            end = inner.index('</article>') + len('</article>')
        elif inner.startswith('<a class="appcard"'):
            end = inner.index('</a>') + len('</a>')
        else:
            raise ValueError('Unexpected homepage card markup')
        cards.append(inner[:end])
        inner = inner[end:]
    if len(cards) != 10:
        raise ValueError(f'Expected ten homepage cards; found {len(cards)}')
    ordered = ''.join(cards[i] for i in (4, 5, 6, 7, 8, 9, 0, 1, 2, 3))
    return html[:match.start(2)] + ordered + html[match.end(2):]

def update_request(html, index):
    html, count = re.subn(r'(<h1>.*?</h1><p>).*?(</p>)', lambda m: m[1] + REQUEST_INTRO[index] + m[2], html, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Request introduction not found')
    html, count = re.subn(r'<p class="request-steps">.*?</p>', '<p class="request-steps">' + REQUEST_STEPS[index] + '</p>', html, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Request steps not found')
    html, count = re.subn(r'(<aside class="contact-panel">.*?<p>).*?(</p>)', lambda m: m[1] + PHONE_NOTES[index] + m[2], html, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Request phone note not found')
    html = re.sub(r'(id="request-status"[^>]*data-message=")[^"]+(" hidden)', lambda m: m[1] + DOWNLOAD_NOTES[index] + m[2], html, count=1)
    company, contact, application, button, note = FIELD_LABELS[index]
    start = '<form id="inquiry"'
    form_start = html.index(start)
    grid_start = html.index('<div class="fieldgrid">', form_start) + len('<div class="fieldgrid">')
    extra = ''.join(f'<label>{label}<input name="{name}" type="text"></label>' for label, name in ((company, 'company'), (contact, 'buyer_contact'), (application, 'application')))
    html = html[:grid_start] + extra + html[grid_start:]
    form_end = html.index('</form>', grid_start)
    button_at = html.index('<button class="button">', grid_start, form_end)
    cta = f'<a id="send-whatsapp" class="button whatsapp-inquiry" href="https://wa.me/8618588600270" target="_blank" rel="noopener noreferrer">{button} ↗</a><p class="whatsapp-note">{note}</p>'
    if index == 0:
        cta = (
            '<details class="sample-specs" hidden>'
            '<summary>Empresa y especificaciones opcionales</summary>'
            '<div class="fieldgrid"></div></details>' + cta
        )
    html = html[:button_at] + cta + html[button_at:]
    html = html.replace('<select name="material" required>', '<select name="material">', 1)
    return html

def replace_url_references(text, old, new):
    # Match an entire path component, including extensionless routes and query links.
    text = re.sub(r'(?<=/)' + re.escape(old) + r'\.html(?=["?#<])', new + '.html', text)
    text = re.sub(r'(?<=/)' + re.escape(old) + r'(?=["?#<])', new, text)
    return re.sub(r'(?<=href=")' + re.escape(old) + r'(?=\.html["?#])', new, text)

def apply_professional_update(dist):
    dist = Path(dist)
    for index, name in enumerate(HOMES):
        page = dist / name
        html = page.read_text(encoding='utf-8')
        html, count = re.subn(r'<h1>.*?</h1>', '<h1>' + HERO[index] + '</h1>', html, count=1, flags=re.S)
        if count != 1:
            raise ValueError(f'Homepage heading missing: {name}')
        html = reorder_home_cards(html)
        html, count = re.subn(r'(<section id="buyer-guides">.*?<p class="section-intro">).*?(</p>)', lambda m: m[1] + BUYER_INTRO[index] + m[2], html, count=1, flags=re.S)
        if count != 1:
            raise ValueError(f'Buyer introduction missing: {name}')
        html = re.sub(r'<section class="questions">.*?</section>', '', html, count=1, flags=re.S)
        html = re.sub(r'<section class="first-order-faq">.*?</section>', '', html, count=1, flags=re.S)
        html = html.replace('2026-11-24', '2026-11-25')
        page.write_text(html, encoding='utf-8')
    for index, name in enumerate(REQUESTS):
        page = dist / name
        html = update_request(page.read_text(encoding='utf-8'), index)
        html = html.replace('2026-11-24', '2026-11-25')
        script_version = '20261128-muestra' if index == 0 else '20261125-professional'
        html = re.sub(r'/buyer\.js(?:\?[^" ]+)?', '/buyer.js?v=' + script_version, html)
        if index == 0:
            html = re.sub(r'/unified-layout\.css(?:\?[^" ]+)?', '/unified-layout.css?v=20261128-muestra', html)
        html = html.replace('href="/unified-layout.css"', 'href="/unified-layout.css?v=20261125-professional"')
        page.write_text(html, encoding='utf-8')
    for page in dist.glob('*.html'):
        html = page.read_text(encoding='utf-8')
        for old, new in CATALOG_URLS.items():
            html = replace_url_references(html, old, new)
        if page.stem in CATALOG_URLS:
            html = html.replace('2026-11-24', '2026-11-25')
        page.write_text(html, encoding='utf-8')
    sitemap = dist / 'sitemap.xml'
    xml = sitemap.read_text(encoding='utf-8')
    for old, new in CATALOG_URLS.items():
        xml = replace_url_references(xml, old, new)
        (dist / (old + '.html')).rename(dist / (new + '.html'))
    changed = [dist / name for name in HOMES + REQUESTS]
    changed += [dist / (name + '.html') for name in CATALOG_URLS.values()]
    for page in changed:
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', page.read_text(encoding='utf-8'))
        if not canonical:
            raise ValueError(f'Canonical URL missing: {page.name}')
        xml = xml.replace('<loc>' + canonical[1] + '</loc><lastmod>2026-11-24</lastmod>', '<loc>' + canonical[1] + '</loc><lastmod>2026-11-25</lastmod>')
    sitemap.write_text(xml, encoding='utf-8')
