import {test} from 'node:test';
import assert from 'node:assert/strict';
import {filterInvestors, safeURL, available, money, dateText, normalize, readFilterState, filterOptions} from '../model.js';

const make = (id, name, sector, status = 'supported') => ({
  id, name, published: true, conflicts: [],
  navigation: {
    sectors: sector.split(';').map(label => ({id: normalize(label), label: label.trim(), source_statuses: ['supported']})),
    stage: [{id: 'seed', label: 'Seed', source_statuses: ['partial']}, {id: 'series-a', label: 'Series A', source_statuses: ['partial']}],
  }, claims: [
    {field: 'sectors', value: sector, status: 'supported'},
    {field: 'stage', value: 'seed; Series A', status: 'partial'},
    {field: 'ticket', value: {min: 250000, max: 400000, currency: 'EUR'}, status},
    {field: 'total_investment_capital', value: null, status: 'not_found'},
  ],
});
test('diacritic-insensitive search composes with literal source filters and sorting', () => {
  const rows = [make('a', 'Žáček Ventures', 'Zdravotnictví; Věda'), make('b', 'Alfa', 'Energie')];
  assert.deepEqual(filterInvestors(rows, {q: 'zacek', sector: 'veda', stage: 'series-a', availability: 'ticket'}).map(r => r.id), ['a']);
  assert.deepEqual(filterInvestors(rows, {q: 'ZDRAVOTNICTVI'}).map(r => r.id), ['a']);
  assert.equal(filterInvestors(rows, {q: 'zacek', sector: 'energie'}).length, 0);
  assert.deepEqual(filterInvestors(rows, {sort: 'desc'}).map(r => r.id), ['a', 'b']);
});
test('shared URL and form IDs restore the same combined canonical filters', () => {
  const rows = [make('a', 'Žáček Ventures', 'Zdravotnictví; Věda'), make('b', 'Alfa', 'Energie')];
  const restored = readFilterState('?q=ZACEK&sector=V%C4%9Bda&stage=SEED&availability=ticket&sort=desc', rows);
  const form = {q: 'ZACEK', sector: 'veda', stage: 'seed', availability: 'ticket', sort: 'desc'};
  assert.deepEqual(restored, form);
  assert.deepEqual(filterInvestors(rows, restored).map(r => r.id), filterInvestors(rows, form).map(r => r.id));
  rows[0].claims[0].value += '; explanatory note';
  assert(!filterOptions(rows, 'sectors').some(c => c.label.includes('explanatory note')));
  assert(!readFilterState('?stage=made-up', rows).stage);
});
test('historical, partial and conflicting tickets never count as supported availability', () => {
  const row = make('a', 'Investor', 'Tech', 'historical_unconfirmed');
  assert.equal(available(row, 'ticket'), false);
  row.claims[2].status = 'partial'; assert.equal(available(row, 'ticket'), false);
  row.claims[2].status = 'supported'; row.conflicts.push({field: 'ticket'});
  assert.equal(available(row, 'ticket'), false);
  assert.equal(filterInvestors([row], {availability: 'ticket'}).length, 0);
  assert.equal(available(row, 'total_investment_capital'), false);
});
test('external links reject dangerous schemes, relative URLs and credentials', () => {
  for (const url of ['javascript:alert(1)', 'data:text/html,bad', '//example.com', '/local', 'https://secret:password@example.com', 'file:///secret']) assert.equal(safeURL(url), null);
  assert.equal(safeURL('https://example.com/evidence'), 'https://example.com/evidence');
});
test('missing values, currencies, fund bounds and year precision remain distinct', () => {
  assert.equal(money(null), 'Nezjištěno');
  assert.match(money({min: 250000, max: 400000, currency: 'EUR'}), /250-400 tis\. EUR/);
  assert.match(money({amount: 500000000, currency: 'USD', bound: 'greater_than'}), /Přes 500 mil\. USD/);
  assert.equal(dateText('2022', 'year'), '2022');
});
