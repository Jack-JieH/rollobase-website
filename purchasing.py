"""Buyer-facing catalog and inquiry pages shared across the three locales."""
from html import escape
from urllib.parse import urlencode

routes = {
    'catalog':['materiales.html','materials.html','catalog-zh.html'],
    'request':['cotizacion-muestras.html','quote-sample.html','request-zh.html'],
    'sourcing':['abastecimiento.html','sourcing.html','sourcing-zh.html'],
    'quality':['calidad-trazabilidad.html','quality-traceability.html','quality-zh.html'],
    'printing':['pruebas-impresion.html','printing-compatibility.html','printing-zh.html'],
    'woodfree':['papel-no-estucado.html','uncoated-woodfree.html','woodfree-zh.html'],
    'coated':['papel-semibrillante.html','semi-gloss-coated-paper.html','coated-zh.html'],
    'thermal':['papel-termico-directo.html','direct-thermal-paper.html','thermal-zh.html'],
    'bopp':['pelicula-bopp.html','bopp-film.html','bopp-zh.html'],
    'pe':['pelicula-pe.html','pe-film.html','pe-zh.html'],
    'pet':['pelicula-pet.html','pet-film.html','pet-zh.html'],
}
options = {'A':(60,14,50),'B':(60,20,50),'C':(70,14,60),'D':(70,20,60)}
def labels(t):
    return dict(
        catalog=t('Catálogo','Material catalog','材料目錄'),sample=t('Solicitar muestra','Request a sample','索取樣品'),
        quote=t('Preparar cotización','Prepare a quote request','準備詢價'),request=t('Cotización y muestras','Quotes & samples','詢價與索樣'),
        sourcing=t('Abastecimiento','Sourcing','採購與驗貨'),
        face=t('Frontal','Facestock','面材'),adh=t('Adhesivo','Adhesive','感壓膠'),liner=t('Soporte','Release liner','離型底材'),
        pending=t('Por confirmar con el proveedor','Supplier confirmation required','待供應商確認'),
        wood=t('Papel no estucado en bobina madre','Uncoated woodfree labelstock jumbo rolls','模造紙不乾膠母卷'),
        stock=t('Combinaciones de consulta. Disponibilidad y tolerancias sujetas a confirmación.','Inquiry constructions. Availability and tolerances require supplier confirmation.','以下為詢價組合，可供範圍及允差待供應商確認。'),
        specs=t('Construcción y datos para la prueba','Construction and trial specifications','三層結構與打樣規格'),
        TDS=t('Ficha técnica (TDS)','Technical data sheet (TDS)','技術資料表（TDS）'),
        extra=t('Solicite el código del proveedor, la versión de la ficha, el método de ensayo, las tolerancias y las condiciones de almacenamiento y embalaje.','Request the supplier SKU, dated data sheet, test method, tolerances, storage conditions and packing specification.','請索取供應商料號、資料表版本、測試方法、允差、儲存條件及包裝規格。'),
    )

def extra_pages(i,t,rows,keys,apps,guide,home,fields):
    l=labels(t)
    names=dict(zip(keys,[r[0] for r in rows]))
    names['woodfree']=l['wood']
    notes=dict(zip(keys,[r[1] for r in rows]))
    notes['woodfree']=t('Compare el gramaje del frontal y del adhesivo hot melt antes de pedir una muestra de papel para etiquetas.','Compare face grammage and hot-melt adhesive coat weight before requesting an uncoated paper labelstock trial.','比較模造紙面材克重、熱熔膠塗布量與格拉辛底紙，再選擇組合索樣。')
    apps=dict(zip(keys,apps))
    path=lambda k:routes[k][i]
    def request(key,kind,choice='', short_label=None):
        query=urlencode(dict(material=key,mode=kind,option=choice))
        label = short_label or l[kind] + ' →'
        accessible = f' aria-label="{l[kind]} · {choice}"' if choice else ''
        return f'<a class="buy-link"{accessible} href="{path("request")}?{escape(query)}">{label}</a>'
    def crumb(label):
        return f'<p class="crumb"><a href="{home[i]}">{t("Inicio","Home","首頁")}</a> / <a href="{path("catalog")}">{l["catalog"]}</a> / {label}</p>'
    compare=t('Papel frente a película: compare el frontal, el uso y los datos que faltan para la prueba.','Compare paper and film by facestock, application and trial requirements.','依面材、印刷與成品用途比較紙類及薄膜母卷，確認需要打樣的條件。')
    search=t('Buscar por material, aplicación, impresión o referencia','Search by material, application, printing or reference','搜尋材料、用途、印刷方式或參考編號')
    entries=[]
    for key in [*keys,'woodfree']:
        app=apps.get(key,l['stock'])
        terms={'woodfree':'A B C D 60/14/50 60/20/50 70/14/60 70/20/60 hot melt 熱熔膠 termofusible glassine',
               'thermal':'barcode codigo barras logística direct thermal 熱感 條碼 sin ribbon',
               'coated':'semi gloss semibrillo couché papel ilustración 銅版紙 flexografía',
               'bopp':'PP polypropylene transparente blanco clear white 透明 白色',
               'pe':'PE squeezable flexible 可擠壓','pet':'PET polyester durable poliéster 銘牌'}[key]
        entries.append(f'<a class="appcard" data-search="{terms}" href="{path(key)}"><span>{app}</span><h3>{names[key]}</h3><p>{notes[key]}</p></a>')
    note=t('Sin coincidencias. Pruebe con BOPP, térmico o 60/14/50.','No matches. Try BOPP, thermal or 60/14/50.','沒有符合項目，可試 BOPP、熱感或 60/14/50。')
    catalog=f'<section><h1>{l["catalog"]}</h1><p>{compare}</p><label class="search">{search}<input type="search" id="lookup"></label><div class="appgrid">{"".join(entries)}</div><p hidden id="no-results">{note}</p></section>'
    yield 'catalog',l['catalog'],compare,catalog
    trials={
        'coated':t('Imprima la imagen con la tinta prevista. Revise los detalles finos y la transferencia de tinta tras el secado; repita después de exponer la etiqueta a la humedad prevista.','Print the artwork with the intended ink. Check fine detail and ink transfer after drying, then repeat after expected moisture exposure.','以預定油墨印出含細線的圖樣，乾燥後檢查網點與擦墨；若用於潮濕環境，再測受潮後的印面。'),
        'thermal':t('Imprima un código con la velocidad y energía previstas. Compruebe su lectura antes y después del transporte simulado; registre si el papel tiene capa protectora.','Print a barcode at the intended speed and energy. Check readability before and after simulated handling and record whether the face has a protective topcoat.','以量產速度與熱能列印條碼，記錄紙面有無保護塗層；模擬運輸摩擦前後各掃讀一次。'),
        'bopp':t('Aplique una muestra blanca o transparente al envase lleno. En la versión transparente, observe burbujas y blanqueamiento tras la condensación; confirme la adherencia de la tinta.','Apply a white or clear sample to the filled bottle. On clear film, inspect bubbles and adhesive whitening after condensation, and check ink anchorage.','將白色或透明膜貼在已裝填的瓶身，檢查油墨附著；透明版再觀察結露後的氣泡與膠層泛白。'),
        'pe':t('Marque la posición de la etiqueta sobre el panel flexible. Comprima y suelte el envase repetidamente; registre las arrugas y el levantamiento de bordes.','Mark the label position on the flexible panel. Squeeze and release the pack repeatedly and record creases and edge lift.','標出瓶身擠壓區與貼標位置，重複擠壓、回彈，記錄皺褶位置與翹邊狀況。'),
        'pet':t('Ensaye la etiqueta impresa sobre el acabado real del equipo. Registre legibilidad y adhesión después de los ciclos de limpieza y exposición térmica acordados.','Test the printed label on the actual equipment finish. Record legibility and adhesion after the agreed cleaning and thermal exposure cycles.','在設備實際塗裝面上試貼，按雙方約定的清洗與溫度循環測試，分別記錄字跡可讀性及膠層附著。'),
        'woodfree':t('Use una misma superficie y conserve las muestras con su referencia A–D. Registre el método de impresión y observe absorción de tinta, definición y comportamiento en el troquelado.','Use the same substrate and retain samples with their A–D references. Record printing method, ink absorption, definition and die-cutting behaviour.','使用同一被貼物，依 A～D 留存樣品並記錄印刷方式、吸墨、線條清晰度與模切排廢狀況。'),
    }
    for key in names:
        name=names[key]
        info=notes[key]
        body=crumb(name)+f'<section class="buy-head"><div><h1>{name}</h1><p>{info}</p></div><div>{request(key,"sample")}{request(key,"quote")}</div></section>'
        if key=='woodfree':
            heading=t('Comparar las opciones A–D','Compare options A–D','比較 A～D 打樣規格')
            unit_note=t('Gramaje de cada capa (g/m²)','Weight of each layer (g/m²)','各層克重（g/m²）')
            columns=''.join(f'<th scope="col">{ref}</th>' for ref in options)
            layers=[l['face'],t('Adhesivo hot melt','Hot-melt adhesive','熱熔膠'),t('Soporte glassine','Glassine liner','格拉辛底紙')]
            body+=f'<section id="compare"><h2>{heading}</h2><p>{l["stock"]}</p><table class="trial-comparison"><caption>{unit_note}</caption><thead><tr><th scope="col">{t("Opción","Option","組合")}</th>{columns}</tr></thead><tbody>'
            for idx,layer in enumerate(layers):
                cells=''.join(f'<td>{weights[idx]}</td>' for weights in options.values())
                body+=f'<tr><th scope="row">{layer}</th>{cells}</tr>'
            body+='</tbody><tfoot>'
            actions=[('sample',t('Muestra','Sample','索樣')),('quote',t('Cotizar','Quote','詢價'))]
            for kind,label in actions:
                buttons=''.join(f'<td>{request(key,kind,ref,label)}</td>' for ref in options)
                body+=f'<tr><th scope="row">{l[kind]}</th>{buttons}</tr>'
            body+='</tfoot></table></section>'
            q=t('¿14 o 20 g/m² de adhesivo?','14 or 20 g/m² of adhesive?','熱熔膠 14 或 20 g/m² 怎麼選？')
            ans=t('Compare A con B o C con D sobre el mismo envase, con la misma presión, temperatura y tiempo de reposo. El gramaje del adhesivo por sí solo no determina la adhesión al pelado.','Compare A with B or C with D on the same substrate, using the same application pressure, temperature and dwell time. Coat weight alone does not establish peel adhesion.','A 與 B、C 與 D 可分別在相同被貼物、貼標壓力、溫度與靜置時間下比較。塗膠量本身無法判定剝離黏著力。')
            body+=f'<aside><h3>{q}</h3><p>{ans}</p></aside>'
        unit='g/m²' if key in ('coated','thermal','woodfree') else 'μm'
        values=[(l['face'],f'{name} · {unit}'),(l['adh'],('Hot melt · g/m²' if key=='woodfree' else l['pending'])),
                (l['liner'],('Glassine · g/m²' if key=='woodfree' else l['pending'])),(l['TDS'],l['extra'])]
        body+=f'<section><h2>{l["specs"]}</h2><dl class="spec-table">'+''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in values)+'</dl>'
        body+=f'<div class="toc"><a href="{guide[i]}#adhesives">{t("Comparar adhesivos","Compare adhesives","比較膠種")}</a><a href="{guide[i]}#brief">{t("Medidas de bobina","Roll dimensions","母卷尺寸")}</a><button class="print-sheet" type="button">{t("Imprimir ficha de selección / PDF","Print selection sheet / PDF","列印選材單／另存 PDF")}</button></div></section>'
        trialheading=t('Prueba recomendada para esta aplicación','Trial for this application','此用途的試樣重點')
        record=t('Anote lote, equipo, superficie, temperatura y tiempo de reposo. Acuerde el criterio de aceptación antes de la prueba.','Log the lot, equipment, surface, temperature and dwell time. Agree the acceptance criteria before the trial.','記錄批號、設備、被貼物、溫度與靜置時間；試樣前先約定驗收條件。')
        body+=f'<section class="questions"><h2>{trialheading}</h2><div><p>{trials[key]}</p><p>{record}</p><a href="{guide[i]}#layers">{t("Guía técnica de la construcción","Labelstock construction guide","回到材料結構與技術指南")} →</a></div></section>'
        yield key,name,info,body
    flow=[(t('Selección del proveedor','Supplier selection','選廠'),t('Solicite identificación de la planta, ficha técnica y especificación de la construcción.','Request mill identification, a dated technical data sheet and a construction specification.','向供應商取得生產廠識別、技術資料表與材料結構規格。')),
          (t('Muestra de referencia','Reference sample','樣品確認'),t('Registre el código, la superficie de prueba y el resultado acordado antes del pedido.','Record the reference, test substrate and agreed acceptance criteria before ordering.','訂購前記錄樣品編號、試貼表面及雙方同意的驗收條件。')),
          (t('Inspección y trazabilidad','Inspection and traceability','驗貨與追溯'),t('Compare el lote con la muestra aprobada. Revise ancho, metraje y núcleo; guarde el número de lote por rollo.','Match the lot to the approved sample. Check width, length and core and record the lot for each roll.','將出貨批次與核准樣品比對，檢查幅寬、長度及紙管，逐卷記錄批號。')),
          (t('Embalaje y carga','Packing and loading','包裝與裝櫃'),t('Acuerde protección de cantos y humedad. Verifique pesos, marcas y lista de empaque antes de cargar.','Agree edge and moisture protection. Check weights, markings and the packing list before loading.','約定端面防護及防潮方式，裝運前核對重量、箱嘜與裝箱單。'))]
    intro=t('Puntos que el comprador y el proveedor deben acordar en una compra internacional de bobinas.','Checks for a buyer and supplier to agree when sourcing rolls internationally.','國際採購母卷時，買家與貿易供應商應逐項約定的查核內容。')
    yield 'sourcing',l['sourcing'],intro,f'<section><h1>{l["sourcing"]}</h1><p>{intro}</p><div class="options">'+''.join(f'<article><h3>{k}</h3><p>{v}</p></article>' for k,v in flow)+'</div></section>'
    heading=l['request']
    helptext=t('Elija el material y descargue su solicitud. El archivo se guarda en su dispositivo; envíelo a su contacto comercial. Este formulario no envía pedidos ni confirma muestras.','Choose a material and download your brief. The file is saved to your device for you to send to your sales contact. This form does not send orders or confirm samples.','選擇材料並下載需求單，檔案會儲存到你的裝置，再交給業務窗口。此表單不會自動寄送訂單或確認樣品。')
    def select(k,label,items):
        opts=''.join(f'<option value="{v}">{n}</option>' for v,n in items)
        return f'<label>{label}<select name="{k}">{opts}</select></label>'
    controls=select('mode',t('Solicitud','Request','需求'),[('sample',l['sample']),('quote',l['quote'])])
    controls+=select('material',l['face'],[('',t('Elegir material','Choose material','選擇材料')),*names.items()])
    controls+=select('option',t('Combinación','Construction','模造紙組合'),[('',l['pending'])]+[(k,k+' · '+'/'.join(map(str,v))+' g/m²') for k,v in options.items()])
    specs=[('sku',t('Referencia del proveedor (si se conoce)','Supplier SKU (if known)','供應商料號（如有）')),('width',t('Ancho útil','Usable width','可用幅寬')+' (mm)'),('length',t('Longitud','Roll length','卷長')+' (m)'),('diameter',t('Diámetro exterior máximo','Maximum roll OD','最大卷外徑')+' (mm)'),('core',t('Diámetro interior del núcleo','Core ID','紙管內徑')+' (mm)'),('quantity',t('Superficie requerida','Required area','需求面積')+' (m²)'),('port',t('País y puerto de destino','Destination country and port','目的國與港口')),('surface',t('Superficie de aplicación','Application surface','被貼物表面')),('press',fields[4]),('temperature',fields[2]),('test',fields[-1])]
    for k,n in specs:
        typ='type="number" min="0.01" step="any"' if k in ('width','length','diameter','core','quantity') else 'type="text"'
        controls+=f'<label>{n}<input name="{k}" {typ}></label>'
    yield 'request',heading,helptext,f'<section><h1>{heading}</h1><p>{helptext}</p><form id="inquiry"><div class="fieldgrid">{controls}</div><button class="button">{t("Descargar solicitud","Download request","下載需求單")} ↓</button></form></section>'
