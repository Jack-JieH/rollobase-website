"""Shared, reviewed five-language presentation and sales contact details."""
from html import escape, unescape
import re

PHONE = '+8618588600270'
DISPLAY_PHONE = '+86 185 8860 0270'

# Locale order is shared with seo_update: ES, EN, zh-Hant, RU, zh-Hans.
COPY = {
 'home_title':['Bobinas madre autoadhesivas para etiquetas','Self-adhesive master rolls for label converters','自黏標籤母卷，從選材到索樣','Самоклеящиеся материалы в джамбо-рулонах','不干胶标签母卷，从选材到索样'],
 'audience':['Para impresores, convertidores y distribuidores','For printers, converters and distributors','供標籤印刷廠、加工廠與經銷商選材','Для типографий, переработчиков и дистрибьюторов','供标签印刷厂、加工厂与经销商选材'],
 'intro':['Material autoadhesivo sin imprimir en bobinas jumbo. Compare papel y película por aplicación, confirme frontal, adhesivo y liner, y prepare una muestra o cotización con las medidas de su equipo.','Unprinted self-adhesive labelstock in jumbo rolls. Choose paper or film by application, check facestock, adhesive and liner, then prepare a sample or quote brief with your machine dimensions.','依成品用途比較紙類與薄膜母卷，確認面材、膠黏劑與離型底材，再帶著設備尺寸索樣或詢價。供後續印刷、分條與模切的未印刷自黏卷材。','Материалы без печати для производства этикеток. Выберите бумагу или плёнку по применению, уточните лицевой материал, клей и подложку, затем подготовьте запрос образца или цены с размерами для вашего оборудования.','按成品用途比较纸类与薄膜母卷，确认面材、胶粘剂和离型底材，再带着设备尺寸索样或询价。供后续印刷、分切与模切的未印刷不干胶卷材。'],
 'catalog':['Ver materiales','Browse materials','瀏覽材料','Каталог материалов','浏览材料'],
 'sample':['Solicitar muestra','Request a sample','索取樣品','Запросить образец','索取样品'],
 'quote':['Solicitar cotización','Request a quote','索取報價','Запросить цену','索取报价'],
 'use_heading':['Empiece por la aplicación de su etiqueta','Start with your label application','先看標籤用途，再選材料','Начните с применения этикетки','先看标签用途，再选材料'],
 'use_intro':['Elija el envase y las condiciones de uso. En cada producto encontrará la estructura, los datos a confirmar y los accesos a muestra y cotización.','Choose the packaging and service conditions. Each product page brings together construction, specifications to confirm, and sample and quote links.','從包裝、印刷與使用環境開始。各產品頁可查看結構、比較規格，並直接準備索樣或報價。','Выберите упаковку и условия эксплуатации. На странице материала представлены состав, параметры для согласования и ссылки на запрос образца и цены.','从包装、印刷和使用环境开始。各产品页可查看结构、比较规格，并直接准备索样或报价。'],
 'coated_use':['Etiquetas a color para envases secos','Color labels on dry packaging','乾燥包裝的彩色標籤','Цветные этикетки для сухой упаковки','干燥包装的彩色标签'],
 'thermal_use':['Logística, códigos de barras y balanzas','Shipping barcodes and scale labels','物流條碼與秤重標籤','Логистика, штрихкоды и весы','物流条码与称重标签'],
 'bopp_use':['Envases con exposición a humedad','Containers exposed to moisture','潮濕環境中的容器標籤','Упаковка в условиях влажности','潮湿环境中的容器标签'],
 'pe_use':['Etiquetas para envases flexibles','Labels on squeezable containers','可擠壓瓶身標籤','Этикетки для мягких флаконов','可挤压瓶身标签'],
 'pet_use':['Identificación de equipos y activos','Equipment and asset identification','設備與資產識別','Маркировка оборудования и активов','设备与资产识别'],
 'woodfree_use':['Impresión en papel sin estucar','Printing on uncoated paper','未塗佈紙面印刷','Печать на немелованной бумаге','未涂布纸面印刷'],
 'woodfree_name':['Papel no estucado · A–D','Woodfree paper · A–D','模造紙 · A～D','Немелованная бумага · A–D','书写纸 · A～D'],
 'woodfree_note':['Compare frontal, hot melt y glassine en una sola tabla y elija su muestra.','Compare facestock, hot melt and glassine in one table, then choose a sample.','同表比較面材、熱熔膠與格拉辛底紙，直接選擇索樣組合。','Сравните лицевой материал, термоклей и глассин в одной таблице и выберите образец.','同表比较面材、热熔胶与格拉辛底纸，直接选择索样组合。'],
 'spec_heading':['Ficha para comparar y cotizar','Specifications for comparison and quotation','規格比較與詢價資料','Параметры для сравнения и расчёта цены','规格比较与询价资料'],
 'face':['Frontal y gramaje / espesor','Facestock and grammage / thickness','面材與克重／厚度','Лицевой материал: плотность / толщина','面材与克重／厚度'],
 'adhesive':['Adhesivo y gramaje de recubrimiento','Adhesive and coat weight','膠種與塗膠量','Клей и масса покрытия','胶型与涂胶量'],
 'liner':['Liner y gramaje / espesor','Release liner and grammage / thickness','離型底材與克重／厚度','Подложка: плотность / толщина','离型底材与克重／厚度'],
 'dimensions':['Medidas y sentido de bobinado','Roll dimensions and winding direction','母卷尺寸與捲繞方向','Размеры и направление намотки','母卷尺寸与收卷方向'],
 'tests':['Ensayo y documentación técnica','Trial conditions and technical documents','測試條件與技術文件','Испытания и технические документы','测试条件与技术文件'],
 'face_pending':['Confirme el valor y la tolerancia por referencia.','Confirm value and tolerance for the specific SKU.','數值與允差依正式料號確認。','Уточните значение и допуск по конкретному артикулу.','数值与公差按正式料号确认。'],
 'wood_face':['60 o 70 g/m²; consulte la combinación A–D.','60 or 70 g/m²; see the A–D construction.','60 或 70 g/m²，依 A～D 組合對照。','60 или 70 г/м² — по варианту A–D.','60 或 70 g/m²，按 A～D 组合对照。'],
 'wood_adh':['Hot melt: 14 o 20 g/m² según A–D. Confirme la formulación y las temperaturas de aplicación y servicio.','Hot melt: 14 or 20 g/m² according to A–D. Confirm the grade, application temperature and service conditions.','熱熔膠 14 或 20 g/m²，依 A～D 組合。膠配方、貼標溫度與使用條件需確認。','Термоклей: 14 или 20 г/м² по варианту A–D. Уточните состав, температуру нанесения и условия эксплуатации.','热熔胶 14 或 20 g/m²，按 A～D 组合。胶配方、贴标温度与使用条件需确认。'],
 'adh_pending':['Especifique la formulación, el gramaje y el envase. Confirme temperaturas de aplicación y servicio antes de aprobar.','Specify the grade, coat weight and application surface. Confirm application and service temperatures before approval.','指定膠配方、塗膠量與被貼物，並核對貼標及使用溫度；數值待確認。','Укажите состав, массу покрытия и поверхность. До согласования уточните температуры нанесения и эксплуатации.','指定胶配方、涂胶量与被贴物，并核对贴标及使用温度；数值待确认。'],
 'wood_liner':['Glassine: 50 o 60 g/m² según A–D. Confirme fuerza de desprendimiento y tolerancias.','Glassine: 50 or 60 g/m² according to A–D. Confirm release force and tolerances.','格拉辛底紙 50 或 60 g/m²，依 A～D 組合；離型力及允差待確認。','Глассин: 50 или 60 г/м² по варианту A–D. Уточните усилие отделения и допуски.','格拉辛底纸 50 或 60 g/m²，按 A～D 组合；离型力及公差待确认。'],
 'liner_pending':['Confirme tipo, gramaje o espesor y fuerza de desprendimiento. Valide troquelado y dispensación en su equipo.','Confirm type, grammage or thickness, and release force. Validate die-cutting and dispensing on your equipment.','確認底材種類、克重或厚度及離型力，並以實際設備驗證模切與剝標。','Уточните тип, плотность или толщину и усилие отделения. Проверьте высечку и подачу на своём оборудовании.','确认底材种类、克重或厚度及离型力，并用实际设备验证模切与剥标。'],
 'roll_details':['Ancho útil (mm), longitud (m), diámetro interior del núcleo (mm), diámetro exterior máximo (mm) y sentido de bobinado. Medidas disponibles y tolerancias por confirmar.','Usable width (mm), length (m), core ID (mm), maximum roll OD (mm), and winding direction. Available sizes and tolerances require confirmation.','可用幅寬（mm）、卷長（m）、紙芯內徑（mm）、最大卷外徑（mm）與捲繞方向。可供尺寸及允差需逐項確認。','Полезная ширина (мм), длина (м), внутренний диаметр втулки (мм), максимальный наружный диаметр (мм) и направление намотки. Доступные размеры и допуски согласуются.','有效门幅（mm）、卷长（m）、纸芯内径（mm）、最大卷径（mm）与收卷方向。可供尺寸及公差需逐项确认。'],
 'test_details':['Registre equipo, tinta o ribbon, superficie, temperaturas y criterio de aceptación. Solicite referencia, versión de TDS y resultados correspondientes al material y lote.','Record machine, ink or ribbon, application surface, temperatures and acceptance criteria. Request SKU, TDS revision and results for the specific material and batch.','記錄設備、油墨或碳帶、被貼物、溫度與驗收條件；索取正式料號、TDS 版本及對應材料和批次的測試結果。','Запишите оборудование, краски или риббон, поверхность, температуры и критерии приёмки. Запросите артикул, версию TDS и результаты для материала и партии.','记录设备、油墨或碳带、被贴物、温度与验收条件；索取正式料号、TDS 版本及对应材料和批次的测试结果。'],
 'contact':['Contacto comercial','Sales contact','業務聯絡','Связь с отделом продаж','业务联系'],
 'call':['Llamar','Call','撥打電話','Позвонить','拨打电话'],
 'contact_note':['Descargue su solicitud y llame para coordinar cómo compartirla.','Download your brief, then call to arrange how to share it.','下載需求單後，請電話確認資料交付方式。','Скачайте запрос и позвоните, чтобы согласовать способ его передачи.','下载需求单后，请电话确认资料交付方式。'],
 'form_intro':['Elija el material, indique las condiciones de prueba y descargue su solicitud. Llame al contacto comercial para coordinar cómo compartirla. La descarga no envía solicitudes ni confirma muestras.','Choose a material, add the trial requirements and download your brief. Call the sales contact to arrange how to share it. Downloading does not submit a request or confirm a sample.','選擇材料、填寫試樣條件並下載需求單，再電話聯絡業務確認交付方式。下載不會自動送出詢價或確認樣品。','Выберите материал, укажите условия испытания и скачайте запрос. Позвоните в отдел продаж, чтобы согласовать его передачу. Скачивание не отправляет заявку и не подтверждает выдачу образца.','选择材料、填写试样条件并下载需求单，再电话联系业务确认交付方式。下载不会自动提交询价或确认样品。'],
 'steps':['1. Elija material y combinación · 2. Complete los datos · 3. Descargue y contacte','1. Choose material and construction · 2. Add requirements · 3. Download and contact','1. 選材料與組合　2. 填寫需求　3. 下載並聯絡','1. Выберите материал · 2. Заполните данные · 3. Скачайте и свяжитесь с нами','1. 选材料与组合　2. 填写需求　3. 下载并联系'],
 'winding':['Sentido de bobinado','Winding direction','捲繞方向','Направление намотки','收卷方向'],
 'unspecified':['Por confirmar','To be confirmed','待確認','Уточнить','待确认'],
 'outside':['Frontal imprimible hacia fuera','Printable face out','印刷面朝外','Печатная сторона наружу','印刷面朝外'],
 'inside':['Frontal imprimible hacia dentro','Printable face in','印刷面朝內','Печатная сторона внутрь','印刷面朝内'],
 'drawing':['Según plano / muestra de referencia','Per drawing / reference sample','依圖面／參考樣品確認','По чертежу / образцу','按图纸／参考样品确认'],
 'download_status':['Solicitud generada. Revise las descargas y llame para coordinar cómo compartirla. No se ha enviado una solicitud automáticamente.','Brief generated. Check your downloads and call to arrange sharing it. No request has been sent automatically.','需求單已產生，請查看下載項目，再電話確認資料交付方式；尚未自動送出詢價或索樣。','Запрос сформирован. Проверьте загрузки и позвоните для согласования передачи. Заявка автоматически не отправлялась.','需求单已生成，请查看下载项目，再电话确认资料交付方式；尚未自动提交询价或索样。'],
}


def replace_once(pattern, replacement, source):
    result, count = re.subn(pattern, lambda m:replacement(m) if callable(replacement) else replacement, source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Missing expected page section: '+pattern)
    return result


BOPP_FIELDS = (
    ('bopp_face', ['Acabado BOPP', 'BOPP finish', 'BOPP 面材外觀', 'Вариант плёнки BOPP', 'BOPP 面材外观'], (
        ('white', ['Blanco', 'White', '白色', 'Белая', '白色']),
        ('clear', ['Transparente', 'Clear', '透明', 'Прозрачная', '透明']),
        ('compare', ['Comparar blanco y transparente', 'Compare white and clear', '比較白色與透明', 'Сравнить белую и прозрачную', '比较白色与透明']),
    )),
    ('bopp_container', ['Material del envase (por ejemplo, PET o vidrio)', 'Container material (e.g. PET or glass)', '容器材質（例如 PET 或玻璃）', 'Материал тары (например, ПЭТ или стекло)', '容器材质（例如 PET 或玻璃）'], ()),
    ('bopp_surface', ['Estado del envase al etiquetar', 'Container condition at application', '貼標當下的容器狀態', 'Состояние тары при этикетировании', '贴标时容器的状态'], (
        ('dry', ['Seco', 'Dry', '乾燥', 'Сухая', '干燥']),
        ('condensation', ['Con condensación', 'With condensation', '有結露', 'С конденсатом', '有冷凝水']),
        ('compare', ['Comparar ambas condiciones', 'Compare both conditions', '比較兩種狀態', 'Сравнить оба условия', '比较两种状态']),
    )),
)


def bopp_fields(index):
    fields = []
    for name, labels, choices in BOPP_FIELDS:
        attrs = f'name="{name}" data-bopp-field disabled'
        if choices:
            options = (('', COPY['unspecified']), *choices)
            control = f'<select {attrs}>'+''.join(
                f'<option value="{value}">{escape(text[index])}</option>' for value,text in options
            )+'</select>'
        else:
            control = f'<input {attrs} type="text">'
        fields.append(f'<label hidden>{escape(labels[index])}{control}</label>')
    return ''.join(fields)


def apply_design(dist, groups):
    for key, paths in groups.items():
        for i, path in enumerate(paths):
            t = lambda name:COPY[name][i]
            request = groups['request'][i]
            html = (dist/path).read_text()
            if key=='home':
                hero = '<div class="hero-copy"><p class="eyebrow">'+escape(t('audience'))+'</p><h1>'+escape(t('home_title'))+'</h1><p>'+escape(t('intro'))+'</p>'
                hero += '<div class="hero-actions"><a class="button" href="'+groups['catalog'][i]+'">'+escape(t('catalog'))+'</a><a class="button button-outline" href="'+request+'?mode=sample">'+escape(t('sample'))+'</a><a class="hero-quote" href="'+request+'?mode=quote">'+escape(t('quote'))+' →</a></div></div>'
                html = replace_once(r'<div class="hero-copy">.*?</div>',hero,html)
                html = replace_once(r'(<section id="materials"><div class="sectionhead"><h2>).*?(</h2>)',lambda m:m[1]+escape(t('use_heading'))+m[2],html)
                html = replace_once(r'(<section id="materials">.*?</div>)(<div class="appgrid">)',lambda m:m[1]+'<p class="section-intro">'+escape(t('use_intro'))+'</p>'+m[2],html)
                section = re.search(r'<section id="materials">.*?</section>',html,re.S)[0]
                for product in ('coated','thermal','bopp','pe','pet'):
                    target = re.escape(groups[product][i])
                    section = replace_once(r'(<a class="appcard" href="'+target+r'"><span>).*?(</span>)',lambda m:m[1]+escape(t(product+'_use'))+m[2],section)
                wood_card = '<a class="appcard" href="'+groups['woodfree'][i]+'#compare"><span>'+escape(t('woodfree_use'))+'</span><h3>'+escape(t('woodfree_name'))+'</h3><p>'+escape(t('woodfree_note'))+'</p><b aria-hidden="true">↗</b></a>'
                section = section.replace('</div></section>',wood_card+'</div></section>',1)
                html = replace_once(r'<section id="materials">.*?</section>',section,html)
                hub = re.search(r'<section id="buyer-guides">.*?</section>',html,re.S)[0]
                html = html.replace(hub,'',1)
                html = replace_once(r'(<section class="feature">.*?</section>)',lambda m:m[1]+hub,html)
            if key=='catalog':
                for product in ('coated','thermal','bopp','pe','pet','woodfree'):
                    html = replace_once(r'(<a class="appcard"[^>]*href="'+re.escape(groups[product][i])+r'"><span>).*?(</span>)',lambda m:m[1]+escape(t(product+'_use'))+m[2],html)
            if key in ('coated','thermal','bopp','pe','pet','woodfree'):
                html = replace_once(r'(<section class="buy-head"><div>)(<h1>)',lambda m:m[1]+'<p class="eyebrow">'+escape(t(key+'_use'))+'</p>'+m[2],html)
                name = unescape(re.search(r'<h1>(.*?)</h1>',html,re.S)[1])
                unit = 'g/m²' if key in ('coated','thermal','woodfree') else 'μm'
                face = name+' · '+(t('wood_face') if key=='woodfree' else unit+'. '+t('face_pending'))
                rows = [('face',face),('adhesive',t('wood_adh' if key=='woodfree' else 'adh_pending')),('liner',t('wood_liner' if key=='woodfree' else 'liner_pending')),('dimensions',t('roll_details')),('tests',t('test_details'))]
                specs = '<section class="product-specs"><h2>'+escape(t('spec_heading'))+'</h2><dl class="spec-table">'+''.join('<dt><span class="spec-number">'+str(n)+'</span>'+escape(t(label))+'</dt><dd>'+escape(value)+'</dd>' for n,(label,value) in enumerate(rows,1))+'</dl>'
                html = replace_once(r'<section><h2>[^<]*</h2><dl class="spec-table">.*?</dl>',specs,html)
                for kind,label in [('sample','sample'),('quote','quote')]:
                    target = request+'?material='+key+'&amp;mode='+kind+'&amp;option='
                    # The top product actions are independent of the A–D table controls.
                    html = replace_once(r'(<a class="buy-link" href="'+re.escape(target)+r'">).*?(</a>)',lambda m:m[1]+escape(t(label))+' →'+m[2],html)
            if key=='request':
                html = replace_once(r'(<section><h1>.*?</h1>)<p>.*?</p>',lambda m:m[1]+'<p>'+escape(t('form_intro'))+'</p><p class="request-steps">'+escape(t('steps'))+'</p>',html)
                html = html.replace('<form id="inquiry">','<form id="inquiry" data-contact="'+escape(t('contact')+': '+DISPLAY_PHONE,quote=True)+'">',1)
                html = html.replace('<select name="material">','<select name="material" required>',1)
                html = replace_once(r'(<label>[^<]*<select name="option">.*?</select></label>)',lambda m:m[1]+bopp_fields(i),html)
                winding = '<label>'+escape(t('winding'))+'<select name="winding">'+''.join('<option value="'+value+'">'+escape(t(label))+'</option>' for value,label in [('', 'unspecified'),('outside','outside'),('inside','inside'),('drawing','drawing')])+'</select></label>'
                html = replace_once(r'(<label>[^<]*<input name="core"[^>]*></label>)',lambda m:m[1]+winding,html)
                status = '<p id="request-status" class="request-status" role="status" aria-live="polite" data-message="'+escape(t('download_status'),quote=True)+'" hidden></p>'
                html = html.replace('</form>',status+'</form>',1)
                contact = '<aside class="contact-panel"><h2>'+escape(t('contact'))+'</h2><a class="button" href="tel:'+PHONE+'">'+escape(t('call'))+' '+DISPLAY_PHONE+'</a><p>'+escape(t('contact_note'))+'</p></aside>'
                html = html.replace('</form>','</form>'+contact,1)
            contact = '<div class="footer-contact"><strong>'+escape(t('contact'))+'</strong><a href="tel:'+PHONE+'">'+DISPLAY_PHONE+'</a></div>'
            html = html.replace('</footer>',contact+'</footer>',1)
            html = html.replace('style.css?v=20261119-five','style.css?v=20261119-latam').replace('src="buyer.js"','src="buyer.js?v=20261122-bopp"')
            (dist/path).write_text(html)
