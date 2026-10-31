import test from 'node:test';
import assert from 'node:assert/strict';
import {utc,classify,overlaps} from '../estudos/h03-r86/inventariar-tempos.mjs';

test('inventory does not invent a timezone or turn an absent duration into zero',()=>{
  assert.equal(utc('2026-10-30T12:00:00'),null);
  assert.equal(utc({utc:'2026-10-30T12:00:00Z'}),'2026-10-30T12:00:00.000Z');
  assert.equal(classify({startUtc:'2026-10-30T12:00:00Z'}).durationMs,null);
  assert.equal(classify({elapsedMs:0}).durationMs,0);
});
test('consolidated containers are identified without counting their nested intervals again',()=>{
  const r=classify({records:[{elapsedMs:9000}]});assert.equal(r.classification,'container_nao_expandido');assert.equal(r.durationMs,null);
});
test('elapsed and UTC differences are retained separately instead of silently replacing a measurement',()=>{
  const r=classify({elapsedMs:9500,startUtc:'2026-10-30T12:00:00Z',endUtc:'2026-10-30T12:00:10Z',rankingAllowed:true});
  assert.equal(r.durationMs,9500);assert.equal(r.utcDifferenceMs,10000);assert.equal(r.durationMinusUtcMs,-500);assert.equal(r.eligibleForFinalFlowRanking,false);
  assert.throws(()=>classify({durationMs:-1}),/negativa/);
});
test('nested and adjacent intervals are distinguished without summing either',()=>{
  const base={durationMs:1000};const t=x=>'2026-10-30T12:00:'+x+'Z';
  const r=overlaps([{...base,id:'A',startUtc:t('00'),endUtc:t('10')},{...base,id:'B',startUtc:t('02'),endUtc:t('05')},{...base,id:'C',startUtc:t('10'),endUtc:t('12')}]);
  assert.equal(r.length,1);assert.deepEqual([r[0].a,r[0].b,r[0].overlapMs],['A','B',3000]);
});
