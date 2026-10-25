import {STATUS, CAPITAL, BASIS, safeURL, dateText, valueText, money, firstClaim, claimsFor, filterOptions, readFilterState, filterInvestors, limitations} from './model.js';

const $ = id => document.getElementById(id);
const form = $('filters'), dialog = $('detail');
let dataset, published = [], sources = new Map(), lastTrigger = null, lastInvestor = null, loading = false;
const el = (tag, text, className) => {
  const node = document.createElement(tag);
  if (text !== undefined && text !== null) node.textContent = String(text).replace(/[–—]/g, '-');
  if (className) node.className = className;
  return node;
};
function externalLink(label, url) {
  const safe = safeURL(url);
  if (!safe) return el('span', label + ' (odkaz není dostupný)');
  const a = el('a', label, 'source-link');
  a.href = safe; a.target = '_blank'; a.rel = 'noopener noreferrer';
  a.append(el('span', ' ↗')); return a;
}
function stateFromURL() {
  return readFilterState(location.search, published);
}
function writeFilters() {
  const url = new URL(location.href);
  for (const key of ['q', 'sector', 'stage', 'availability']) {
    const value = form.elements.namedItem(key).value;
    if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
  }
  history.replaceState(history.state, '', url);
  renderTable();
}
function restoreFilters() {
  const state = stateFromURL();
  for (const key of ['q', 'sector', 'stage', 'availability']) form.elements.namedItem(key).value = state[key];
  // Canonical IDs make shared URLs and the selected form values identical.
  const url = new URL(location.href);
  for (const key of ['sector', 'stage', 'availability']) {
    if (state[key]) url.searchParams.set(key, state[key]); else url.searchParams.delete(key);
  }
  history.replaceState(history.state, '', url);
}
function resetFilters() {
  form.reset();
  const url = new URL(location.href);
  url.search = '';
  history.replaceState(history.state, '', url);
  renderTable();
}
function option(select, value, label) { const o = el('option', label); o.value = value; select.append(o); }
function initFilters() {
  for (const [id, field] of [['sector', 'sectors'], ['stage', 'stage']]) {
    const select = $(id);
    select.replaceChildren(select.options[0]);
    for (const category of filterOptions(published, field)) {
      option(select, category.id, category.label + (category.limited ? ' (omezená opora)' : ''));
    }
  }
  const select = $('availability'); select.replaceChildren(select.options[0]);
  for (const [value, label] of [['ticket', 'Ticket doložen bez rozporu'], ['capital', 'Celkový kapitál doložen'], ['both', 'Oba údaje doloženy'], ['incomplete', 'Alespoň jeden údaj nedoložen']]) {
    const count = filterInvestors(published, {availability: value}).length;
    if (count) option(select, value, `${label} (${count})`);
  }
}
function renderMetrics() {
  const c = dataset.metrics.coverage;
  const items = [
    [published.length, 'Publikovaných investorů', 'Shoda aktuální AI a referenční klasifikace'],
    [dataset.metrics.classification.candidates, 'Prověřovaných kandidátů', 'Zmrazený, záměrně vybraný seznam'],
    [`${c.ticket.numerator}/${c.ticket.denominator}`, 'Obvyklá výše investice', 'Doložený ticket bez nevyřešeného rozporu'],
    [`${c.total_investment_capital.numerator}/${c.total_investment_capital.denominator}`, 'Celkový spravovaný kapitál', 'Souhrnné AUM, nikoli součet fondů'],
  ];
  $('metrics').replaceChildren(...items.map(([value, label, help]) => {
    const box = el('div', null, 'metric'); box.append(el('strong', value), el('span', label), el('small', help)); return box;
  }));
}
function renderTable() {
  if (!dataset) return;
  const state = stateFromURL(), rows = filterInvestors(published, state);
  $('clear-search').hidden = !state.q;
  $('result-count').textContent = `Zobrazeno ${rows.length} z ${published.length} publikovaných investorů`;
  $('name-heading').setAttribute('aria-sort', state.sort === 'desc' ? 'descending' : 'ascending');
  $('sort-arrow').textContent = state.sort === 'desc' ? '↓' : '↑';
  $('sort-description').textContent = state.sort === 'desc' ? ', řazeno sestupně, změnit na vzestupné řazení' : ', řazeno vzestupně, změnit na sestupné řazení';
  $('table-scroll').hidden = rows.length === 0;
  $('empty-state').hidden = rows.length !== 0;
  const body = $('investors'); body.replaceChildren();
  for (const inv of rows) {
    const tr = el('tr'); tr.dataset.investor = inv.id;
    if (location.hash === '#investor=' + encodeURIComponent(inv.id)) tr.classList.add('selected');
    const name = el('td'), link = el('a', inv.name, 'investor-name');
    link.href = '#investor=' + encodeURIComponent(inv.id); link.dataset.openInvestor = inv.id;
    name.append(link); tr.append(name);
    for (const field of ['sectors', 'stage', 'ticket', 'total_investment_capital']) {
      const td = el('td'), c = firstClaim(inv, field);
      const conflict = inv.conflicts.find(r => r.field === field);
      if (conflict) {
        for (const cid of conflict.claim_ids) {
          const claim = inv.claims.find(r => r.id === cid);
          td.append(el('div', valueText(claim.value), 'data-value'));
        }
        td.append(el('span', 'Odlišné hodnoty zdrojů', 'table-status'));
      } else {
        td.append(el('div', valueText(c?.value), field === 'sectors' ? 'truncate' : 'data-value'));
        if (c && !['supported', 'not_found'].includes(c.status)) td.append(el('span', STATUS[c.status]?.[0] || 'Omezená opora', 'table-status'));
        if (field === 'total_investment_capital' && c?.value != null && !c.valid_as_of) td.append(el('span', 'Vlastní údaj, bez data ocenění', 'table-status'));
      }
      tr.append(td);
    }
    const limits = el('td');
    for (const label of limitations(inv).slice(0, 3)) limits.append(el('span', label, 'limitation'));
    const action = el('td'), detail = el('a', 'Zobrazit', 'detail-link');
    detail.href = link.href; detail.dataset.openInvestor = inv.id; detail.setAttribute('aria-label', 'Zobrazit detail ' + inv.name);
    action.append(detail); tr.append(limits, action); body.append(tr);
  }
}
function badges(claim) {
  const wrap = el('div');
  wrap.append(el('span', STATUS[claim.status]?.[0] || 'Stav neurčen', 'status' + (claim.status !== 'supported' ? ' warning' : '')));
  if (claim.review) {
    const label = {supported: 'Reference: podpořeno', uncertain: 'Reference: nejisté', incorrect: 'Reference: nesprávné'}[claim.review.label];
    wrap.append(el('span', label, 'status' + (claim.review.label !== 'supported' ? ' warning' : '')));
  }
  return wrap;
}
function sourceBlock(sourceId) {
  const source = sources.get(sourceId), wrap = el('div', null, 'evidence');
  if (!source) { wrap.append(el('p', 'Zdroj není v balíčku dostupný.')); return wrap; }
  wrap.append(externalLink(source.title, source.url));
  wrap.append(el('p', source.publisher));
  const dl = el('dl');
  for (const [label, value] of [['Kontrola zdroje AI', dateText(source.accessed_on)], ['Publikace stránky', dateText(source.published_on)]]) dl.append(el('dt', label), el('dd', value));
  wrap.append(dl, el('p', source.evidence_summary, 'note'));
  return wrap;
}
function factCard(c, inv, expanded = false) {
  const box = el('article', null, 'fact'); box.dataset.claim = c.id;
  const main = el('div', null, 'fact-main');
  main.append(el('p', valueText(c.value), 'fact-value' + (typeof c.value === 'object' && c.value !== null ? ' money' : '')), badges(c));
  if (c.field === 'ticket' && c.value) main.append(el('p', BASIS[c.value.basis] || 'Rozpětí podle uvedeného zdroje.', 'detail-copy'));
  if (c.field === 'total_investment_capital' && c.value && !c.valid_as_of) main.append(el('p', 'Vlastní zveřejněný údaj bez data ocenění. Nejde o doložený disponibilní kapitál.', 'detail-copy'));
  if (c.value === null) main.append(el('p', STATUS[c.status]?.[1] || 'Hodnota nebyla zjištěna.', 'detail-copy'));
  const source = sources.get(c.source_id);
  if (source) {
    const origin = el('div', null, 'fact-source');
    origin.append(externalLink(source.publisher, source.url), el('span', 'Kontrola AI ' + dateText(source.accessed_on)));
    main.append(origin);
  }
  const detail = el('details'); detail.open = expanded;
  detail.append(el('summary', 'Zdroj, datum a poznámka'));
  const evidence = sourceBlock(c.source_id);
  const dl = el('dl');
  let scope = {manager: 'Správce / organizace', organization: 'Investiční organizace'}[c.scope];
  if (c.scope.startsWith('fund:')) scope = inv.funds.find(f => f.id === c.scope.slice(5))?.name || 'Konkrétní fond';
  dl.append(el('dt', 'Rozsah údaje'), el('dd', scope || c.scope), el('dt', 'Platnost údaje'), el('dd', dateText(c.valid_as_of)));
  evidence.append(dl, el('p', STATUS[c.status]?.[1] || '', 'note'));
  if (c.note) evidence.append(el('p', c.note, 'note'));
  if (c.review) {
    const review = el('div', null, 'review-note');
    review.append(el('p', `Reference dodaná uživatelem: ${c.review.reviewer}, ${dateText(c.review.reviewed_on)}.`), el('p', c.review.reason), el('p', 'Zápis provedla AI. Podpořený přepis neřeší automaticky aktuálnost ani rozpory mezi zdroji.'));
    evidence.append(review);
  } else evidence.append(el('p', 'Samostatná lidská reference tohoto tvrzení není vyplněna.'));
  detail.append(evidence); box.append(main, detail); return box;
}
function section(title) { const node = el('section', null, 'detail-section'); node.append(el('h3', title)); return node; }
function investorDetail(inv) {
  const content = $('detail-content'); content.replaceChildren(el('h2', inv.name)); content.firstChild.id = 'detail-title';
  const website = externalLink(inv.website, inv.website); website.classList.add('website'); content.append(website);
  if (inv.conflicts.length) {
    const notice = el('div', null, 'notice'); notice.append(el('p', 'Rozpor mezi zdroji. ' + inv.conflicts.map(r => r.explanation).join(' '))); content.append(notice);
  }
  const ticket = section('Obvyklá výše investice');
  for (const c of claimsFor(inv, 'ticket')) ticket.append(factCard(c, inv));
  content.append(ticket);
  const profile = section('Zaměření a přítomnost');
  for (const [field, title] of [['investor_type', 'Typ investora'], ['czech_office', 'Česká přítomnost'], ['sectors', 'Investiční zaměření'], ['stage', 'Investiční fáze'], ['geography', 'Geografické zaměření']]) {
    profile.append(el('h4', title));
    for (const c of claimsFor(inv, field)) profile.append(factCard(c, inv));
  }
  content.append(profile);
  const capital = section('Kapitálové údaje');
  capital.append(el('p', 'Souhrnné AUM, velikost fondu, fundraising a proinvestované prostředky jsou různé veličiny. Historické fondy nesčítáme do současného AUM.', 'detail-copy'));
  for (const c of [...claimsFor(inv, 'total_investment_capital'), ...claimsFor(inv, 'capital_reference')]) {
    capital.append(el('h4', c.value ? CAPITAL[c.value.metric] || 'Jiný kapitálový údaj' : 'Celkový spravovaný kapitál organizace (AUM)'), factCard(c, inv));
  }
  content.append(capital);
  const transactions = section('Doložené investice');
  for (const t of inv.transactions) {
    const tx = el('article', null, 'transaction');
    const dateKind = {announcement: 'oznámení', article_date: 'datum článku', portfolio_year: 'rok v portfoliu', publication: 'publikace', embedded_announcement: 'vložené oznámení'}[t.date_kind] || 'datum dle zdrojové evidence';
    tx.append(el('h3', t.company), el('p', `${dateText(t.date, t.date_precision)} (${dateKind}${t.date_precision === 'year' ? ', znám pouze rok' : ''})`));
    const round = el('p'); round.append(el('strong', 'Částka celého kola: '), document.createTextNode(money(t.round_amount))); tx.append(round);
    const contribution = el('p'); contribution.append(el('strong', 'Vlastní příspěvek investora: '), document.createTextNode(money(t.investor_contribution))); tx.append(contribution);
    tx.append(el('p', 'Částka kola se nepřisuzuje jednotlivému investorovi. ' + t.note));
    const sidList = [...new Set([t.source_id, ...t.corroborating_source_ids, t.contribution_source_id].filter(Boolean))];
    for (const sid of sidList) tx.append(sourceBlock(sid));
    transactions.append(tx);
  }
  content.append(transactions);
  const decision = section('Proč je investor zařazen');
  decision.append(el('p', 'Doložený přímý VC mandát, česká přítomnost a pojmenovaná investice; rozhodnutí vychází ze zdrojů u jednotlivých údajů a referenčního posouzení níže.', 'detail-copy'));
  const r = inv.classification.reference;
  decision.append(el('p', `Aktuální AI: zařadit. Referenční klasifikace: zařadit (${r.reviewer}, ${dateText(r.reviewed_on)}). Původní AI: ${inv.classification.initial_ai === 'include' ? 'zařadit' : 'zdržení se rozhodnutí'}.`, 'detail-copy'), el('p', r.reason, 'detail-copy'));
  decision.append(el('p', dataset.review_provenance + ' Klasifikace nepotvrzuje všechny atributy ani právní registrace.', 'detail-copy'));
  content.append(decision);
}
function methodology() {
  const content = $('detail-content'); content.replaceChildren(el('h2', 'Metodika a kvalita dat')); content.firstChild.id = 'detail-title';
  const list = el('ul', null, 'method-list');
  for (const text of [
    'Publikujeme pouze shodu aktuálního rozhodnutí AI a uživatelem dodané referenční klasifikace: přímý VC investor s doloženou českou přítomností a konkrétní pojmenovanou investicí. Nevyřešené identity nejsou v seznamu.',
    'Jednotkou je investiční organizace nebo značka. Jednotlivé fondy jsou vedeny samostatně. Česká kontaktní adresa není dokladem českého domicilu fondu ani fyzické návštěvy kanceláře.',
    'Odkaz dokládá původ tvrzení, nikoli automaticky jeho pravdivost. Kontrola stránky, publikace a platnost částky jsou různá data. Zdroje nejsou kompletně archivované a mohou se změnit.',
    'Kategorie filtrů jsou navigační pomůcka normalizovaná z původních tvrzení, nikoli nové nezávisle ověřené údaje. Sektorově otevřený mandát neznamená automatické zařazení do všech sektorů. Raná fáze bez přesného rozsahu se nerozepisuje na jednotlivá kola.',
    'Úplnost vyjadřuje podíl publikovaných investorů s podporovaným nenulovým údajem. Neříká, že je údaj pravdivý. Částečné, historické či rozporné tickety dostupnost bez rozporu nezvyšují.',
    'Pilot je malý záměrný kontrastní vzorek českých VC organizací. Výsledky nelze přenést na celý světový trh, jiné typy investorů nebo soukromé osoby.',
    'Částky se zobrazují v původních měnách bez přepočtů. AUM není disponibilní kapitál. Velikosti historických fondů se nesčítají do současného kapitálu.',
  ]) list.append(el('li', text));
  content.append(list);
  const m = dataset.metrics.classification, claims = dataset.metrics.claims;
  const measurement = section('Co bylo měřeno');
  measurement.append(el('p', `Precision původních pozitivních klasifikací: ${m.precision.numerator}/${m.precision.denominator}. Recall v kontrolovaném seznamu: ${m.recall_in_reviewed_candidate_set.numerator}/${m.recall_in_reviewed_candidate_set.denominator}. Abstence mohou recall snížit. Nejde o přesnost všech atributů ani odhad trhu.`, 'detail-copy'));
  measurement.append(el('p', `Uživatelem dodaná kontrola atributů: ${claims.human_reviewed} tvrzení, ${claims.correct} podpořených, ${claims.incorrect} nesprávných a ${claims.uncertain} nejistých. Shoda vyřešených tvrzení: ${claims.correct}/${claims.resolved}. Nejistá tvrzení jsou mimo tento jmenovatel a ostatní tvrzení tím nejsou potvrzena.`, 'detail-copy'));
  measurement.append(el('p', dataset.review_provenance + ' Reviewer a datum jsou zachovány u konkrétních kontrol. Wilsonův interval je u tohoto záměrného vzorku pouze popisný, nikoli populační odhad.', 'detail-copy'));
  content.append(measurement);
  const legend = section('Jak číst stavy údajů');
  for (const [label, meaning] of [...Object.values(STATUS), ['Rozpor mezi zdroji', 'Zdroje se liší. Zobrazujeme jednotlivé hodnoty s původem, nevytváříme sjednocený odhad.']]) {
    const row = el('div', null, 'legend-row'); row.append(el('strong', label), el('span', meaning)); legend.append(row);
  }
  content.append(legend);
}
function exportsPanel() {
  const content = $('detail-content'); content.replaceChildren(el('h2', 'Exporty celého pilotu')); content.firstChild.id = 'detail-title';
  content.append(el('p', 'Všechny soubory níže obsahují celý publikovaný dataset. Aktuální vyhledávání ani filtry jejich obsah nemění.', 'detail-copy'));
  for (const [label, path, help] of [
    ['Stáhnout publikovaný přehled CSV', './exports/investor_summary.csv', 'Souhrn investorů se zdrojovými URL, stavy a oddělenými příznaky ověření. UTF-8 s BOM.'],
    ['Stáhnout publikovaný dataset JSON', './data.json', 'Publikovaní investoři, všechna jejich tvrzení, zdroje, transakce, rozhodnutí a původ referenčních kontrol.'],
    ['Stáhnout metriky JSON', './exports/metrics.json', 'Klasifikace zmrazeného vzorku, dostupnost atributů a samostatné výsledky atributových referencí.'],
  ]) {
    const row = el('div', null, 'download-item'), a = el('a', label, 'secondary'); a.href = path; a.download = path.split('/').pop(); row.append(a, el('p', help, 'detail-copy')); content.append(row);
  }
}
function routeTarget() {
  if (location.hash === '#metodika') return {type: 'method'};
  if (location.hash === '#exporty') return {type: 'exports'};
  if (location.hash.startsWith('#investor=')) {
    try { return {type: 'investor', id: decodeURIComponent(location.hash.slice(10))}; } catch { return {type: 'invalid'}; }
  }
  return null;
}
function syncRoute() {
  if (!dataset) return;
  const target = routeTarget();
  for (const row of document.querySelectorAll('#investors tr')) row.classList.toggle('selected', target?.type === 'investor' && row.dataset.investor === target.id);
  if (!target) {
    if (dialog.open) {
      dialog.close();
      const trigger = lastTrigger?.isConnected ? lastTrigger : [...document.querySelectorAll('[data-open-investor]')].find(n => n.dataset.openInvestor === lastInvestor && n.className === lastTrigger?.className);
      (trigger || $('search')).focus({preventScroll: true});
    }
    document.title = 'Databáze investorů'; return;
  }
  if (target.type === 'method') { methodology(); $('detail-kind').textContent = 'Pravidla a omezení'; }
  else if (target.type === 'exports') { exportsPanel(); $('detail-kind').textContent = 'Data ke stažení'; }
  else {
    const inv = published.find(r => r.id === target.id);
    if (inv) { investorDetail(inv); $('detail-kind').textContent = 'Detail investora'; }
    else {
      const content = $('detail-content'); content.replaceChildren(el('h2', 'Investor není v publikovaném pilotu'), el('p', 'Tento odkaz nevede na publikovaný záznam. Zavřete detail a vyberte investora z přehledu.', 'detail-copy')); content.firstChild.id = 'detail-title';
    }
  }
  document.title = $('detail-title').textContent + ' | Databáze investorů';
  if (!dialog.open) dialog.showModal();
  dialog.scrollTop = 0; $('close-detail').focus();
}
function openRoute(hash, trigger) {
  lastTrigger = trigger; lastInvestor = trigger?.dataset.openInvestor || null;
  if (location.hash !== hash) history.pushState({investorDrawer: true}, '', hash);
  syncRoute();
}
function closeDetail() {
  if (history.state?.investorDrawer) history.back();
  else { const url = new URL(location.href); url.hash = ''; history.replaceState(null, '', url); syncRoute(); }
}
async function loadData() {
  if (loading) return;
  loading = true; dataset = undefined;
  $('load-state').hidden = false; $('error-state').hidden = true; $('table-scroll').hidden = true; $('empty-state').hidden = true;
  form.inert = true; $('reset').disabled = true;
  const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch('./data.json', {signal: controller.signal});
    if (!response.ok) throw new Error('Dataset could not be loaded');
    const data = await response.json();
    if (data.schema_version !== 1 || !Array.isArray(data.investors) || !Array.isArray(data.sources) || !data.metrics?.coverage) throw new Error('Invalid dataset');
    dataset = data;
    // This flag is emitted by Python. No client-side inference of publication.
    published = data.investors.filter(inv => inv.published === true);
    sources = new Map(data.sources.map(s => [s.id, s]));
    $('as-of').textContent = 'Stav dat ' + dateText(data.as_of);
    const repo = safeURL(data.repository_url);
    $('repo-link').hidden = !repo; if (repo) $('repo-link').href = repo;
    initFilters(); restoreFilters(); renderMetrics(); renderTable(); syncRoute();
  } catch {
    dataset = undefined; published = []; sources = new Map();
    $('metrics').replaceChildren(); $('repo-link').hidden = true;
    $('error-state').hidden = false; $('result-count').textContent = 'Přehled není načten';
    $('as-of').textContent = 'Stav dat není dostupný';
    document.title = 'Data nejsou dostupná | Databáze investorů';
  } finally {
    clearTimeout(timer); loading = false; $('load-state').hidden = true;
    form.inert = !dataset; $('reset').disabled = !dataset;
  }
}

form.addEventListener('submit', event => { event.preventDefault(); writeFilters(); });
$('search').addEventListener('input', event => { if (!event.isComposing) writeFilters(); });
$('search').addEventListener('compositionend', writeFilters);
for (const id of ['sector', 'stage', 'availability']) $(id).addEventListener('change', writeFilters);
$('clear-search').addEventListener('click', () => { $('search').value = ''; writeFilters(); $('search').focus(); });
for (const id of ['reset', 'empty-reset']) $(id).addEventListener('click', resetFilters);
$('sort').addEventListener('click', () => {
  const url = new URL(location.href);
  if (stateFromURL().sort === 'desc') url.searchParams.delete('sort'); else url.searchParams.set('sort', 'desc');
  history.replaceState(history.state, '', url); renderTable();
});
$('investors').addEventListener('click', event => {
  const link = event.target.closest('[data-open-investor]');
  if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
  event.preventDefault(); openRoute('#investor=' + encodeURIComponent(link.dataset.openInvestor), link);
});
for (const [id, hash] of [['method-link', '#metodika'], ['export-link', '#exporty']]) $(id).addEventListener('click', event => {
  if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
  event.preventDefault(); openRoute(hash, event.currentTarget);
});
$('close-detail').addEventListener('click', closeDetail);
dialog.addEventListener('cancel', event => { event.preventDefault(); closeDetail(); });
window.addEventListener('popstate', () => { restoreFilters(); renderTable(); syncRoute(); });
window.addEventListener('hashchange', syncRoute);
$('retry').addEventListener('click', loadData);
// Until this module has bound the actions, the static HTML exposes no enabled
// actionless buttons. Loading below separately owns filter availability.
for (const button of document.querySelectorAll('button[disabled]')) button.disabled = false;
loadData();
