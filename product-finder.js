const finder = document.querySelector('[data-product-finder]');

if (finder) {
  const form = finder.querySelector('form');
  const cards = [...finder.querySelectorAll('[data-product]')];
  const status = finder.querySelector('[data-result-status]');
  const empty = finder.querySelector('[data-empty]');
  const { q, family, use } = form.elements;
  const normalize = value => value.normalize('NFKD')
    .replace(/\p{Mark}/gu, '')
    .replace(/[‐‑–—～~]/g, '-')
    .toLowerCase().trim();
  const tokens = query => query.replace(/([a-z0-9])(\p{Script=Han})/gu, '$1 $2')
    .replace(/(\p{Script=Han})([a-z0-9])/gu, '$1 $2')
    .split(/\s+/).filter(Boolean);
  const materialCodes = new Map([
    ['bopp', 'bopp'], ['бопп', 'bopp'], ['pe', 'pe'], ['пэ', 'pe'], ['pet', 'pet'], ['пэт', 'pet'],
  ]);
  const searchable = cards.map(card => [card, normalize(card.textContent + ' ' + card.dataset.keywords)]);

  const start = new URLSearchParams(location.search);
  q.value = start.get('q') || '';
  for (const field of [family, use]) {
    const value = start.get(field.name);
    if ([...field.options].some(option => option.value === value)) field.value = value;
  }

  function update() {
    const query = normalize(q.value);
    const code = materialCodes.get(query);
    const terms = tokens(query);
    let count = 0;
    for (const [card, searchText] of searchable) {
      const matchesQuery = code ? card.dataset.product === code : terms.every(term => searchText.includes(term));
      const match = matchesQuery && (family.value === 'all' || card.dataset.family === family.value)
        && (use.value === 'all' || card.dataset.use === use.value);
      card.hidden = !match;
      if (match) count += 1;
    }
    status.textContent = status.dataset.format.replace('{count}', count);
    empty.hidden = count !== 0;
  }

  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.addEventListener('submit', event => {
    event.preventDefault();
    update();
  });
  form.addEventListener('reset', () => requestAnimationFrame(update));
  update();
  form.hidden = false;
}
