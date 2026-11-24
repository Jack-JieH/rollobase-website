"""Eight confirmed roll families, original sales copy and attribution-free owned media."""
from pathlib import Path
from html import escape as e
import json,re
from purchasing import routes
from russian import RU_ROUTES
from brand_contact import BRAND_FILES
from site_photos import photo_html

LANGS=['es-419','en','zh-Hant','ru','zh-Hans']
SUFFIX=['es','en','zh','ru','zh-cn']
# Localized names, uses, construction and a practical sample check; no unconfirmed specifications.
PRODUCTS={
'color-thermal': {'photo':'jumbo-color-thermal','family':'paper','use':'logistics','rows':[
['Papel térmico de color','Para distinguir rutas, lotes o categorías mediante el color de la etiqueta.','Papel térmico de color, adhesivo sensible a la presión y liner. La impresión térmica directa no requiere ribbon.','Pruebe el contraste y la lectura del código sobre el color elegido con su impresora.'],
['Coloured direct thermal paper','Use colour to distinguish shipping routes, batches or product groups.','Coloured thermal paper, pressure-sensitive adhesive and release liner. Direct thermal printing needs no ribbon.','Test barcode contrast and scanning on the chosen colour with your printer.'],
['彩色熱感紙母卷','利用標籤底色區分配送路線、批次或商品類別，方便現場辨識。','由彩色熱感面紙、感壓膠與離型底紙構成。採直熱列印時不需碳帶。','先選底色，再用實際印表機測試文字對比與條碼掃讀。'],
['Цветная термобумага','Цвет помогает различать маршруты доставки, партии и группы товаров.','Цветная термобумага, самоклеящийся слой и антиадгезионная подложка. Прямая термопечать не требует риббона.','Проверьте контраст и считывание штрихкода на выбранном цвете с вашим принтером.'],
['彩色热敏纸母卷','利用标签底色区分配送路线、批次或商品类别，方便现场识别。','由彩色热敏面纸、压敏胶和离型底纸构成。采用直接热敏打印时不需要碳带。','先选底色，再用实际打印机测试文字对比度和条码扫描。']]},
'color-coated': {'photo':'jumbo-color-coated','family':'paper','use':'print','rows':[
['Papel estucado de color','Para etiquetas de identificación, clasificación y promociones con un fondo de color.','Frontal de papel estucado de color, adhesivo y liner. Elija la tinta o el ribbon según el proceso de impresión.','Compare el color bajo la iluminación de uso y pruebe la adherencia de la tinta y el roce.'],
['Coloured coated paper','For identification, sorting and promotional labels with a coloured background.','Coloured coated paper facestock, adhesive and release liner. Match the ink or ribbon to your printing process.','Check the colour under the intended lighting, then test ink adhesion and rub resistance.'],
['彩色銅版紙母卷','適合分類識別、商品標示與促銷標籤，以底色協助區分不同資訊。','由彩色塗佈紙面材、感壓膠與離型底紙構成。油墨或碳帶須配合印刷方式選擇。','在實際光線下確認色樣，再試印檢查油墨附著與耐摩擦表現。'],
['Цветная мелованная бумага','Для маркировки, сортировки и промоэтикеток с цветным фоном.','Цветная мелованная бумага, клеевой слой и антиадгезионная подложка. Краску или риббон подбирают под способ печати.','Оцените цвет при рабочем освещении, затем проверьте адгезию краски и стойкость к истиранию.'],
['彩色铜版纸母卷','适合分类识别、商品标示和促销标签，以底色协助区分不同信息。','由彩色涂布纸面材、压敏胶和离型底纸构成。油墨或碳带须配合印刷方式选择。','在实际光线下确认色样，再试印检查油墨附着和耐摩擦表现。']]},
'synthetic-paper': {'photo':'jumbo-synthetic','family':'film','use':'print','rows':[
['Papel sintético autoadhesivo','Para etiquetas donde interesa una apariencia de papel con un frontal de película.','Frontal sintético, adhesivo y liner. La composición y el tratamiento superficial se eligen según la impresión y el uso.','Pruebe impresión, troquelado y adhesión sobre el envase. Si habrá humedad, incluya esa condición en la prueba.'],
['Self-adhesive synthetic paper','For labels that need a paper-like appearance with a film-based facestock.','Synthetic facestock, adhesive and release liner. Composition and surface treatment depend on the printing process and application.','Trial printing, die-cutting and adhesion on the actual packaging. Include moisture exposure if relevant.'],
['合成紙不乾膠母卷','需要紙張外觀、同時考慮薄膜面材的標籤，可從合成紙開始試樣。','由合成面材、感壓膠與離型底材構成。面材組成及表面處理依印刷與使用條件選擇。','先試印、模切及實物貼標；若會接觸水氣，將潮濕條件一併納入測試。'],
['Самоклеящаяся синтетическая бумага','Для этикеток с внешним видом бумаги и лицевым слоем на основе плёнки.','Синтетический лицевой слой, клей и подложка. Состав и обработку поверхности подбирают под печать и применение.','Проверьте печать, высечку и приклеивание к упаковке. При работе во влажной среде включите её в испытания.'],
['合成纸不干胶母卷','需要纸张外观、同时考虑薄膜面材的标签，可从合成纸开始试样。','由合成面材、压敏胶和离型底材构成。面材组成及表面处理按印刷和使用条件选择。','先试印、模切和实物贴标；若会接触水汽，将潮湿条件一并纳入测试。']]},
'release-paper': {'photo':'release-liner','family':'liner','use':'converting','rows':[
['Papel siliconado de soporte','Soporte para recubrimiento, laminación y conversión de materiales autoadhesivos.','Papel base con tratamiento antiadherente. Se suministra como liner, sin frontal de etiqueta ni adhesivo añadido.','Indique el adhesivo y el proceso. Pruebe el desprendimiento, la estabilidad del soporte y el dispensado.'],
['Release paper','A release backing for adhesive coating, laminating and labelstock converting.','Base paper with a release coating. Supplied as a liner, without a label facestock or added adhesive layer.','Tell us the adhesive and converting process. Test release behaviour, liner stability and dispensing.'],
['離型紙卷','用於塗膠、貼合及不乾膠材料加工，承載膠層並協助後續剝離。','由原紙與離型處理層構成。此產品為單獨底材，不包含標籤面材與膠層。','請說明配合的膠種與加工方式，再測試離型力、底紙穩定性及剝標表現。'],
['Антиадгезионная бумага','Подложка для нанесения клея, ламинирования и переработки самоклеящихся материалов.','Бумага-основа с антиадгезионным покрытием. Поставляется отдельно, без лицевого слоя этикетки и клея.','Укажите клей и процесс переработки. Проверьте отделение, стабильность подложки и подачу этикеток.'],
['离型纸卷','用于涂胶、复合和不干胶材料加工，承载胶层并协助后续剥离。','由原纸和离型处理层构成。此产品为单独底材，不包含标签面材和胶层。','请说明配合的胶型和加工方式，再测试离型力、底纸稳定性和剥标表现。']]}
}
COPY=[
 dict(about='Somos RolloBase',company='Fabricamos materiales autoadhesivos en bobinas madre para impresores, convertidores y distribuidores. Suministramos papel térmico y estucado, sus versiones de color, PET, BOPP, papel sintético y papel siliconado de soporte.',approach='Cuéntenos dónde se pegará la etiqueta y cómo la va a imprimir. A partir de esa información podemos revisar el frontal, el adhesivo y el liner. La muestra le permite comprobar la combinación en su equipo antes de decidir el pedido.',hero='Bobinas autoadhesivas para su próxima producción',intro='Papel o película, blanco, transparente o de color. Encuentre el material para su etiqueta y prepare una muestra para probarla en su línea.',catalog='Todos los materiales',structure='Cómo está compuesto',trial='Qué probar con la muestra',sample='Solicitar muestra',view='Ver producto',liner='Papel siliconado',converting='Recubrimiento y conversión',workflow='De la primera muestra al siguiente pedido',steps=[['Elegir el material','Empecemos por el envase, la impresión y las condiciones de uso.'],['Ajustar el formato','Indique ancho, longitud, núcleo y sentido de bobinado para revisar el formato de su equipo.'],['Probar antes de producir','Compruebe impresión, corte y adhesión con la muestra en condiciones reales.'],['Preparar el pedido','Deje por escrito la combinación aprobada y los documentos necesarios para su destino.']],faq='Antes de su primer pedido',qas=[['¿Qué necesitan para cotizar?','Indíquenos material, adhesivo, liner, medidas, núcleo, cantidad y país de destino. Si aún no tiene una especificación, empiece por el uso de la etiqueta.'],['¿De qué color es el liner?','El color depende de la combinación elegida. Confírmelo con la muestra; el color por sí solo no identifica sus propiedades.'],['¿Puedo pedir el ancho para mi máquina?','Envíenos el ancho útil, diámetro del núcleo, diámetro exterior máximo y sentido de bobinado. Revisaremos la viabilidad antes de cotizar.'],['¿Cuándo puede salir el primer pedido?','La fecha se confirma con la especificación, la cantidad y la aprobación de la muestra. Consúltenos su fecha requerida al enviar la solicitud.'],['¿Cómo consulto ribbons y equipos?','En la guía de impresión encontrará ribbons de cera, mixtos y de resina, además de equipos de aplicación. Indique el modelo y el uso para consultar compatibilidad y disponibilidad.']],more='Conozca RolloBase'),
 dict(about='We are RolloBase',company='We manufacture self-adhesive master-roll materials for printers, converters and distributors. Our range includes thermal and coated paper, coloured versions of both, PET, BOPP, synthetic paper and release paper.',approach='Tell us what the label will stick to and how you plan to print it. That gives us a starting point for the facestock, adhesive and liner. A sample lets you check the combination on your own equipment before placing an order.',hero='Labelstock for your next production run',intro='Paper or film, white, clear or coloured. Find the material for your label and prepare a sample to trial on your line.',catalog='All materials',structure='Material construction',trial='What to check with a sample',sample='Request a sample',view='View product',liner='Release paper',converting='Coating and converting',workflow='From the first sample to the next order',steps=[['Choose the material','Start with the packaging, printing process and service conditions.'],['Match the roll format','Share the width, length, core and winding direction your equipment needs.'],['Trial before production','Check printing, cutting and adhesion under actual conditions.'],['Prepare the order','Record the approved construction and the documents needed for your destination.']],faq='Before your first order',qas=[['What do you need for a quote?','Tell us the material, adhesive, liner, roll dimensions, core, quantity and destination country. If you do not yet have a specification, start with the label application.'],['What colour is the liner?','It depends on the construction you choose. Confirm it with the sample; colour alone does not describe the liner’s performance.'],['Can I request a width for my machine?','Send the usable width, core diameter, maximum roll diameter and winding direction. We will review feasibility before quoting.'],['When can the first order ship?','The date is confirmed once the specification, quantity and sample approval are settled. Include your required date in the request.'],['How do I enquire about ribbons and equipment?','Our printing guide covers wax, wax-resin and resin ribbons, plus label application equipment. Share the model and application to discuss compatibility and availability.']],more='About RolloBase'),
 dict(about='關於 RolloBase',company='RolloBase 專注製造不乾膠母卷材料，服務標籤印刷廠、加工廠與經銷商。我們供應熱感紙、銅版紙及其彩色系列，以及 PET、BOPP、合成紙和離型紙。',approach='選材料時，我們先了解標籤貼在哪裡、怎麼印刷，以及使用環境，再討論面材、膠與底材的搭配。你可以先索取樣品，在自己的設備和包裝上試用，確認合適後再決定訂單。',hero='為下一批標籤，選好母卷材料',intro='紙類或薄膜，白色、透明或彩色。從標籤用途找到合適的材料，再用樣品確認印刷和貼標效果。',catalog='全部材料',structure='材料結構',trial='樣品拿到後，先看這些',sample='索取樣品',view='查看產品',liner='離型紙',converting='塗佈與加工',workflow='從第一次打樣，到下一次訂購',steps=[['選材料','告訴我們包裝材質、印刷方式與使用環境。'],['確認卷材尺寸','提供設備需要的幅寬、卷長、紙芯與捲向，逐項核對。'],['先試樣','用實際包裝及設備，檢查印刷、模切與貼合效果。'],['確認訂單資料','記錄確認過的材料組合，並核對目的地所需文件。']],faq='第一次訂購，先了解這幾件事',qas=[['詢價要提供什麼？','材料、膠種、底材、卷材尺寸、紙芯、數量與目的國。還沒有確定規格也沒關係，先說明標籤用途即可開始討論。'],['底紙是什麼顏色？','依材料組合選擇，請以確認的樣品為準。顏色本身不能代表底紙的離型或加工性能。'],['可以按設備需要的幅寬詢價嗎？','可以先提供有效幅寬、紙芯內徑、最大卷外徑與捲向。我們會在報價前確認可行的尺寸。'],['第一批訂單何時能出貨？','需依材料規格、數量與樣品確認情況安排。詢價時請告訴我們希望的到貨時間，再一起確認交期。'],['碳帶與設備怎麼詢問？','印刷指南有蠟基、蠟樹脂基、樹脂基碳帶及貼標設備介紹。提供機型和用途，即可進一步確認相容性與供應情況。']],more='了解我們'),
 dict(about='О RolloBase',company='RolloBase производит самоклеящиеся материалы в джамбо-рулонах для типографий, переработчиков и дистрибьюторов. Мы поставляем термобумагу и мелованную бумагу, в том числе цветные варианты, ПЭТ, BOPP, синтетическую и антиадгезионную бумагу.',approach='Расскажите, на что будет наклеена этикетка и как вы планируете её печатать. Это поможет подобрать лицевой материал, клей и подложку. Образец позволит проверить сочетание на вашем оборудовании и упаковке до заказа.',hero='Материалы для следующего тиража этикеток',intro='Бумага или плёнка, белая, прозрачная или цветная. Выберите материал по применению и проверьте образец на своей линии.',catalog='Все материалы',structure='Состав материала',trial='Что проверить на образце',sample='Запросить образец',view='Подробнее',liner='Антиадгезионная бумага',converting='Нанесение покрытия и переработка',workflow='От первого образца до следующего заказа',steps=[['Выбор материала','Начните с упаковки, способа печати и условий эксплуатации.'],['Формат рулона','Укажите ширину, длину, втулку и направление намотки для вашего оборудования.'],['Пробный запуск','Проверьте печать, высечку и приклеивание в реальных условиях.'],['Подготовка заказа','Зафиксируйте согласованный состав и необходимые документы для страны назначения.']],faq='Перед первым заказом',qas=[['Что нужно для расчёта цены?','Укажите материал, клей, подложку, размеры рулона, втулку, количество и страну назначения. Если спецификации ещё нет, начните с применения этикетки.'],['Какого цвета будет подложка?','Цвет зависит от выбранной конструкции и согласуется по образцу. Сам по себе цвет не определяет свойства подложки.'],['Можно запросить ширину под наше оборудование?','Сообщите полезную ширину, диаметр втулки, максимальный диаметр рулона и направление намотки. До расчёта цены мы проверим возможность изготовления.'],['Когда возможна первая отгрузка?','Срок согласуется после уточнения спецификации, количества и утверждения образца. Укажите желаемую дату получения в запросе.'],['Как узнать о риббонах и оборудовании?','В руководстве по печати представлены восковые, смешанные и смоляные риббоны, а также аппликаторы этикеток. Укажите модель и задачу для проверки совместимости и наличия.']],more='Подробнее о RolloBase'),
 dict(about='关于 RolloBase',company='RolloBase 专注制造不干胶母卷材料，服务标签印刷厂、加工厂和经销商。我们供应热敏纸、铜版纸及其彩色系列，以及 PET、BOPP、合成纸和离型纸。',approach='选材料时，我们先了解标签贴在哪里、怎么印刷，以及使用环境，再讨论面材、胶和底材的搭配。你可以先索取样品，在自己的设备和包装上试用，确认合适后再决定订单。',hero='为下一批标签，选好母卷材料',intro='纸类或薄膜，白色、透明或彩色。从标签用途找到合适的材料，再用样品确认印刷和贴标效果。',catalog='全部材料',structure='材料结构',trial='样品拿到后，先看这些',sample='索取样品',view='查看产品',liner='离型纸',converting='涂布与加工',workflow='从第一次打样，到下一次订购',steps=[['选材料','告诉我们包装材质、印刷方式和使用环境。'],['确认卷材尺寸','提供设备需要的幅宽、卷长、纸芯和卷向，逐项核对。'],['先试样','用实际包装和设备，检查印刷、模切和贴合效果。'],['确认订单资料','记录确认过的材料组合，并核对目的地所需文件。']],faq='第一次订购，先了解这几件事',qas=[['询价要提供什么？','材料、胶型、底材、卷材尺寸、纸芯、数量和目的国。还没有确定规格也没关系，先说明标签用途即可开始讨论。'],['底纸是什么颜色？','按材料组合选择，请以确认的样品为准。颜色本身不能代表底纸的离型或加工性能。'],['可以按设备需要的幅宽询价吗？','可以先提供有效幅宽、纸芯内径、最大卷外径和卷向。我们会在报价前确认可行的尺寸。'],['第一批订单何时能出货？','需按材料规格、数量和样品确认情况安排。询价时请告诉我们希望的到货时间，再一起确认交期。'],['碳带与设备怎么询问？','印刷指南有蜡基、蜡树脂基、树脂基碳带和贴标设备介绍。提供机型和用途，即可进一步确认兼容性和供应情况。']],more='了解我们')]

def apply(dist,origin):
    dist=Path(dist)
    media=json.loads((Path(__file__).parent/'site-photos.json').read_text())
    groups={k:v+[RU_ROUTES[k],k+'-zh-cn.html'] for k,v in routes.items()}
    groups['home']=['index.html','en.html','zh.html','ru.html','zh-cn.html']
    groups['about']=list(BRAND_FILES)
    groups['guide']=['productos.html','products.html','products-zh.html','products-ru.html','guide-zh-cn.html']
    new_paths={k:[f'{k}-{s}.html' for s in SUFFIX] for k in PRODUCTS}
    def url(path): return origin+('/' if path=='index.html' else '/'+path)
    # Explicit .html URLs work on static hosts without additional rewrite rules.
    def photo(key,i):
        return photo_html(key,media['photos'],media['copy'][LANGS[i]])
    def workflow(c):
        return '<section class="order-workflow"><h2>'+e(c['workflow'])+'</h2><div class="order-steps">'+''.join(f'<article><small>{j:02}</small><h3>{e(t)}</h3><p>{e(s)}</p></article>' for j,(t,s) in enumerate(c['steps'],1))+'</div></section>'
    def faq(c):
        return '<section class="first-order-faq"><h2>'+e(c['faq'])+'</h2>'+''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in c['qas'])+'</section>'
    for i,c in enumerate(COPY):
        request='/'+groups['request'][i].removesuffix('.html')
        template=(dist/groups['coated'][i]).read_text()
        cards=[]
        for code,p in PRODUCTS.items():
            name,desc,construction,trial=p['rows'][i]
            path=new_paths[code][i]
            sample=request+'?material='+code+'&amp;mode=sample'
            body=f'<section class="expanded-product"><p><a href="/{groups["catalog"][i]}">{e(c["catalog"])} →</a></p><div class="product-story"><div><h1>{e(name)}</h1><p>{e(desc)}</p><a class="button" href="{sample}">{e(c["sample"])}</a></div>{photo(p["photo"],i)}</div></section><section><h2>{e(c["structure"])}</h2><p>{e(construction)}</p><h2>{e(c["trial"])}</h2><p>{e(trial)}</p><a class="buy-link" href="{sample}">{e(c["sample"])} →</a></section>'
            html=re.sub(r'<main>.*?</main>',lambda m:'<main>'+body+'</main>',template,flags=re.S)
            html=re.sub(r'<title>.*?</title>',lambda m:'<title>'+e(name)+' | RolloBase</title>',html)
            for prop,value in [('name="description"',desc),('property="og:title"',name+' | RolloBase'),('property="og:description"',desc),('property="og:url"',url(path))]:
                html=re.sub(r'<meta '+prop+r'[^>]*>',lambda m,prop=prop,value=value:'<meta '+prop+' content="'+e(value,quote=True)+'">',html)
            html=re.sub(r'<link rel="canonical"[^>]*>',lambda m:'<link rel="canonical" href="'+url(path)+'">',html)
            html=re.sub(r'<link rel="alternate"[^>]*>','',html)
            alt=''.join(f'<link rel="alternate" hreflang="{lang}" href="{url(fp)}">' for lang,fp in zip(LANGS+['x-default'],new_paths[code]+[new_paths[code][0]]))
            html=html.replace('</head>',alt+'</head>')
            nav='<div class="languages">'+''.join(f'<a href="/{fp}" lang="{lang}"'+(' aria-current="page"' if j==i else '')+'>'+label+'</a>' for j,(lang,fp,label) in enumerate(zip(LANGS,new_paths[code],['ES','EN','繁中','RU','简中'])))+'</div>'
            html=re.sub(r'<div class="languages">.*?</div>',lambda m:nav,html,flags=re.S)
            schema={'@context':'https://schema.org','@type':'WebPage','name':name,'description':desc,'url':url(path),'inLanguage':LANGS[i],'dateModified':'2026-11-24','about':{'@type':'Product','name':name,'description':desc,'brand':{'@type':'Brand','name':'RolloBase'},'image':origin+'/photos/'+media['photos'][p['photo']]['file']}}
            html=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:'<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script>',html,flags=re.S)
            (dist/path).write_text(html)
            cards.append(f'<article class="finder-card" data-product="{code}" data-family="{p["family"]}" data-use="{p["use"]}" data-keywords="{e(name+" "+desc,quote=True)}">{photo(p["photo"],i)}<h2>{e(name)}</h2><p>{e(desc)}</p><div class="finder-actions"><a href="/{path}">{e(c["view"])}</a><a href="{sample}">{e(c["sample"])}</a></div></article>')
        path=dist/groups['catalog'][i]; html=path.read_text()
        html=html.replace('<div class="finder-cards">','<div class="finder-cards">'+''.join(cards),1)
        html=re.sub(r'(<select name="family">.*?)(</select>)',lambda m:m[1]+f'<option value="liner">{e(c["liner"])}</option>'+m[2],html,flags=re.S)
        html=re.sub(r'(<select name="use">.*?)(</select>)',lambda m:m[1]+f'<option value="converting">{e(c["converting"])}</option>'+m[2],html,flags=re.S)
        html=re.sub(r'(data-format="[^"]*">)([^<]*?)6(?=</p>)',r'\g<1>\g<2>10',html)
        path.write_text(html)
        path=dist/groups['request'][i]; html=path.read_text()
        options=''.join(f'<option value="{code}">{e(p["rows"][i][0])}</option>' for code,p in PRODUCTS.items())
        html=re.sub(r'(<select name="material"[^>]*>.*?)(</select>)',lambda m:m[1]+options+m[2],html,flags=re.S)
        # The selector now includes standalone liner as well as label facestock.
        material_labels=['Material','Material','材料','Материал','材料']
        html=re.sub(r'(<label>)[^<]*(<select name="material")',lambda m:m[1]+material_labels[i]+m[2],html,count=1)
        path.write_text(html)
        about=f'<section class="company-story" id="company"><h2>{e(c["about"])}</h2><p>{e(c["company"])}</p><p>{e(c["approach"])}</p></section>'
        path=dist/groups['about'][i]; html=path.read_text()
        html=re.sub(r'<section><h1>.*?</section>',lambda m:about.replace('<h2>','<h1>',1).replace('</h2>','</h1>',1)+workflow(c),html,count=1,flags=re.S)
        # Keep page description and visible company statement aligned.
        html=re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*',lambda m:m[1]+e(c['company'],quote=True),html)
        path.write_text(html)
        path=dist/groups['home'][i]; html=path.read_text()
        html=re.sub(r'(<div class="hero-copy">.*?<h1>).*?(</h1><p>).*?(</p>)',lambda m:m[1]+e(c['hero'])+m[2]+e(c['intro'])+m[3],html,count=1,flags=re.S)
        teaser=about.replace('</section>',f'<a class="buy-link" href="/{groups["about"][i]}">{e(c["more"])} →</a></section>')
        html=html.replace('<section id="materials">',teaser+'<section id="materials">',1)
        new_home_cards=''.join('<article class="site-photo-card">'+photo(p['photo'],i)+'<a class="appcard" href="/'+new_paths[code][i]+'"><h3>'+e(p['rows'][i][0])+'</h3><p>'+e(p['rows'][i][1])+'</p><b aria-hidden="true">↗</b></a></article>' for code,p in PRODUCTS.items())
        html=re.sub(r'(<section id="materials">.*?<div class="appgrid">)',lambda m:m[1]+new_home_cards,html,count=1,flags=re.S)
        html=html.replace('</main>',workflow(c)+faq(c)+'</main>')
        path.write_text(html)
        # Eight materials together, with real detail-page links.
        keys=[('thermal','jumbo-thermal'),('coated','jumbo-coated'),('color-thermal','jumbo-color-thermal'),('color-coated','jumbo-color-coated'),('pet','jumbo-pet'),('bopp','jumbo-bopp'),('synthetic-paper','jumbo-synthetic'),('release-paper','release-liner')]
        gallery=''.join('<article>'+photo(key,i)+f'<a class="buy-link" href="/{(new_paths[code] if code in new_paths else groups[code])[i]}">{e(c["view"])} →</a></article>' for code,key in keys)
        path=dist/groups['guide'][i]; html=path.read_text()
        html=re.sub(r'<section id="material-photo-reference">.*?</section>',lambda m:'<section id="material-photo-reference"><h2>'+e(c['catalog'])+'</h2><div class="site-photo-gallery">'+gallery+'</div></section>',html,flags=re.S)
        path.write_text(html)
    # Refresh the short home guide text without altering technical guidance.
    guide_titles=['Antes de decidir el material','Before you settle on a material','選定材料前，再看這些','Перед выбором материала','选定材料前，再看这些']
    guide_copy=['Revise cómo se imprime y se pega la muestra. Aquí encontrará qué comprobar en las pruebas, el embalaje y la documentación.','Check how the sample prints and sticks. These guides cover trial checks, packing and the documents to discuss before ordering.','樣品印得如何、貼得牢不牢，都要放到實際條件下看。這裡整理了試樣、包裝與文件的確認重點。','Проверьте печать и приклеивание образца. В этих руководствах собраны вопросы испытаний, упаковки и документов перед заказом.','样品印得如何、贴得牢不牢，都要放到实际条件下看。这里整理了试样、包装和文件的确认重点。']
    for i,name in enumerate(groups['home']):
        path=dist/name; html=path.read_text()
        html=re.sub(r'(<section id="buyer-guides"><h2>).*?(</h2><p>).*?(</p>)',lambda m:m[1]+e(guide_titles[i])+m[2]+e(guide_copy[i])+m[3],html,count=1,flags=re.S)
        path.write_text(html)
    # Remove stock-photo blocks together with their attribution, not just their credits.
    # Retain only the user-authorized originals. Product diagrams and text citations remain.
    for path in dist.glob('*.html'):
        html=path.read_text(); lang=re.search(r'<html lang="([^"]+)"',html)[1]; i=LANGS.index(lang)
        def authorized(m):
            block=m[0]
            if 'site-photo-cutout' in block: return re.sub(r'<figcaption>.*?</figcaption>','',block,flags=re.S)
            if '<img' in block: return ''
            return block
        html=re.sub(r'<figure\b.*?</figure>',authorized,html,flags=re.S)
        # The hero uses the authorized coated-paper image, not a third-party factory.
        if path.name in groups['home']:
            hero_photo=re.sub(r'<figcaption>.*?</figcaption>','',photo('jumbo-coated',i),flags=re.S).replace('loading="lazy"','fetchpriority="high"')
            html=re.sub(r'(<section class="hero">.*?)</section>',lambda m:m[1]+hero_photo+'</section>',html,count=1,flags=re.S)
        html=re.sub(r'(<footer>.*?)<details>.*?</details>',lambda m:m[1],html,count=1,flags=re.S)
        if path.name in groups['about']+groups['home']:
            def revise_schema(m):
                data=json.loads(m[1])
                for node in data.get('@graph',[]):
                    if node.get('@type')=='WebPage':
                        node['description']=COPY[i]['company'] if path.name in groups['about'] else COPY[i]['intro']
                        node['dateModified']='2026-11-24'
                return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'
            html=re.sub(r'<script type="application/ld\+json">(.*?)</script>',revise_schema,html,flags=re.S)
        html=html.replace('</head>','<link rel="stylesheet" href="/catalog-expansion.css"></head>')
        path.write_text(html)
    css='''.company-story{max-width:880px}.company-story p{line-height:1.85}.order-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px;background:#eaf0df;padding:32px}.order-steps small{color:#b63e21;font-weight:700}.order-steps p{line-height:1.75}.first-order-faq details{border-top:1px solid #b9c8c4;padding:22px 0}.first-order-faq summary{font-size:1.12rem;font-weight:650;cursor:pointer}.first-order-faq details p{max-width:820px;line-height:1.8}.product-story{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}.product-story h1{font-size:clamp(2rem,4vw,3.5rem)}.product-story p{line-height:1.85}.site-photo-pair:empty{display:none}.feature:not(:has(figure)){display:block;max-width:880px}.hero .site-photo{margin:0}.site-photo-gallery article{min-width:0}.site-photo-gallery article>a{display:inline-block;margin-top:12px}@media(max-width:760px){.order-steps{grid-template-columns:1fr;gap:20px;padding:24px}.product-story{grid-template-columns:1fr;gap:24px}.first-order-faq summary{line-height:1.6}.company-story p{font-size:1rem}}'''
    (dist/'catalog-expansion.css').write_text(css)
    sitemap=dist/'sitemap.xml'; xml=sitemap.read_text()
    added=''.join(f'<url><loc>{url(p)}</loc><lastmod>2026-11-24</lastmod></url>' for paths in new_paths.values() for p in paths)
    sitemap.write_text(xml.replace('</urlset>',added+'</urlset>'))
