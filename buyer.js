const searchBox = document.querySelector('#lookup')
if (searchBox) {
  const cards = [...document.querySelectorAll('[data-search]')]
  const normalize = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
  searchBox.addEventListener('input', () => {
    const terms = normalize(searchBox.value.trim()).split(/\s+/)
    for (const card of cards) {
      const content = normalize(card.textContent + ' ' + card.dataset.search)
      card.hidden = !terms.every(term => content.includes(term))
    }
    document.querySelector('#no-results').hidden = cards.some(card => !card.hidden)
  })
}
document.querySelector('.print-sheet')?.addEventListener('click', () => window.print())
const form = document.querySelector('#inquiry')
if (form) {
  const whatsapp = document.querySelector('#send-whatsapp')
  const specs = form.querySelector('.sample-specs')
  const mobile = window.matchMedia('(max-width: 760px)')
  const fieldsGrid = form.querySelector('.fieldgrid')
  const fields = [...fieldsGrid.children]
  const quickFields = new Set(['buyer_contact', 'application', 'mode', 'material', 'option',
    'bopp_face', 'bopp_container', 'bopp_surface', 'port'])
  const dock = document.querySelector('.contact-whatsapp')
  const dockUrl = dock?.href

  function updateSampleLayout() {
    if (!specs) return
    const compact = mobile.matches && form.elements.mode.value === 'sample'
    if (compact === !specs.hidden) return
    if (compact) {
      const optionalGrid = specs.querySelector('.fieldgrid')
      for (const label of fields) {
        if (!quickFields.has(label.control.name)) optionalGrid.append(label)
      }
    } else {
      // Restore the original desktop and quote order, keeping entered field values.
      fieldsGrid.append(...fields)
    }
    specs.hidden = !compact
  }
  function requestLines() {
    const lines = ['RolloBase', document.querySelector('main h1').textContent, '']
    for (const field of form.querySelectorAll('input,select')) {
      if (field.disabled || !field.value.trim()) continue
      const value = field.selectedOptions ? field.selectedOptions[0].textContent : field.value
      lines.push(field.labels[0].firstChild.textContent.trim() + ': ' + value)
    }
    if (form.dataset.contact) lines.push('', form.dataset.contact)
    return lines
  }
  function updateWhatsapp() {
    if (whatsapp) whatsapp.href = 'https://wa.me/8618588600270?text=' + encodeURIComponent(requestLines().join('\n'))
    if (specs && whatsapp && dock) dock.href = specs.hidden ? dockUrl : whatsapp.href
  }
  const params = new URLSearchParams(location.search)
  for (const select of form.querySelectorAll('select')) {
    const wanted = params.get(select.name)
    if ([...select.options].some(option => option.value === wanted)) select.value = wanted
  }
  function update() {
    const material = form.elements.material.value
    const choice = form.elements.option
    choice.disabled = material !== 'woodfree'
    choice.parentElement.hidden = choice.disabled
    if (choice.disabled) choice.value = ''

    for (const field of form.querySelectorAll('[data-bopp-field]')) {
      field.disabled = material !== 'bopp'
      field.parentElement.hidden = field.disabled
    }

    const query = new URLSearchParams()
    for (const key of ['material', 'mode', 'option', 'bopp_face', 'bopp_surface']) {
      const field = form.elements[key]
      if (field && !field.disabled && field.value) query.set(key, field.value)
    }
    for (const link of document.querySelectorAll('.languages a')) {
      const url = new URL(link.href)
      url.search = query
      link.href = url
    }
    updateSampleLayout()
    updateWhatsapp()
  }
  update()
  if (specs) mobile.addEventListener('change', update)
  form.addEventListener('change', update)
  form.addEventListener('input', updateWhatsapp)
  form.addEventListener('submit', event => {
    event.preventDefault()
    const lines = requestLines()
    const blob = new Blob(['\uFEFF'+lines.join('\n')+'\n'],{type:'text/plain;charset=utf-8'})
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = ['RolloBase',form.elements.mode.value,form.elements.material.value,form.elements.option.value].filter(Boolean).join('-')+'.txt'
    a.click()
    const status = document.querySelector('#request-status')
    if (status) {
      status.textContent = status.dataset.message
      status.hidden = false
    }
    setTimeout(()=>URL.revokeObjectURL(url),1000)
  })
}
