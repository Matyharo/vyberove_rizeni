// Pure data helpers shared by the table and evidence drawer.
export const STATUS = {
  supported: ['Doloženo zdrojem', 'Použitý zdroj výrok podporuje. Samo o sobě to neznamená lidskou kontrolu ani současnou platnost.'],
  partial: ['Částečně doloženo', 'Zdroj podporuje jen část údaje nebo není vyřešen jeho úplný význam.'],
  inferred: ['Odvozeno', 'Klasifikace odvozená AI z uvedených podkladů, nikoli výslovné tvrzení zdroje.'],
  historical_unconfirmed: ['Historický údaj', 'Starší nebo časově neurčená hodnota. Současná platnost není potvrzena.'],
  undated_reference: ['Údaj bez data platnosti', 'Pomocný údaj bez samostatně doloženého referenčního data.'],
  not_found: ['Nezjištěno', 'Údaj se při omezené rešerši nepodařilo zjistit. Není to důkaz, že nebyl nikdy zveřejněn.'],
  not_disclosed: ['Nezveřejněno dle zdroje', 'Použitý zdroj výslovně uvádí, že údaj nezveřejňuje.'],
};
export const CAPITAL = {
  manager_aum: 'Celkový spravovaný kapitál organizace (AUM)',
  fund_closed_size: 'Historicky evidovaná velikost fondu - význam closingu nejistý',
  fund_reported_managed_capital: 'Spravovaný kapitál konkrétního fondu',
  fund_reported_size: 'Uváděná velikost konkrétního fondu',
  fund_target_size: 'Cíl fundraisingu konkrétního fondu',
  fund_reported_raised_capital: 'Uváděný získaný kapitál fondu',
  invested_to_date: 'Historicky proinvestovaná částka',
  committed_capital: 'Přislíbený kapitál',
  available_for_new_investments: 'Disponibilní kapitál pro nové investice',
};
export const BASIS = {
  check: 'Uváděná výše investičního šeku.',
  preferred_investment: 'Preferovaná velikost investice dle zdroje.',
  sweet_spot: 'Nejčastěji cílené rozpětí; nemusí jít o pevné minimum a maximum.',
  ticket: 'Uváděné rozpětí investice, nikoli velikost celého kola.',
  initial_ticket: 'Počáteční investice. Navazující investice mohou být další.',
  typical_first_investment: 'Obvyklá první investice, nikoli celoživotní součet vkladů.',
  investment: 'Uváděné rozpětí jedné investice.',
};
export const normalize = value => String(value ?? '').normalize('NFD').replace(/\p{M}/gu, '').toLocaleLowerCase('cs').trim();
export const claimsFor = (investor, field) => investor.claims.filter(c => c.field === field);
export const firstClaim = (investor, field) => claimsFor(investor, field)[0];
export function safeURL(value) {
  try {
    const url = new URL(value);
    return ['http:', 'https:'].includes(url.protocol) && url.hostname && !url.username && !url.password ? url.href : null;
  } catch { return null; }
}
export function dateText(value, precision = 'day') {
  if (!value) return 'Neuvedeno';
  if (precision === 'year' || /^\d{4}$/.test(value)) return String(value);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return 'Datum neurčeno';
  return new Intl.DateTimeFormat('cs-CZ', {day: 'numeric', month: 'numeric', year: 'numeric', timeZone: 'UTC'}).format(new Date(value + 'T00:00:00Z'));
}
const number = value => new Intl.NumberFormat('cs-CZ', {maximumFractionDigits: 2}).format(value);
function scaled(value, unit) { return number(value / unit) + (unit === 1e6 ? ' mil.' : unit === 1e3 ? ' tis.' : ''); }
export function money(value) {
  if (value == null) return 'Nezjištěno';
  if (typeof value !== 'object') return String(value);
  if ('min' in value) {
    const unit = value.min >= 1e6 ? 1e6 : value.min >= 1e3 ? 1e3 : 1;
    if (value.min < 1e6 && value.max >= 1e6) return scaled(value.min, 1e3) + ' - ' + scaled(value.max, 1e6) + ' ' + value.currency;
    return number(value.min / unit) + '-' + scaled(value.max, unit) + ' ' + value.currency;
  }
  const unit = value.amount >= 1e6 ? 1e6 : value.amount >= 1e3 ? 1e3 : 1;
  const prefix = value.bound === 'greater_than' ? 'Přes ' : value.bound === 'approximate' ? 'Přibližně ' : '';
  return prefix + scaled(value.amount, unit) + ' ' + value.currency;
}
export function valueText(value) {
  if (value == null) return 'Nezjištěno';
  if (typeof value === 'object') return money(value);
  if (typeof value === 'boolean') return value ? 'Ano' : 'Ne';
  if (value === 'venture_capital') return 'Venture kapitál';
  return String(value).replace(/[–—]/g, '-');
}
export function available(investor, field) {
  const c = firstClaim(investor, field);
  return Boolean(c && c.value !== null && c.status === 'supported' && !investor.conflicts.some(r => r.field === field));
}
export function filterTokens(investor, field) {
  return claimsFor(investor, field).filter(c => c.value !== null).flatMap(c => String(c.value).split(';').map(v => v.trim()).filter(Boolean));
}
export function filterInvestors(investors, state) {
  return investors.filter(inv => {
    const search = normalize(inv.name + ' ' + claimsFor(inv, 'sectors').map(c => valueText(c.value)).join(' '));
    const matches = !state.q || search.includes(normalize(state.q));
    const ticket = available(inv, 'ticket'), capital = available(inv, 'total_investment_capital');
    const data = !state.availability || ({ticket, capital, both: ticket && capital, incomplete: !ticket || !capital})[state.availability];
    return matches && data && (!state.sector || filterTokens(inv, 'sectors').includes(state.sector)) && (!state.stage || filterTokens(inv, 'stage').includes(state.stage));
  }).sort((a, b) => a.name.localeCompare(b.name, 'cs') * (state.sort === 'desc' ? -1 : 1));
}
export function limitations(inv) {
  const result = [];
  if (inv.conflicts.length) result.push('Rozpor mezi zdroji');
  if (firstClaim(inv, 'total_investment_capital')?.value == null) result.push('Celkový kapitál nezjištěn');
  if (inv.claims.some(c => c.status === 'historical_unconfirmed')) result.push('Historické částky');
  if (['sectors', 'stage', 'ticket'].some(f => firstClaim(inv, f)?.status === 'partial')) result.push('Částečné údaje');
  if (inv.claims.some(c => c.review?.label === 'uncertain')) result.push('Nejistá reference');
  if (firstClaim(inv, 'ticket')?.value == null) result.push('Ticket nezjištěn');
  return result;
}
