"""Buyer specifications for semi-gloss paper and BOPP in the five site languages."""
from html import escape

from design_update import COPY, replace_once


# Spanish, English, Traditional Chinese, Russian, Simplified Chinese.
APPLICATION = (
    'Aplicación y condiciones de uso',
    'Application and service conditions',
    '用途與使用條件',
    'Применение и условия эксплуатации',
    '用途与使用条件',
)

ADHESIVE = (
    'Confirme la referencia del adhesivo y su gramaje de recubrimiento si está especificado. '
    'Verifique por separado la temperatura mínima de aplicación y el rango de servicio.',
    'Confirm the adhesive grade and coat weight where specified. '
    'Check minimum application temperature and service temperature range separately.',
    '確認膠黏劑料號及已列明的塗膠量，並分別核對最低貼標溫度與貼標後的使用溫度範圍。',
    'Уточните марку клея и массу покрытия, если она указана. '
    'Отдельно проверьте минимальную температуру нанесения и диапазон рабочих температур.',
    '确认胶黏剂料号及已列明的涂胶量，并分别核对最低贴标温度与贴标后的使用温度范围。',
)

PRODUCTS = {
    'coated': {
        'face': (
            'Papel estucado semibrillo (semigloss). Pida gramaje en g/m², tolerancia y acabado por referencia.',
            'Semi-gloss coated paper. Confirm grammage in g/m², tolerance, and finish for the specific grade.',
            '半光銅版紙。按料號確認面材克重（g/m²）、允差與表面光澤。',
            'Полуглянцевая мелованная бумага. Уточните массу в г/м², допуск и вид отделки по артикулу.',
            '半光铜版纸。按料号确认面材克重（g/m²）、公差与表面光泽。',
        ),
        'liner': COPY['liner_pending'],
        'application': (
            'Para evaluar etiquetas a color en cajas o frascos secos, indique la superficie, el acabado '
            'y las condiciones de uso. Avise si habrá sobreimpresión de datos variables.',
            'For color labels on dry cartons or jars, specify the actual surface, finish, and use conditions. '
            'Note whether variable data will be overprinted.',
            '試作乾燥紙盒或瓶罐的彩色標籤時，請提供實際表面、加工方式及使用條件。若需補印可變資料，請一併說明。',
            'Для цветных этикеток на сухих коробках или банках укажите фактическую поверхность, '
            'отделку и условия эксплуатации. Сообщите, если потребуется допечатка переменных данных.',
            '试做干燥纸盒或瓶罐的彩色标签时，请提供实际表面、加工方式及使用条件。如需加印可变数据，请一并说明。',
        ),
        'tests': (
            'Pruebe texto fino, áreas de color sólido y lectura del código en su equipo. '
            'Pida la ficha técnica (TDS) vigente de la construcción y registre el lote de prueba.',
            'Trial fine text, solid color patches, and barcode readability on your equipment. '
            'Request the current technical data sheet (TDS) for the construction and record the trial lot.',
            '用實際設備試印細字、實地色塊與條碼，確認掃讀。索取該材料結構的現行技術資料表（TDS），並記錄試樣批號。',
            'Проверьте мелкий текст, сплошные плашки и считывание штрихкода на своём оборудовании. '
            'Запросите актуальный технический паспорт (TDS) для выбранной структуры и запишите номер пробной партии.',
            '用实际设备试印细字、实地色块和条码，确认扫码结果。索取该材料结构的现行技术数据表（TDS），并记录试样批号。',
        ),
    },
    'bopp': {
        'face': (
            'Indique BOPP blanco o transparente. Pida espesor nominal en μm, tolerancia y tratamiento '
            'de la cara de impresión por referencia.',
            'Specify white or clear BOPP. Confirm nominal thickness in μm, tolerance, '
            'and print surface treatment for the specific grade.',
            '先選白色或透明 BOPP，按料號確認標稱厚度（μm）、允差與印刷面處理。',
            'Укажите белую или прозрачную плёнку БОПП. Уточните номинальную толщину в мкм, '
            'допуск и обработку поверхности под печать по артикулу.',
            '先选白色或透明 BOPP，按料号确认标称厚度（μm）、公差与印刷面处理。',
        ),
        'liner': (
            'Confirme si la referencia lleva glassine o PET, su gramaje o espesor y su fuerza de desprendimiento. '
            'Pruebe el troquelado y el sensor de la etiquetadora.',
            'Confirm whether the grade uses glassine or PET, its grammage or thickness, and release force. '
            'Test die-cutting and labeler sensor detection.',
            '按料號確認是否使用格拉辛底紙或 PET 底膜、克重或厚度及離型力，並驗證模切與貼標機感測。',
            'Уточните тип подложки по артикулу (глассин или ПЭТ), массу или толщину и усилие отделения. '
            'Проверьте высечку и срабатывание датчика этикетировщика.',
            '按料号确认是否使用格拉辛底纸或 PET 底膜、克重或厚度及离型力，并验证模切和贴标机传感器检测。',
        ),
        'application': (
            'Indique material y forma del envase. Pruebe por separado etiquetar una botella seca antes de refrigerarla '
            'y etiquetar una botella fría con condensación.',
            'Specify the container material and shape. Test labeling a dry bottle before refrigeration separately '
            'from labeling a cold bottle with condensation.',
            '提供容器材質與形狀。「乾燥瓶身貼標後再冷藏」與「瓶身已冰冷結露才貼標」分開測試。',
            'Укажите материал и форму тары. Проверьте отдельно нанесение на сухую бутылку до охлаждения '
            'и нанесение на холодную бутылку с конденсатом.',
            '提供容器材质与形状。「干燥瓶身贴标后再冷藏」与「瓶身已低温且有冷凝水时贴标」分开测试。',
        ),
        'tests': (
            'En el envase real, revise cobertura o claridad, bordes y adherencia de la tinta. '
            'Pida la ficha técnica (TDS) vigente de la construcción y registre el lote de prueba.',
            'On the actual package, check coverage or clarity, edge lift, and ink adhesion. '
            'Request the current technical data sheet (TDS) for the construction and record the trial lot.',
            '在實際容器上檢查遮蔽或清晰度、翹邊與油墨附著。索取該材料結構的現行技術資料表（TDS），並記錄試樣批號。',
            'На реальной таре проверьте укрывистость или прозрачность, отслоение краёв и закрепление краски. '
            'Запросите актуальный технический паспорт (TDS) для выбранной структуры и запишите номер пробной партии.',
            '在实际容器上检查遮盖或清晰度、翘边与油墨附着。索取该材料结构的现行技术数据表（TDS），并记录试样批号。',
        ),
    },
}


def apply_buyer_specifications(dist, groups):
    """Update only the specification lists and return the affected page names."""
    changed = set()
    for product, details in PRODUCTS.items():
        for index, filename in enumerate(groups[product]):
            rows = (
                (COPY['face'][index], details['face'][index]),
                (COPY['adhesive'][index], ADHESIVE[index]),
                (COPY['liner'][index], details['liner'][index]),
                (COPY['dimensions'][index], COPY['roll_details'][index]),
                (APPLICATION[index], details['application'][index]),
                (COPY['tests'][index], details['tests'][index]),
            )
            markup = '<dl class="spec-table">' + ''.join(
                f'<dt><span class="spec-number">{number}</span>{escape(label)}</dt><dd>{escape(value)}</dd>'
                for number, (label, value) in enumerate(rows, 1)
            ) + '</dl>'
            path = dist / filename
            before = path.read_text(encoding='utf-8')
            after = replace_once(
                r'(<section class="product-specs"><h2>[^<]*</h2>)<dl class="spec-table">.*?</dl>',
                lambda match: match[1] + markup,
                before,
            )
            if after != before:
                path.write_text(after, encoding='utf-8')
                changed.add(filename)
    return changed
