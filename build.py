from pathlib import Path
from html import escape
import os
import json
from purchasing import extra_pages, labels, routes
from knowledge import HREFLANG, UPDATED, enrich, metadata, new_pages, structured_data
from russian import add_russian

dist = Path(__file__).parent / 'dist'
origin = os.getenv('SITE_ORIGIN','https://rollobase-materials.onrender.com').rstrip('/')
langs = ['es-419','en','zh-Hant']
home = ['index.html','en.html','zh.html']
guide = ['productos.html','products.html','products-zh.html']
def tr(es,en,zh): return [es,en,zh][i]
def page_url(path):
    return origin + ('/' if path=='index.html' else '/'+path.removesuffix('.html'))
def taglinks(paths):
    return ''.join(f'<link rel="alternate" hreflang="{lang}" href="{page_url(path)}">' for lang,path in zip(HREFLANG+['x-default'],paths+[paths[0]]))
def item(name, detail): return f'<article><h3>{name}</h3><p>{detail}</p></article>'

photographs = json.loads(Path(__file__).with_name('photo-credits.json').read_text())

def photo(slot, index):
    if slot == 'construction':
        return '<figure data-paper-photo></figure>'
    file = 'hero-rolls.webp'
    caption = ['Bobinas de papel en Gmund, Alemania', 'Paper rolls at Gmund, Germany', '德國 Gmund 紙廠的紙母卷'][index]
    dims = 'width="1680" height="1120" fetchpriority="high"'
    author = next(p['author'] for p in photographs if p['file'] == file)
    return f'<figure><img src="{file}" {dims} alt="{caption}"><figcaption>{caption} · {author}</figcaption></figure>'

def credits(index):
    parts = []
    for p in photographs:
        changes = [p['changes_es'], 'The photographer masked client information. Cropped, resized and converted to WebP.', '原作者已遮蔽客戶資料。網頁版經裁切、縮放及 WebP 轉檔。'][index]
        parts.append(f'<p><a href="{p["source"]}">{p["title"]}</a> · {p["author"]} · <a href="{p["license_url"]}">{p["license"]}</a>. {changes}</p>')
    return ''.join(parts)

for i,lang in enumerate(langs):
    home_label=tr('Inicio','Home','首頁')
    materials=tr('Materiales','Materials','材料分類')
    tech=tr('Guía técnica','Technical guide','產品技術指南')
    title=tr('Materiales autoadhesivos en bobina','Self-adhesive labelstock master rolls','自黏標籤材料母卷')
    intro=tr('Compare papeles y películas para etiquetas. Elija el frontal y el adhesivo según el envase, la impresión y las condiciones de uso.','Compare paper and film label materials. Match the facestock and adhesive to your container, printing process and service conditions.','比較紙類與薄膜不乾膠母卷，依容器表面、印刷方式與使用環境，挑選面材及感壓膠。')
    families=[tr('Papeles','Paper labelstock','紙類標籤母卷'),tr('Películas','Film labelstock','薄膜標籤母卷')]
    rows=[
      (tr('Papel estucado semibrillante','Semi-gloss coated paper','半光澤銅版紙'),tr('Etiquetas de frascos y cajas de venta. La superficie lisa favorece la definición de imágenes.','Jar and retail carton labels. The smooth coating supports fine graphics.','用於罐身與商品外盒標籤。平滑塗層適合細緻圖文，潮濕用途需測試表面保護。')),
      (tr('Papel térmico directo','Direct thermal paper','熱感紙（感熱紙）'),tr('Etiquetas de envío y de balanza. El cabezal forma la imagen sin cinta. Compruebe la legibilidad tras luz y calor.','Shipping and scale labels. Heat forms the image without a ribbon. Check readability after exposure to light and heat.','用於物流面單與秤重標籤，熱感層受熱顯色，列印免碳帶。應測試光照、受熱後的條碼可讀性。')),
      (tr('Polipropileno (BOPP)','Polypropylene (BOPP)','雙向延伸聚丙烯（BOPP）'),tr('Etiquetas transparentes o blancas para botellas rígidas. Evalúe humedad, transparencia del adhesivo y adherencia de la tinta.','Clear or white labels for rigid bottles. Test moisture exposure, adhesive clarity and ink anchorage.','用於硬質瓶身的透明或白色標籤。透明標籤需檢查膠層霧度、遇水外觀及油墨附著。')),
      (tr('Polietileno (PE)','Polyethylene (PE)','聚乙烯（PE）'),tr('Etiquetas para botellas flexibles de champú. Pruebe varios ciclos de compresión para detectar arrugas y bordes levantados.','Labels for squeezable shampoo bottles. Squeeze repeatedly and inspect for creases and lifting edges.','用於洗髮精等可擠壓瓶標。以實際填充後的容器反覆擠壓，觀察起皺與翹邊。')),
      (tr('Poliéster (PET)','Polyester (PET)','聚酯（PET）'),tr('Placas de identificación de equipos. Ensaye el conjunto impreso frente al roce, la limpieza y la temperatura previstos.','Equipment identification labels. Test the printed construction for expected abrasion, cleaning and temperature exposure.','用於設備銘牌與資產標籤。以印刷完成的標籤測試摩擦、清潔劑與實際使用溫度。'))]
    groups=[rows[:2],rows[2:]]
    layernames=[tr('Frontal','Facestock','面材'),tr('Adhesivo sensible a la presión','Pressure-sensitive adhesive','感壓膠層'),tr('Soporte antiadherente','Release liner','離型底材')]
    layers=[tr('El papel o la película recibe la impresión y queda en el envase. Su rigidez, opacidad y tratamiento superficial influyen en el aspecto y la adaptación a curvas.','The printed paper or film stays on the container. Stiffness, opacity and surface treatment affect appearance and conformity to curves.','印刷圖文的紙張或薄膜會留在被貼物上。挺度影響曲面服貼性，透明度與表面塗層則影響遮蔽效果及油墨附著。'),tr('La presión pone la capa de adhesivo en contacto con el envase. La adherencia inicial al dispensar y la adhesión final tras el reposo se evalúan por separado.','Application pressure brings the adhesive into contact with the container. Assess initial tack at dispensing and final adhesion after dwell separately.','貼合壓力讓膠層與容器表面充分接觸。貼標當下的初黏力與放置一段時間後的剝離黏著力，須分別評估。'),tr('El papel glassine o la película PET con recubrimiento de silicona protege el adhesivo en la bobina. Durante el troquelado sostiene la etiqueta y se separa al dispensarla.','Silicone-coated glassine paper or PET film protects the adhesive in the roll. It supports the label during die-cutting and peels away at dispensing.','經矽離型處理的格拉辛紙或 PET 離型膜，在收捲時保護膠層。模切時底材承托標籤，剝標時則在離型面分離。')]
    adh=tr('Cómo elegir el adhesivo','How to choose a label adhesive','如何選擇標籤用膠')
    glues=[
    (tr('Acrílico en emulsión','Emulsion acrylic','水性壓克力膠（水膠）'),tr('El agua sirve de vehículo y se elimina durante el recubrimiento. Para un envase transparente, revise claridad y blanqueamiento por humedad.','Water carries the polymer and is removed during coating. For clear packaging, check adhesive clarity and whitening in humid conditions.','塗布時以水為分散介質，乾燥後形成膠層。透明瓶標應以實際樣品檢查膠層霧度及遇水泛白。')),
    (tr('Termofusible de caucho','Rubber-based hot melt','橡膠系熱熔膠'),tr('Se aplica fundido durante la fabricación. Hay formulaciones de alta adherencia inicial para cartón rugoso. Verifique el comportamiento ante calor y luz solar.','Applied molten during manufacture. High-tack grades are candidates for rough cartons. Check service heat and sunlight exposure.','製造時以熔融方式塗布。粗糙紙箱可評估高初黏配方，並檢查高溫與日照後是否滑移或翹邊。')),
    (tr('Acrílico en disolvente','Solvent acrylic','溶劑型壓克力膠（油膠）'),tr('El disolvente se evapora durante la fabricación. Para identificación duradera, compare la ficha del grado y ensaye los líquidos de limpieza reales.','The solvent evaporates during manufacture. For durable identification, compare grade specifications and test with the actual cleaning fluids.','塗布後溶劑揮發形成膠層。耐久識別用途應核對個別配方規格，再以實際清潔劑與溫度試貼。'))]
    selection=tr('Permanente, removible o para frío','Permanent, removable or cold-temperature grades','永久膠、可移膠與低溫膠怎麼選？')
    seltext=tr('Estas designaciones describen el uso. Para una etiqueta temporal, compruebe residuos después del tiempo previsto. En refrigeración, distinga la temperatura al aplicar de la temperatura de servicio y pruebe si hay condensación.','These terms describe intended use. For a temporary label, check for residue after the intended dwell time. For chilled goods, distinguish application temperature from service temperature and test with any condensation present.','這些名稱描述使用需求。短期促銷標籤可評估可移膠，在預定貼附時間後檢查殘膠與表面損傷。冷藏品須區分貼標當下與後續儲運溫度，並以實際結露狀態試貼。')
    structure=tr('Estructura de una bobina madre','Anatomy of a labelstock master roll','不乾膠母卷的三層結構')
    overview=tr('Una bobina madre reúne un frontal imprimible, un adhesivo y un soporte siliconado. El convertidor la corta, imprime y troquela para producir etiquetas.','A master roll combines printable facestock, pressure-sensitive adhesive and a release liner. Converters slit, print and die-cut the stock into finished labels.','不乾膠母卷由可印刷面材、感壓膠與離型底材組成，加工廠可依成品需求分條、印刷及模切，製成標籤。')
    title=tr('Bobinas madre para etiquetas autoadhesivas','Self-adhesive labelstock master rolls','不乾膠標籤母卷選材指南')
    intro=tr('Compare papel térmico directo, papel estucado y películas autoadhesivas en bobina. Elija el material según el envase, la impresión y la temperatura de uso.','From shipping barcodes to squeezable bottles. Compare five label materials by surface, printing process and service conditions.','從物流條碼到可擠壓的洗髮精瓶，依貼標表面、印刷方式與使用環境，比較五種自黏標籤面材。')
    title=tr('Bobinas madre de material autoadhesivo para fabricantes de etiquetas','Self-adhesive labelstock jumbo rolls for converters','標籤加工廠與經銷商用不乾膠母卷')
    intro=tr('Para convertidores y distribuidores. Compare el frontal, el adhesivo y el soporte según su proceso de impresión y la superficie de aplicación.','For label converters and distributors. Match the facestock, adhesive and release liner to your printing process and application surface.','供標籤加工廠與經銷商選材。依印刷方式與被貼表面，比較面材、感壓膠及離型底材，再按同一組規格索樣與詢價。')
    apps=tr('Elegir por aplicación','Choose by application','依成品用途選材')
    specs=tr('Ficha de consulta','Sample brief','打樣規格單')
    action=tr('Comparar materiales','Compare materials','比較標籤材料')
    product_title=tr('Guía de materiales y adhesivos para etiquetas','Labelstock construction and adhesive selection','不乾膠母卷結構與標籤用膠指南')
    appnames=[tr('Frascos y cajas','Jars and retail cartons','罐身與商品外盒'),tr('Envíos y balanzas','Shipping and scale labels','物流面單與秤重標籤'),tr('Botellas rígidas','Rigid bottles','硬質瓶身'),tr('Envases flexibles','Squeezable bottles','可擠壓瓶身'),tr('Equipos y activos','Equipment and assets','設備與資產銘牌')]
    quick=[tr('Gráficos finos en envases secos.','Fine graphics on dry packaging.','乾燥環境下的細緻圖文。'),tr('Datos variables sin ribbon.','Variable data without a ribbon.','免碳帶列印可變條碼。'),tr('Etiquetas blancas o transparentes.','White or clear bottle labels.','透明或白色瓶標。'),tr('Un frontal que acompaña la curva.','A face material that follows the squeeze.','面材需隨瓶身擠壓變形。'),tr('Identificación expuesta a limpieza.','Identification exposed to cleaning.','面對擦拭與清潔劑的識別標籤。')]
    keys=['coated','thermal','bopp','pe','pet']
    checks=[
        tr('Superficie y aplicación','Container and application','容器與貼標環境'),
        tr('Impresión y acabado','Print process and finish','印刷方式與表面處理'),
        tr('Dimensiones y destino','Roll size and destination','母卷尺寸與目的地')]
    checklist=[
        tr('Material del envase, curvatura, humedad y temperaturas de aplicación y de servicio.','Container material, curvature, moisture, application temperature and service temperature.','填寫玻璃、紙箱、PE 或 PET 等被貼物、曲率、濕度，以及貼標和儲運溫度。'),
        tr('Equipo, tintas o ribbon, frontal, adhesivo, soporte y pruebas requeridas.','Press or printer model, ink or ribbon, facestock, adhesive, release liner and trial criteria.','列出機型、油墨或碳帶、面材、膠種、離型底材，以及樣品的驗收條件。'),
        tr('Ancho útil, largo, núcleo, diámetro exterior máximo, cantidad y ciudad o puerto de entrega.','Usable width, roll length, core size, maximum outside diameter, quantity and delivery city or port.','註明可用幅寬、卷長、紙管內徑、最大外徑、數量與交貨城市或港口。')]
    questions=[
      (tr('¿Qué diferencia hay entre térmico directo y transferencia térmica?','Direct thermal vs. thermal transfer labels: which needs a ribbon?','熱感標籤和熱轉印標籤，哪種需要碳帶？'),tr('En térmico directo el cabezal activa el recubrimiento del frontal. En transferencia térmica, una cinta o ribbon aporta la tinta. Antes de comprar la bobina, pruebe la lectura del código después del roce y del almacenamiento previstos.','Direct thermal printing activates the coating on the paper. Thermal transfer uses a ribbon to put an image on a compatible face. Print a sample and check barcode readability after expected handling and storage.','熱感紙由列印頭加熱顯色，熱轉印則用碳帶把圖文轉印至相容的面材。選購條碼標籤母卷前，先印樣並確認經過摩擦與儲存後仍可掃讀。')),
      (tr('¿Cuándo conviene probar BOPP o PE?','Should I trial BOPP or PE for a bottle label?','瓶身標籤應選 BOPP 還是 PE？'),tr('Para botellas rígidas, empiece con BOPP blanco o transparente. Para un envase que se comprime, pruebe PE en una botella llena. Revise bordes, arrugas y adherencia después de varios ciclos.','Start with white or clear BOPP on a rigid bottle. For a squeezable pack, trial PE on the filled container. After repeated squeezes, check adhesion, creases and edge lift.','硬質瓶可先試白色或透明 BOPP 標籤膜，可擠壓容器則可先試 PE。將標籤貼在裝填後的實際瓶身，反覆擠壓後檢查起皺、翹邊與黏著狀態。')),
      (tr('¿Cómo comparar dos cotizaciones de bobinas jumbo?','How do I compare quotes for labelstock jumbo rolls?','如何比較兩份不乾膠母卷報價？'),tr('Compare la misma combinación de frontal, adhesivo y liner por metro cuadrado útil. Pida por separado cantidad mínima, muestra, embalaje, flete y condiciones de entrega.','Compare the same facestock, adhesive and release liner per usable square metre. Ask for the minimum order, sample cost, packing, freight and delivery terms as separate items.','先確認面材、膠層與底材相同，再以每可用平方公尺的價格比較。分別列出最低訂購量、打樣、包裝、運費與交貨條件，可避免卷價相同但可用面積不同。'))]
    if lang == 'es-419':
        questions.extend([
            ('¿Qué adhesivo conviene para etiquetas de productos refrigerados?',
             'Primero distinga dos situaciones. Si se etiqueta antes de enfriar, compruebe la temperatura de servicio del adhesivo. Si el envase ya está frío, compruebe además la temperatura mínima de aplicación y si hay condensación. Pruebe la muestra en el envase real y revise si se levantan los bordes.'),
            ('¿Qué medidas debo indicar al cotizar una bobina madre autoadhesiva?',
             'Indique el ancho útil en milímetros, el largo en metros, el diámetro interior del núcleo y el diámetro exterior máximo que admite la máquina. Añada el sentido de bobinado y la cantidad en metros cuadrados para comparar ofertas equivalentes.'),
        ])
    rfq=f'brief-{lang}.txt'
    formtitle=tr('Solicitud de muestra o cotización','Labelstock sample or quotation request','標籤母卷打樣與詢價規格單')
    fields=[tr('Producto final','Finished label application','成品用途'),tr('Envase y condiciones de uso','Container and service conditions','容器及使用環境'),tr('Temperatura de aplicación / de servicio (°C)','Application / service temperature (°C)','貼標／使用溫度（°C）'),tr('Frontal / adhesivo / liner','Facestock / adhesive / release liner','面材／感壓膠／離型底材'),tr('Equipo, tinta o ribbon','Press, ink or ribbon','印刷設備、油墨或碳帶'),tr('Ancho útil (mm) / largo (m)','Usable width (mm) / length (m)','可用幅寬（mm）／卷長（m）'),tr('Núcleo / diámetro exterior máximo (mm)','Core ID / maximum roll OD (mm)','紙管內徑／最大卷外徑（mm）'),tr('Cantidad (m²) / destino','Quantity (m²) / destination','數量（m²）／目的地'),tr('Ensayo y criterio de aceptación','Trial and acceptance criteria','試樣與驗收條件')]
    (dist/rfq).write_text(formtitle+'\n\n'+'\n\n'.join(f+' ___________________' for f in fields)+'\n',encoding='utf-8-sig')
    facts=''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in questions)
    refname=tr('Fuentes técnicas','Technical sources','技術參考')
    refs=[('LINTEC','https://www.lintec-global.com/products/label/pdf/labelstocks_catalog.pdf'),('Avery Dennison','https://label.averydennison.com/eu/en/home/products/adhesives.html'),('UPM','https://www.adhesivematerials.upm.com/label-solutions/label-types/digital-printing/'),('Chung Hwa Pulp','https://www.chp.com.tw/product/special_paper/detail/8')]
    sources=' · '.join(f'<a href="{url}">{name}</a>' for name,url in refs)
    download=tr('Descargar ficha (.txt)','Download sample brief (.txt)','下載打樣規格單（TXT）')
    ui=labels(tr)
    brief=f'<section id="brief" class="brief"><div><h2>{tr("Antes de pedir una muestra","Before requesting a sample","打樣前要準備什麼？")}</h2><a class="button light" href="{routes["request"][i]}">{ui["request"]} →</a><p><a style="color:white" href="{rfq}" download>{download} ↓</a></p></div><dl>'+''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in zip(checks,checklist))+'</dl></section>'
    def page_header(paths):
        switch=''.join(f'<a href="{path}" lang="{l}" '+('aria-current="page" ' if n==i else '')+f'>{lbl}</a>' for n,(l,path,lbl) in enumerate(zip(langs,paths,['ES','EN','繁中'])))
        brand=f'<a class="brand" href="{home[i]}"><b aria-hidden="true"></b>RolloBase</a>'
        menu=[(routes['catalog'][i],ui['catalog']),(guide[i],tech),(routes['sourcing'][i],ui['sourcing']),(routes['quality'][i],tr('Calidad','Quality','品質文件')),(routes['printing'][i],tr('Impresión','Printing','印刷試驗')),(routes['request'][i],ui['request'])]
        links=''.join(f'<a href="{url}">{label}</a>' for url,label in menu)
        return f'<header><div class="headwrap">{brand}<nav>{links}</nav><div class="languages">{switch}</div></div></header>'
    for product in (False,True):
        paths=guide if product else home
        heading=product_title if product else title
        desc=overview if product else intro
        nav=page_header(paths)
        brand=f'<a class="brand" href="{home[i]}"><b aria-hidden="true"></b>RolloBase</a>'
        if not product:
            cardgroup=''.join(f'<a class="appcard" href="{routes[key][i]}"><span>{app}</span><h3>{mat}</h3><p>{note}</p><b aria-hidden="true">↗</b></a>' for key,app,(mat,_),note in zip(keys,appnames,rows,quick))
            body=f'''<section class="hero"><div class="hero-copy"><h1>{title}</h1><p>{intro}</p><a class="button" href="{routes["catalog"][i]}">{ui["catalog"]} →</a> <a class="buy-link" href="{routes["request"][i]}?mode=quote">{ui["quote"]} →</a></div>'''+photo('hero',i)+'</section>'
            body+=f'<section id="materials"><div class="sectionhead"><h2>{apps}</h2><a href="{guide[i]}">{tech} →</a></div><div class="appgrid">{cardgroup}</div></section>'
            body+=f'<section class="feature">{photo("construction",i)}<div><h2>{structure}</h2><p>{overview}</p><a href="{guide[i]}#layers">{tr("Ver las tres capas","Explore the three layers","查看三層材料圖解")} →</a></div></section>'+brief
        else:
            diagram=''.join(f'<span>{n}</span>' for n in layernames)
            body=f'<section class="lead"><div><h1>{heading}</h1><p>{overview}</p></div><div class="diagram">{diagram}</div></section>'
            jumplinks=[('layers',structure),('adhesives',adh),('materials',materials),('faq',tr('Preguntas frecuentes','Common questions','選材問答'))]
            body+='<div class="toc">'+''.join(f'<a href="#{key}">{label} ↓</a>' for key,label in jumplinks)+'</div>'
            body+=f'<section id="layers"><h2>{structure}</h2><div class="grid">'+''.join(item(*r) for r in zip(layernames,layers))+'</div></section>'
            body+=f'<section id="adhesives"><h2>{adh}</h2><div class="grid">'+''.join(item(*r) for r in glues)+f'</div><aside><h3>{selection}</h3><p>{seltext}</p></aside></section>'
            body+=f'<section id="materials"><h2>{action}</h2>'
            offset=0
            for n,(family,group) in enumerate(zip(families,groups)):
                body+=f'<div id="f{n}" class="family"><h3>{family}</h3><div>'
                for mat,note in group:
                    body+=f'<article class="material" id="{keys[offset]}"><div><small>{appnames[offset]}</small><h4><a href="{routes[keys[offset]][i]}">{mat}</a></h4></div><p>{note}</p></article>'
                    offset+=1
                body+='</div></div>'
            body+='</section>'
            if i==0:
                body+='<aside><h3>¿Qué significa papel ilustración?</h3><p>En Argentina se usa «papel ilustración» para papeles estucados con distintos acabados. Al comparar una oferta de semigloss o papel semibrillo, especifique el brillo, el gramaje y la muestra de referencia. <a href="https://www.inpar.com.ar/index.php">Inpar, Argentina</a> · <a href="https://six-graphics.com/materiales-autoadhesivos/">Six Graphics, Guatemala</a></p></aside>'
            body+=f'<aside><h3>{tr("Cómo leer g/m² y μm","Reading g/m² and μm","克重與厚度怎麼讀？")}</h3><p>{tr("El gramaje mide masa por área; el espesor mide distancia entre las caras. Registre cada capa por separado y confirme el método, la tolerancia y la versión de la ficha técnica.","Grammage measures mass per area. Thickness measures the distance between surfaces. Record each layer separately and confirm the test method, tolerance and data-sheet revision.","克重是每單位面積的質量，厚度是兩表面間的距離。應逐層記錄，另核對測試方法、允差及資料表版本。")}</p><a href="{routes["woodfree"][i]}">{ui["wood"]} →</a></aside>'
            body+=f'<section id="faq" class="questions"><h2>{tr("Preguntas de selección","Material selection questions","採購與選材常見問題")}</h2><div>{facts}<p class="refs">{refname} · {sources}</p></div></section>'+brief
        pagetitle=heading+' | RolloBase'
        pageurl=f'{origin}/{paths[i]}'
        data={'@context':'https://schema.org','@type':'WebPage','url':pageurl,'name':heading,'description':desc,'inLanguage':lang}
        if lang == 'es-419':
            if product:
                pagetitle='Papel térmico, BOPP y adhesivos para etiquetas | RolloBase'
                desc='Compare cinco materiales autoadhesivos en bobina. Revise el frontal, el adhesivo y el liner, elija una muestra y prepare su solicitud de cotización.'
                data['hasPart']={
                    '@type':'WebPageElement', '@id':pageurl+'#faq',
                    'name':'Preguntas de selección', 'url':pageurl+'#faq',
                    'hasPart':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in questions],
                }
            else:
                pagetitle='Bobinas madre autoadhesivas para etiquetas de papel y BOPP | RolloBase'
                desc='Guía para convertidores de etiquetas. Compare bobinas jumbo de papel térmico, papel estucado, BOPP, PE y PET según el envase y el proceso de impresión.'
                buyer_links='<section class="questions"><h2>¿Por dónde empezar?</h2><div><p>Una bobina madre autoadhesiva, también llamada bobina jumbo, es el material en rollo que el convertidor corta, imprime y troquela. Para elegir una construcción, empiece por la superficie donde se pegará la etiqueta.</p><ul><li><a href="productos.html#thermal">Papel térmico directo para etiquetas de envío</a></li><li><a href="productos.html#bopp">BOPP blanco o transparente para botellas rígidas</a></li><li><a href="productos.html#adhesives">Adhesivos para etiquetas permanentes, removibles o en frío</a></li></ul></div></section>'
                body=body.removesuffix(brief)+buyer_links+brief
            data['description']=desc
        foot=f'<footer>{brand}<details><summary>{tr("Créditos fotográficos","Photo credits","攝影作品與授權")}</summary>{credits(i)}</details></footer>'
        def save_page(paths,pagetitle,desc,data,body):
            pageurl=page_url(paths[i])
            nav=page_header(paths)
            key = 'home' if paths==home else 'guide' if paths==guide else next(k for k,v in routes.items() if v==paths)
            pagetitle,desc=metadata(key,i)
            body=enrich(key,i,body,routes,home,guide)
            if key!='home' and 'class="crumb"' not in body:
                body=f'<p class="crumb"><a href="{home[i]}">{home_label}</a> / {escape(pagetitle.removesuffix(" | RolloBase"))}</p>'+body
            data=structured_data(key,i,pagetitle,desc,pageurl,origin,page_url(home[i]),body)
            social=f'<meta property="og:type" content="website"><meta property="og:site_name" content="RolloBase"><meta property="og:title" content="{escape(pagetitle)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{pageurl}">'
            (dist/paths[i]).write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(pagetitle)}</title><meta name="description" content="{escape(desc)}"><link rel="canonical" href="{pageurl}">{taglinks(paths)}{social}<script type="application/ld+json">{data}</script><link rel="stylesheet" href="style.css?v=20261116-ru"><script defer src="buyer.js"></script></head><body>{nav}<main>{body}</main>{foot}</body></html>')
        save_page(paths,pagetitle,desc,data,body)
    for key,heading,desc,body in extra_pages(i,tr,rows,keys,appnames,guide,home,fields):
        paths=routes[key]
        data={'@context':'https://schema.org','@type':'WebPage','name':heading,'description':desc,'inLanguage':lang,'url':origin+'/'+paths[i]}
        save_page(paths,heading+' | RolloBase',desc,data,body)
    for key,heading,desc,body in new_pages(i,routes,home):
        save_page(routes[key],heading+' | RolloBase',desc,{},body)


ru_paths = add_russian(dist, {'home':home,'guide':guide,**routes}, origin)
urls = ''.join(f'<url><loc>{page_url(path)}</loc><lastmod>{UPDATED}</lastmod></url>' for path in home + guide + [p for paths in routes.values() for p in paths] + ru_paths)
(dist/'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>')
(dist/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {origin}/sitemap.xml\n')

from seo_update import publish_update
publish_update(dist, {'home':home,'guide':guide,**routes}, origin)
