"""Localized buyer guidance and discoverability for the existing catalog."""
from html import escape
from html.parser import HTMLParser
import json

UPDATED = '2026-11-19'
HREFLANG = ['es', 'en', 'zh-Hant']

# The site remains a selection/inquiry catalog. No inventory, certification,
# mill ownership or printer compatibility is inferred from third-party sources.
META = {
 'home': (
  ['Bobinas jumbo autoadhesivas para etiquetas | RolloBase', 'Labelstock jumbo rolls: paper, BOPP, PE & PET | RolloBase', '不乾膠母卷選材、規格比較與索樣 | RolloBase'],
  ['Compare papel semibrillo, térmico, BOPP, PE, PET y papel no estucado. Prepare muestras, cotizaciones por m² útil y controles de recepción.', 'Compare paper, thermal, BOPP, PE, PET and woodfree labelstock. Prepare sample requests, usable-area quotes and roll acceptance checks.', '比較銅版紙、熱感紙、BOPP、PE、PET 與模造紙不乾膠母卷。查看三層結構、A～D 規格、每可用平方米比價、索樣與卷長驗收。']),
 'guide': (
  ['Material autoadhesivo: frontal, adhesivo y liner | RolloBase', 'Labelstock layers, adhesives & release liners | RolloBase', '不乾膠母卷三層結構、膠水與離型底材指南 | RolloBase'],
  ['Entienda el frontal, el adhesivo y el soporte siliconado. Compare emulsión acrílica, hot melt y acrílico en disolvente para su etiqueta.', 'Understand facestock, adhesive and release liner. Compare emulsion acrylic, hot melt and solvent acrylic, application temperature and trial criteria.', '深入了解面材、感壓膠與離型底材，對照水膠、熱熔膠、油膠的選用重點，區分貼標溫度與使用溫度，再以實際容器試貼。']),
 'catalog': (
  ['Catálogo de materiales autoadhesivos en bobina | RolloBase', 'Labelstock material catalog & selection guide | RolloBase', '不乾膠母卷材料目錄與用途比較 | RolloBase'],
  ['Busque papel semibrillo, térmico directo, BOPP, PE, PET y papel no estucado. Compare aplicaciones y datos que debe confirmar por referencia.', 'Search coated paper, direct thermal, BOPP, PE, PET and woodfree labelstock. Compare applications and the specifications to confirm for each SKU.', '依材料、用途與參考組合搜尋銅版紙、熱感紙、BOPP、PE、PET 與模造紙。對照三層結構與待確認規格，進入對應產品索樣。']),
 'request': (
  ['Muestras y cotización de bobinas autoadhesivas | RolloBase', 'Labelstock sample rolls, MOQ & quote checklist | RolloBase', '不乾膠母卷索樣、MOQ 與每平方米報價 | RolloBase'],
  ['Prepare una solicitud por material y combinación A–D. Revise MOQ por referencia, ancho útil, metraje, equipo, destino y comparación por m².', 'Prepare a material-specific sample or quote brief. Check SKU MOQ, usable width, roll length, press, destination and cost per usable square metre.', '選擇材料與模造紙 A～D 組合，下載索樣或詢價需求單。確認料號 MOQ、幅寬、卷長、機型、目的港與每可用平方米價格。']),
 'sourcing': (
  ['Embalaje, metraje y recepción de bobinas | RolloBase', 'Labelstock export packing & roll length acceptance | RolloBase', '不乾膠母卷出口包裝、卷長驗收與短碼計算 | RolloBase'],
  ['Revise la lista de empaque por bobina, CBM, peso neto y bruto. Acuerde medición del metraje, tolerancias y cálculo de faltantes antes del pedido.', 'Check roll-level packing lists, pallet CBM and net/gross weight. Agree length measurement, tolerances and shortage calculations before ordering.', '逐卷核對料號、批號、裝箱單、棧板 CBM 與淨毛重。透過卷長複驗步驟及有條件算例，事先約定允差、短碼折讓和索賠資料。']),
 'quality': (
  ['TDS, COA y trazabilidad de material autoadhesivo | RolloBase', 'Labelstock TDS, COA & roll traceability checklist | RolloBase', '不乾膠母卷 TDS、COA 與逐卷品質追溯 | RolloBase'],
  ['Vincule lote, número de bobina, TDS y resultados de inspección. Sepa qué verificar en documentos FSC y declaraciones de uso alimentario.', 'Link batch, roll ID, TDS revision and inspection results. Learn what to check in FSC records and food-use documentation before approval.', '將批號、卷號、TDS 版本與 COA 檢驗結果串聯，查核 FSC 與食品用途文件的適用範圍，建立可追溯的採購紀錄。']),
 'printing': (
  ['Pruebas de impresión y compatibilidad de etiquetas | RolloBase', 'Labelstock printing compatibility & trial checklist | RolloBase', '不乾膠材料印刷相容性與試印驗證 | RolloBase'],
  ['Defina modelo, tinta o ribbon, referencia y ajustes antes de probar. Revise impresión, secado, códigos de barras, troquelado y aplicación.', 'Specify printer model, ink or ribbon, material SKU and settings. Check print, cure, barcodes, die-cutting and application before claiming compatibility.', '依精確機型、油墨或碳帶、材料料號與設定試印，檢查乾燥固化、條碼、模切排廢與實際試貼，保留相容性驗證紀錄。']),
 'woodfree': (
  ['Papel no estucado autoadhesivo: opciones A–D | RolloBase', 'Woodfree labelstock: compare A–D sample constructions | RolloBase', '模造紙不乾膠母卷 A～D 規格比較與索樣 | RolloBase'],
  ['Compare papel 60/70, hot melt 14/20 y glassine 50/60 g/m² en una tabla. Elija A, B, C o D y prepare su muestra; disponibilidad por confirmar.', 'Compare 60/70 gsm woodfree paper, 14/20 gsm hot melt and 50/60 gsm glassine in one table. Select A–D for a sample; supply requires confirmation.', '同表比較模造紙 60／70、熱熔膠 14／20、格拉辛底紙 50／60 g/m²，點選 A、B、C、D 直接準備索樣；供貨及允差待確認。']),
 'coated': (
  ['Papel semibrillo autoadhesivo en bobina | RolloBase', 'Semi-gloss coated paper labelstock jumbo rolls | RolloBase', '半光澤銅版紙不乾膠母卷與印刷選材 | RolloBase'],
  ['Papel semibrillo, estucado o couché para etiquetas de frascos y cajas. Confirme gramaje, adhesivo, liner y prueba de impresión antes de cotizar.', 'Semi-gloss coated paper for jar and retail carton labels. Confirm face grammage, adhesive, liner and print trial before requesting a quote.', '銅版紙適用於罐身與商品外盒標籤選材。確認面材克重、塗層、膠種及底紙，以實際油墨試印後再索樣與詢價。']),
 'thermal': (
  ['Papel térmico autoadhesivo Eco y Top | RolloBase', 'Direct thermal labelstock: Eco vs Top explained | RolloBase', '熱感紙不乾膠母卷 Eco／Top 差異與索樣 | RolloBase'],
  ['Distinga térmico directo de transferencia térmica, Eco de Top y papel sin adhesivo de etiquetas. Confirme protección, sensibilidad y adhesivo.', 'Compare direct thermal Eco and Top grades, ribbon requirements and adhesive construction. Confirm coating, sensitivity and storage requirements.', '比較熱感紙 Eco 與 Top 保護層、熱感與熱轉印差異，以及未上膠熱感紙與自黏標籤結構；依保存環境、感度和膠種索樣。']),
 'bopp': (
  ['BOPP autoadhesivo blanco y transparente | RolloBase', 'White & clear BOPP self-adhesive labelstock | RolloBase', '白色與透明 BOPP 不乾膠母卷選材 | RolloBase'],
  ['Compare BOPP blanco y transparente para botellas rígidas. Revise opacidad, claridad del adhesivo, tinta, tratamiento superficial y liner.', 'Compare white and clear BOPP for rigid bottle labels. Review opacity, adhesive clarity, ink anchorage, surface treatment and release liner.', '比較硬質瓶標用白色與透明 BOPP 膜，核對遮蔽性、膠層霧度、油墨附著、表面處理與離型底材，再進行結露試貼。']),
 'pe': (
  ['Película PE autoadhesiva para envases flexibles | RolloBase', 'PE labelstock for squeezable bottle labels | RolloBase', 'PE 不乾膠母卷與可擠壓瓶身標籤 | RolloBase'],
  ['Evalúe película de polietileno para envases que se comprimen. Pruebe curvatura, arrugas, adhesión y levantamiento de bordes sobre el envase lleno.', 'Evaluate polyethylene film for squeezable packaging. Test conformity, wrinkles, adhesion and edge lift on the actual filled container.', 'PE 聚乙烯膜用於可擠壓瓶身選材。以實際裝填容器評估服貼性、反覆擠壓、起皺與翹邊，再確認膜厚與膠種。']),
 'pet': (
  ['Película PET autoadhesiva para identificación | RolloBase', 'PET labelstock for durable identification labels | RolloBase', 'PET 不乾膠母卷與設備識別標籤 | RolloBase'],
  ['Evalúe poliéster para etiquetas de equipos y activos. Confirme adhesivo, impresión y resistencia bajo las condiciones reales de limpieza y calor.', 'Evaluate polyester for equipment and asset labels. Confirm adhesive, print and resistance under the actual cleaning and temperature conditions.', 'PET 聚酯膜用於設備與資產識別選材。分別確認面材、膠層與印刷系統，測試實際清潔劑、摩擦及使用溫度。']),
}

# Each question and answer is an ES / EN / Traditional Chinese triplet.
QA = {
 'catalog': [
  (['¿Cómo elegir papel semibrillo, térmico directo o BOPP?', 'How do I choose coated paper, direct thermal or BOPP?', '銅版紙、熱感紙與 BOPP 如何選？'],
   ['Empiece por el uso: gráficos en envases secos, papel semibrillo; datos variables sin ribbon, térmico directo; etiquetas de botellas rígidas, BOPP. Después confirme impresión, adhesivo, humedad y temperatura con una muestra.', 'Start with the application: coated paper for graphics on dry packs, direct thermal for variable data without a ribbon, and BOPP for rigid bottles. Then trial the printing, adhesive, moisture and temperature conditions.', '先看用途：乾燥包裝圖文可評估銅版紙，免碳帶可變資料可評估熱感紙，硬質瓶標可評估 BOPP；接著以樣品確認印刷、膠種、潮濕與溫度條件。']),
  (['¿Cómo confirmo las existencias?', 'How do I confirm stock availability?', '如何確認供貨狀態？'],
   ['El catálogo sirve para elegir el material y pedir cotización. Antes de confirmar el pedido, verifique por escrito la ficha técnica (TDS), el ancho, el metraje, las tolerancias, el pedido mínimo y la disponibilidad.', 'Use the catalog to select materials and request a quote. Confirm the TDS, roll width and length, tolerances, minimum order and availability in writing before order acceptance.', '此目錄供選材與詢價。接單前請以書面確認 TDS、幅寬、卷長、允差、起訂量及供貨狀態。']),
 ],
 'request': [
  (['¿Qué información necesita una muestra lista para probar?', 'What information is needed for a press-ready sample?', '索樣時要提供哪些資料？'],
   ['Indique material o combinación A–D, referencia si existe, ancho útil, longitud, núcleo, diámetro máximo, equipo y tinta o ribbon. Añada envase, temperaturas, criterio de aceptación y país de destino. Confirme por separado costo y envío de la muestra.', 'Specify the material or A–D construction, known SKU, usable width, length, core, maximum roll diameter, machine and ink or ribbon. Add the container, temperatures, acceptance criteria and destination country. Confirm sample and shipping charges separately.', '提供材料或 A～D 組合、已知料號、可用幅寬、卷長、紙管、最大外徑、機型及油墨或碳帶，再補充被貼物、溫度、驗收條件與目的國。樣品費和運費另行確認。']),
  (['¿Cómo comparar cotizaciones por m² útil?', 'How do I compare quotes per usable square metre?', '如何以每可用平方米比較報價？'],
   ['Área útil = ancho útil en metros × longitud útil en metros × número de bobinas. Divida el importe comparable entre esa área, con la misma construcción, moneda y costos incluidos. Ejemplo ilustrativo: 1 m × 1 000 m = 1 000 m²; USD 200 ÷ 1 000 = USD 0,20/m². No es una oferta.', 'Usable area = usable width in metres × usable length in metres × roll count. Divide the comparable charge by that area using the same construction, currency and included costs. Illustrative example: 1 m × 1,000 m = 1,000 m²; USD 200 ÷ 1,000 = USD 0.20/m². This is not a quote.', '可用面積＝可用幅寬（m）×可用卷長（m）×卷數，再以相同結構、幣別與費用範圍的金額除以面積。教學算例：1 m × 1,000 m＝1,000 m²；USD 200 ÷ 1,000＝USD 0.20/m²。這不是實際報價。']),
  (['¿Cuál es el MOQ y se pueden mezclar materiales?', 'What is the MOQ, and can materials share a trial pallet?', 'MOQ 與混棧板試單要怎麼確認？'],
   ['Solicite MOQ por referencia y por ancho, cantidad por bobina y condición de palé mixto. Los mínimos pueden depender de fabricación, corte y embalaje. Aún no hay un MOQ ni una política de mezcla confirmados en este catálogo.', 'Request MOQ by SKU and width, quantity per roll and mixed-pallet conditions. Minimums can depend on production, slitting and packing. This catalog does not yet state a confirmed MOQ or mixed-pallet policy.', '分別確認每個料號、每種幅寬的 MOQ、每卷數量與混棧板條件，並區分生產、分切及包裝限制。本目錄尚無已確認的 MOQ 或混棧板政策。']),
  (['¿Qué revisar en una oferta EXW o FOB?', 'What should an EXW or FOB quote specify?', 'EXW 與 FOB 報價應確認什麼？'],
   ['Indique regla, lugar o puerto y versión Incoterms® 2020. EXW pone la mercancía a disposición sin cargar ni despachar la exportación; FOB entrega a bordo en el puerto de embarque. Para contenedores, evalúe FCA. Desglose gastos con el proveedor.', 'State the rule, named place or port and Incoterms® 2020. EXW makes goods available without loading or export clearance; FOB delivers onboard at the shipment port. For containers, consider FCA. Confirm itemized charges with the supplier.', '寫明條件、具名地點或港口及 Incoterms® 2020。EXW 為備妥供提取，通常不含裝車與出口清關；FOB 在裝運港船上交貨。貨櫃運輸可評估 FCA，並逐項確認費用。']),
  (['¿Desde cuándo se cuenta el plazo?', 'When does the lead-time clock start?', '樣品、試單和回購交期從哪天起算？'],
   ['Separe preparación de muestra, fabricación, inspección, salida y transporte. Confirme el inicio: aprobación de especificaciones, pago o muestra aceptada. Indique días naturales o hábiles. Los plazos se confirman por pedido.', 'Separate sample preparation, manufacturing, inspection, dispatch and transit. Confirm whether timing starts with specification approval, payment or sample approval, and whether days are calendar or working days. Lead times require order-level confirmation.', '將備樣、生產、檢驗、出貨與運輸分開，確認從規格核准、付款或樣品認可哪一天起算，並註明日曆日或工作日。實際交期須按訂單確認。']),
 ],
 'sourcing': [
  (['¿Qué debe contener la lista de empaque por bobina?', 'What belongs on a roll-level packing list?', '逐卷裝箱單應記錄哪些欄位？'],
   ['Relacione pedido, referencia, lote, número de bobina y palé. Registre ancho, longitud, cantidad, pesos, dimensiones del bulto y marcas. Haga coincidir cantidades e identificación con la factura y los documentos de inspección.', 'Link order, SKU, batch, roll ID and pallet. Record width, length, quantity, weights, package dimensions and marks. Reconcile quantities and identification with the invoice and inspection documents.', '串聯訂單、料號、批號、卷號與棧板號，記錄幅寬、卷長、數量、重量、包裝尺寸及箱嘜；再與發票及檢驗資料核對。']),
  (['¿Cómo calcular CBM y distinguir peso neto y bruto?', 'How do I calculate CBM and distinguish net/gross weight?', '棧板 CBM、淨重與毛重如何計算？'],
   ['CBM = largo × ancho × alto exterior, en metros, sumado por bulto. Ejemplo ilustrativo: 1,20 × 1,00 × 1,10 = 1,32 m³. El peso bruto incluye embalaje y palé. Declare por separado la tara y si el núcleo está incluido en el peso neto acordado.', 'CBM = external length × width × height in metres, summed across packages. Illustrative example: 1.20 × 1.00 × 1.10 = 1.32 m³. Gross weight includes packing and pallet. State tare separately and agree whether cores are included in the reported net roll weight.', 'CBM＝包裝後外長×外寬×外高（m），各件加總。教學算例：1.20 × 1.00 × 1.10＝1.32 m³。毛重包含包材與棧板，另列皮重，並事先約定卷材淨重是否含紙管。']),
  (['¿Cómo volver a medir un posible faltante de metros?', 'How should a suspected short roll be remeasured?', '懷疑短碼時，如何複驗卷長？'],
   ['Conserve rollo, etiqueta y fotos. Acorde medición, calibración del contador, tensión y definición de longitud útil. Anote empalmes, desperdicio acordado y resultados por bobina; invite a ambas partes a revisar el registro. Peso o diámetro solos no prueban el metraje.', 'Retain the roll, label and photos. Agree the measurement method, counter calibration, tension and usable-length definition. Log splices, agreed waste and roll-level results for joint review. Weight or diameter alone does not prove the delivered length.', '保留卷材、卷標與照片，約定量測方法、計米器校正、張力及可用長度定義。逐卷記錄接頭、約定損耗與量測結果，交由雙方複核。只看重量或外徑不足以證明實際卷長。']),
  (['¿Cómo calcular un abono por faltante?', 'How can a shortage credit be calculated?', '短碼折讓如何算，允差怎麼處理？'],
   ['Si el contrato acepta abonar todo el faltante verificado: abono = metros faltantes aceptados × ancho facturable en m × precio por m². Ejemplo: (1 000 − 980) × 1 × USD 0,20 = USD 4. La tolerancia, los empalmes, el flete y el plazo de reclamación se acuerdan aparte; el ejemplo no crea una política de compensación.', 'If the contract credits the full accepted shortage: credit = accepted missing metres × billable width in m × price per m². Example: (1,000 − 980) × 1 × USD 0.20 = USD 4. Agree tolerance, splices, freight and claim deadline separately; this example does not establish a compensation policy.', '若合約約定對已接受的短少長度全額折讓：折讓額＝雙方確認短少米數×計價幅寬（m）×每 m² 單價。算例：(1,000−980) × 1 × USD 0.20＝USD 4。允差、接頭、運費及索賠期限須另約定，算例不代表賠償政策。']),
  (['¿Cómo proteger las bobinas durante el transporte?', 'How should rolls be protected in transit?', '出口包裝如何降低受潮與端面壓傷？'],
   ['Acuerde barrera contra humedad, protección de cantos, sujeción sin deformación y límites de apilado. Fotografíe antes de cerrar y cargar. Registre daños y condición de recepción antes de retirar embalajes. El diseño debe validarse con peso, ruta y almacenamiento reales.', 'Agree moisture protection, edge guards, restraint that avoids distortion and stacking limits. Photograph before closing and loading. Record receipt condition before removing packing. Validate the design against actual weight, route and storage conditions.', '約定防潮層、端面護板、避免變形的固定方式及堆疊限制。封裝與裝運前拍照，到貨拆包前記錄外觀。包裝設計需按實際重量、運輸路線及倉儲條件驗證。']),
  (['¿Qué comprobar sobre el proveedor?', 'What should I verify about the supplier?', '採購前要核實哪些供應商資訊？'],
   ['Verifique razón social, domicilio, beneficiario de pago y si actúa como fabricante o distribuidor. Pida evidencia de la relación con la planta, aprobación de muestra y especificación firmada. Una fotografía de referencia no acredita una fábrica propia.', 'Verify legal name, address, payment beneficiary and manufacturer/distributor role. Request evidence of the mill relationship, approved sample and signed specification. A reference photograph does not establish factory ownership.', '核對公司法定名稱、地址、收款主體及製造商／經銷商角色，取得生產廠關係證據、核准樣品與簽認規格。參考照片不能作為自有工廠證明。']),
 ],
 'quality': [
  (['¿Cómo vincular bobina, lote, TDS y COA?', 'How do roll ID, batch, TDS and COA connect?', '卷號、批號、TDS 與 COA 要如何串聯？'],
   ['Registre pedido → referencia → lote → número de bobina. Vincule la versión de TDS y el COA o informe de inspección del lote. La TDS describe la especificación; el COA debe identificar el lote y los resultados declarados. Compruebe que ambos documentos corresponden a la misma construcción.', 'Record order → SKU → batch → roll ID. Link the TDS revision and batch COA or inspection report. The TDS describes the specification; the COA should identify the batch and reported results. Check that both refer to the same construction.', '建立訂單→料號→批號→卷號對照，再連結 TDS 版本與該批 COA／檢驗報告。TDS 說明規格；COA 應識別批次及所申報的檢驗結果。兩者都需對應同一材料結構。']),
  (['¿Qué debe incluir un informe de ensayo?', 'What should a trial report record?', '試樣報告要記錄哪些條件？'],
   ['Solicite método y versión, unidades, probetas, acondicionamiento, superficie, temperatura, tiempo de reposo y criterio de aceptación. Separe adhesión al pelado, tack y resistencia al cizallamiento. Añada impresión, roce y lectura de código según la aplicación; no compare valores obtenidos con condiciones distintas.', 'Request method/version, units, specimens, conditioning, surface, temperature, dwell time and acceptance criteria. Separate peel, tack and shear results. Add print, rub and barcode checks for the application; results from different conditions are not directly comparable.', '索取方法及版本、單位、試片、調濕、被貼物、溫度、靜置時間與驗收條件。剝離、初黏及持黏分別記錄，再依用途加入印面、耐磨與條碼檢查；不同條件的數值不可直接比較。']),
  (['¿Cómo revisar una declaración FSC?', 'How do I check an FSC claim?', '如何查核特定料號的 FSC 聲明？'],
   ['Busque al titular y el código en el registro oficial FSC. Revise vigencia y alcance, y solicite la declaración correspondiente en la documentación del producto. Este catálogo no declara que RolloBase ni sus materiales estén certificados.', 'Check the holder and code in the official FSC record. Review validity and scope, and request the applicable product claim in the transaction documents. This catalog does not claim FSC certification for RolloBase or its materials.', '在 FSC 官方資料庫核對持有人、代碼、有效狀態與範圍，再索取該產品交易文件上的適用聲明。本目錄未宣稱 RolloBase 或所列材料已取得 FSC 認證。']),
  (['¿Qué confirmar para un envase de alimentos?', 'What should I confirm for food packaging?', '食品包裝標籤應先確認哪些文件？'],
   ['Declare país de venta, alimento, contacto previsto, tiempo y temperatura. Solicite documentación para la construcción completa, incluida la impresión. Una referencia normativa o la declaración de un adhesivo no demuestra por sí sola la aptitud de la etiqueta final.', 'Specify destination market, food, intended contact, duration and temperature. Request documentation for the full construction, including printing. A regulation reference or adhesive statement alone does not establish suitability of the finished label.', '先說明銷售地、食品、預期接觸方式、時間與溫度，再索取涵蓋完整結構及印刷的文件。只有法規名稱或單一膠水聲明，無法單獨證明成品標籤適用。']),
 ],
 'printing': [
  (['¿Cuándo se puede afirmar compatibilidad?', 'When can printer compatibility be claimed?', '什麼情況才能宣稱材料與機型相容？'],
   ['Cuando existe una prueba documentada para el modelo y versión exactos, la referencia del material, la tinta o ribbon y los ajustes usados. Registre fecha y límites de la prueba. El nombre BOPP, PE o PET por sí solo no confirma compatibilidad.', 'After a documented trial for the exact machine/model variant, material SKU, ink or ribbon and settings. Record the date and limits of the trial. The material name BOPP, PE or PET alone does not establish compatibility.', '需有精確機型與版本、材料料號、油墨或碳帶及使用設定的實測紀錄，並註明日期與測試範圍。只寫 BOPP、PE 或 PET，不能證明相容性。']),
  (['¿Térmico directo o transferencia térmica?', 'Direct thermal or thermal transfer?', '熱感列印與熱轉印需要什麼耗材？'],
   ['El térmico directo forma la imagen en un frontal termosensible, sin ribbon. La transferencia térmica usa ribbon sobre una superficie compatible. Confirme modo, recubrimiento y ajustes en la documentación del equipo y haga una prueba.', 'Direct thermal forms an image on heat-sensitive media without a ribbon. Thermal transfer uses a ribbon on compatible media. Confirm the mode, coating and settings in the machine documentation and run a trial.', '熱感列印在感熱面材上受熱顯色，不用碳帶；熱轉印以碳帶轉印至相容面材。依設備文件確認列印模式、表面塗層與設定，再進行試印。']),
  (['¿Qué revisar en BOPP para inkjet, UV o flexografía?', 'What should BOPP trials check for inkjet, UV or flexo?', 'BOPP 噴墨、UV 或柔印要測什麼？'],
   ['Confirme recubrimiento receptor o tratamiento superficial para la tinta elegida y si el proceso requiere primer. Registre velocidad, secado o curado y antigüedad del material. Compruebe anclaje, roce, aspecto con humedad y troquelado; en transparente, incluya la capa de blanco si se utiliza.', 'Confirm the receptive coating or surface treatment for the chosen ink, and whether the process requires primer. Record speed, drying or curing and material age. Check ink anchorage, rub, wet appearance and die-cutting; include white ink in clear-film trials when used.', '確認選定油墨所需的吸墨塗層或表面處理，以及製程是否需要底塗。記錄速度、乾燥固化及材料存放時間，檢查油墨附著、耐磨、受潮外觀與模切；透明膜若使用白墨，須一起測試。']),
 ],
 'thermal': [
  (['¿Qué diferencia hay entre Eco y Top?', 'What is the difference between Eco and Top?', '熱感紙 Eco 與 Top 有何差異？'],
   ['Eco suele designar papel térmico sin capa protectora adicional; Top incorpora protección superficial. Confirme en la TDS qué caras están protegidas y pruebe agua, roce y condiciones de almacenamiento. Eco no significa automáticamente ecológico.', 'Eco generally denotes thermal paper without an additional protective coat; Top includes surface protection. Check which sides are coated in the TDS and test water, rub and storage exposure. Eco does not automatically mean environmentally certified.', 'Eco 通常指未加額外保護層的熱感紙，Top 則有保護塗層；應按 TDS 確認正反面保護方式，實測水、摩擦與保存條件。Eco 名稱不等於環保認證。']),
  (['¿Papel térmico sin adhesivo y autoadhesivo son iguales?', 'Are non-adhesive thermal paper and labelstock the same?', '未上膠熱感紙和熱感標籤母卷一樣嗎？'],
   ['No. El papel térmico sin adhesivo conserva su capa termosensible, pero no es la construcción de frontal, adhesivo y liner de esta página. Aquí se consulta material autoadhesivo; el suministro de papel sin adhesivo no está confirmado.', 'No. Non-adhesive thermal paper still has its heat-sensitive layer, but is not the facestock/adhesive/liner construction shown here. This page covers self-adhesive labelstock; non-adhesive paper supply is not confirmed.', '不一樣。未上膠熱感紙仍有感熱層，但不等於本頁面材、膠層與底材的自黏結構。本頁供不乾膠選材詢問，未上膠熱感原紙供貨尚未確認。']),
 ],
 'bopp': [
  (['¿BOPP blanco o transparente?', 'White or clear BOPP?', '白色 BOPP 與透明 BOPP 如何選？'],
   ['Use una muestra blanca para evaluar cobertura del envase y una transparente para ver el contenido. Compare opacidad o claridad, burbujas, adhesivo y tinta blanca sobre la botella real. Elija por resultado visual y de aplicación, no solo por el nombre de la película.', 'Trial white film for container coverage and clear film where the contents should remain visible. Compare opacity or clarity, bubbles, adhesive and white ink on the actual bottle. Choose based on the finished appearance and application result.', '需要遮蔽瓶身底色時試白膜，希望透出內容物時試透明膜；在實際瓶身比較遮蔽性或透明度、氣泡、膠層與白墨效果，再依成品外觀及貼附結果選型。']),
  (['¿PET o glassine como liner?', 'PET or glassine release liner?', 'BOPP 面材可以搭配 PET 或格拉辛底材嗎？'],
   ['El frontal y el liner se seleccionan por separado. Confirme el código de la construcción y pruebe despegue, troquelado, detección y tensión con su equipo. No deduzca el liner a partir del nombre BOPP; las combinaciones disponibles requieren confirmación.', 'Facestock and liner are separate choices. Confirm the construction code and test release, die-cutting, sensing and tension on your equipment. Do not infer the liner from the word BOPP; available combinations require confirmation.', '面材與離型底材需分開選擇。確認結構料號後，以設備測試離型、模切、感測及張力；不能由 BOPP 名稱推定底材，實際可供搭配仍需確認。']),
 ],
 'coated': [
  (['¿Papel semibrillo, couché y papel ilustración son equivalentes?', 'Do semi-gloss and coated paper mean the same specification?', '銅版紙、半光紙與 couché 是否代表相同規格？'],
   ['Son términos comerciales que pueden variar según el mercado. En la consulta indique acabado, gramaje, adhesivo, liner y una muestra de referencia. El nombre semibrillo o couché no sustituye una TDS de la construcción completa.', 'Commercial terms vary by market. Specify finish, grammage, adhesive, liner and a reference sample. The words semi-gloss or coated paper do not replace a TDS for the complete construction.', '不同市場的商業名稱可能不一致。詢價時同時列明表面光澤、克重、膠種、底材與參考樣品；銅版紙或半光紙名稱不能取代完整結構的 TDS。']),
 ],
 'pe': [
  (['¿Cómo probar una etiqueta para un envase que se comprime?', 'How should a squeezable-bottle label be trialled?', '可擠壓瓶標應如何試樣？'],
   ['Pruebe el envase lleno, con la curvatura y panel reales. Registre tiempo de reposo, temperatura y ciclos de compresión; observe arrugas, recuperación y bordes. Confirme por separado película, tinta y adhesivo.', 'Use the filled pack and its actual curved panel. Record dwell time, temperature and squeeze cycles; inspect wrinkles, recovery and edges. Confirm the film, ink and adhesive separately.', '以裝填後的實際瓶身和曲面試貼，記錄靜置時間、溫度與擠壓次數，觀察皺褶、回彈及翹邊，並分別確認面膜、油墨與膠層。']),
 ],
 'pet': [
  (['¿PET garantiza resistencia al calor o a productos químicos?', 'Does PET alone guarantee heat or chemical resistance?', 'PET 面材是否就能保證耐熱、耐化學品？'],
   ['No. Evalúe la etiqueta completa: película, adhesivo, impresión y protección superficial. Pruebe los líquidos, tiempos y temperaturas reales sobre el acabado del equipo; solicite resultados para la referencia elegida.', 'No. Assess the complete label: film, adhesive, printing and surface protection. Test the actual fluids, durations and temperatures on the equipment finish and request results for the chosen SKU.', '不能。應評估面膜、膠層、印刷及表面保護的完整標籤；以設備實際塗裝面、液體、接觸時間與溫度試驗，索取所選料號的結果。']),
 ],
 'woodfree': [
  (['¿Las opciones A–D están en stock?', 'Are A–D available from stock?', 'A～D 有現貨嗎？'],
   ['A–D identifican combinaciones para solicitar prueba y cotización. Confirme tolerancias, disponibilidad y TDS antes de ordenar. Los valores de la tabla son gramajes por capa, no espesores.', 'A–D identify constructions for sample and quote requests. Confirm tolerances, availability and TDS before ordering. The table values are layer grammages, not thicknesses.', 'A～D 是用於索樣與詢價的組合代號。下單前須確認允差、供貨與 TDS。表格數值是各層克重，不是厚度。']),
 ],
}

SOURCES = {
 'request': [('ICC: Incoterms® 2020', 'https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/'), ('ICC: choosing a rule', 'https://library.iccwbo.org/content/clp/Others/incoterms_2020_checklist_2024-update.pdf')],
 'sourcing': [('International Trade Administration: export documents', 'https://www.trade.gov/common-export-documents')],
 'quality': [('FSC: certificate search', 'https://connect.fsc.org/fsc-public-certificate-search'), ('European Commission: food contact materials', 'https://food.ec.europa.eu/food-safety/chemical-safety/food-contact-materials/legislation_en')],
 'printing': [('Zebra: direct thermal and thermal transfer', 'https://cpws.zebra.com/cpws/docs/general/direct_thermal.htm'), ('UPM: digital printing materials', 'https://www.adhesivematerials.upm.com/label-solutions/label-types/digital-printing/')],
 'thermal': [('HERMA: Eco and Top thermal labels', 'https://www.herma.com/label/products/thermal-labels-on-rolls/')],
}

def questions(key, i):
    return [(q[i], a[i]) for q, a in QA.get(key, [])]

def faq_section(key, i):
    pairs = questions(key, i)
    if not pairs:
        return ''
    title = ['Preguntas para decidir y comprar', 'Questions before selecting and buying', '選材與採購問答'][i]
    answers = ''.join(f'<article><h3>{escape(q)}</h3><p>{escape(a)}</p></article>' for q,a in pairs)
    refs = ''.join(f'<li><a href="{escape(url)}">{escape(label)}</a></li>' for label,url in SOURCES.get(key, []))
    if refs:
        note = ['Referencias generales. No acreditan suministro, certificación ni compatibilidad de los materiales de RolloBase.', 'General references. They do not establish supply, certification or compatibility of RolloBase materials.', '一般選材參考，不代表 RolloBase 材料的供貨、認證或相容性證明。'][i]
        refs = f'<div class="source-note"><p>{note}</p><ul>{refs}</ul></div>'
    return f'<section id="buyer-answers" class="buyer-answers"><h2>{title}</h2><div class="answer-grid">{answers}</div>{refs}</section>'

def metadata(key, i):
    titles, descriptions = META[key]
    return titles[i], descriptions[i]

def enrich(key, i, body, routes, home, guide):
    t = lambda es,en,zh: [es,en,zh][i]
    if key == 'home':
        destinations = [('request',t('Muestras y costo por m²','Samples and cost per m²','索樣與每平方米比價')), ('sourcing',t('Embalaje y recepción','Packing and acceptance','包裝與卷長驗收')), ('quality',t('TDS, COA y trazabilidad','TDS, COA and traceability','TDS、COA 與品質追溯')), ('printing',t('Pruebas de impresión','Printing trials','印刷相容性試驗'))]
        cards = ''.join(f'<a class="appcard" href="{routes[k][i]}"><h3>{label}</h3></a>' for k,label in destinations)
        lead = t('Del material a una especificación verificable', 'From material choice to a verifiable specification', '從選材到可驗證的採購規格')
        text = t('Una bobina jumbo combina frontal, adhesivo y liner. Compare seis familias, confirme los datos de cada referencia y conserve el mismo código desde la muestra hasta la recepción.', 'A labelstock jumbo roll combines facestock, adhesive and release liner. Compare six material families, confirm each SKU and use the same reference from trial through receipt.', '不乾膠母卷結合面材、感壓膠與離型底材。比較六類材料，逐料號確認規格，並以同一組合代號串聯索樣、報價與到貨驗收。')
        hub = f'<section id="buyer-guides"><h2>{lead}</h2><p class="section-intro">{text}</p><div class="appgrid buyer-hub">{cards}</div><p class="section-intro"><a href="{routes["woodfree"][i]}#compare">{t("Comparar las opciones A–D de papel no estucado", "Compare woodfree constructions A–D", "查看模造紙 A～D 同表比較")} →</a></p></section>'
        body = body.replace('<section id="materials">', hub+'<section id="materials">', 1)
    body += faq_section(key, i)
    if key in ('coated','thermal','bopp','pe','pet','woodfree','guide','catalog'):
        title=t('Datos que debe confirmar antes de comprar','Specifications to confirm before ordering','下單前應確認的規格')
        text=t('Solicite la ficha técnica vigente (TDS), ancho y longitud, tolerancias, temperatura mínima de aplicación, rango de servicio y condiciones de conservación. Los datos aún no verificados se mantienen por confirmar.', 'Request the current TDS, width/length, tolerances, minimum application temperature, service range and storage conditions. Unverified values remain subject to confirmation.', '索取現行 TDS、寬長、允差、最低貼標溫度、使用溫度範圍及儲存條件。未經核實的數值仍須逐項確認。')
        body+=f'<section class="record-callout"><h2>{title}</h2><p>{text}</p><div class="toc"><a href="{routes["quality"][i]}">{t("Documentos y trazabilidad","Documents and traceability","文件與品質追溯")}</a><a href="{routes["printing"][i]}">{t("Plan de prueba de impresión","Printing trial checklist","印刷試驗清單")}</a></div></section>'
    body+=f'<p class="updated">{t("Contenido revisado", "Content reviewed", "內容更新")}：<time datetime="{UPDATED}">{UPDATED}</time></p>'
    return body

def new_pages(i, routes, home):
    t=lambda es,en,zh:[es,en,zh][i]
    for key in ('quality','printing'):
        heading = {'quality':t('Documentos de calidad y trazabilidad por bobina', 'Quality documents and roll traceability', '品質文件與逐卷追溯'), 'printing':t('Validar la impresión antes de comprar', 'Validate printing before buying', '採購前的印刷相容性驗證')}[key]
        intro = META[key][1][i]
        body=f'<p class="crumb"><a href="{home[i]}">{t("Inicio","Home","首頁")}</a> / {heading}</p><section class="buy-head"><div><h1>{heading}</h1><p>{intro}</p></div><a class="button" href="{routes["request"][i]}">{t("Preparar una prueba", "Prepare a trial", "準備試樣需求")}</a></section>'
        if key=='quality':
            text=t('Esta página indica qué solicitar y verificar. Todavía no se publican TDS de proveedor, COA de lote ni certificados propios.', 'This page explains what to request and verify. Supplier TDS, batch COAs and company certificates have not yet been published here.', '本頁說明應索取及核對的資料，目前尚未提供供應商 TDS、批次 COA 或公司證書下載。')
            body+=f'<aside><p>{text}</p></aside>'
        else:
            steps=[t('Identificar equipo, versión y proceso.', 'Identify machine, variant and process.', '識別設備、版本與印刷方式。'), t('Fijar material, lote, tinta o ribbon y ajustes.', 'Fix material, batch, ink or ribbon and settings.', '確認材料、批次、油墨或碳帶及設定。'), t('Imprimir, secar o curar y revisar el acabado.', 'Print, dry or cure and inspect the finish.', '試印、乾燥或固化後檢查印面。'), t('Probar conversión, aplicación y lectura del código.', 'Test converting, application and barcode readability.', '測試加工排廢、試貼及條碼讀取。'), t('Registrar resultados, límites y aprobación.', 'Record results, limits and approval.', '記錄結果、限制與核准結論。')]
            body+='<section class="trial-steps"><h2>'+t('Un registro para repetir la prueba','A repeatable trial record','可重複執行的試驗紀錄')+'</h2><ol>'+''.join(f'<li>{s}</li>' for s in steps)+'</ol></section>'
        yield key, heading, intro, body

class VisibleFAQ(HTMLParser):
    """Read only existing summary/paragraph FAQ pairs to keep JSON-LD literal."""
    def __init__(self):
        super().__init__(); self.q=None; self.a=None; self.capture=None; self.pairs=[]
    def handle_starttag(self, tag, attrs):
        if tag=='summary': self.q=''; self.capture='q'
        if tag=='p' and self.q is not None: self.a=''; self.capture='a'
    def handle_data(self, data):
        if self.capture: setattr(self,self.capture,getattr(self,self.capture)+data)
    def handle_endtag(self, tag):
        if tag in ('summary','p'): self.capture=None
        if tag=='details':
            if self.q and self.a: self.pairs.append((self.q.strip(),self.a.strip()))
            self.q=self.a=None

def structured_data(key,i,title,desc,url,origin,home,body):
    root=origin+'/'
    page={'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':['es-419','en','zh-Hant'][i],'dateModified':UPDATED,'isPartOf':{'@id':root+'#website'}}
    graph=[{'@type':'WebSite','@id':root+'#website','url':root,'name':'RolloBase','inLanguage':['es','en','zh-Hant']},page]
    if key!='home':
        graph.append({'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':['Inicio','Home','首頁'][i],'item':home},{'@type':'ListItem','position':2,'name':title.removesuffix(' | RolloBase'),'item':url}]})
        page['breadcrumb']={'@id':url+'#breadcrumb'}
    existing=VisibleFAQ();existing.feed(body)
    pairs=existing.pairs+questions(key,i)
    if pairs:
        graph.append({'@type':'FAQPage','@id':url+'#questions','inLanguage':page['inLanguage'],'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in pairs]})
        page['hasPart']={'@id':url+'#questions'}
    return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)
