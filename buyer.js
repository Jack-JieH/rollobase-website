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
  }
  update()
  form.addEventListener('change', update)
  form.addEventListener('submit', event => {
    event.preventDefault()
    const lines = ['RolloBase',document.querySelector('main h1').textContent,'']
    for (const field of form.querySelectorAll('input,select')) {
      if (field.disabled || !field.value.trim()) continue
      const value = field.selectedOptions ? field.selectedOptions[0].textContent : field.value
      lines.push(field.labels[0].firstChild.textContent.trim()+': '+value)
    }
    if (form.dataset.contact) lines.push('', form.dataset.contact)
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
