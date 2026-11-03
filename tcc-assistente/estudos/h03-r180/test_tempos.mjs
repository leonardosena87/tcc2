import test from 'node:test';
import assert from 'node:assert/strict';
import {normalizeRecent} from './consolidar_tempos.mjs';
const meta={revision:175,name:'R175-processamento-tempo.json',source:'fonte',sha256:'teste'};
test('preserva duracao explicita e diferenca de UTC em campos distintos',()=>{
  const r=normalizeRecent({inicio:{utc:'2026-11-03T00:00:00Z'},fim:'2026-11-03T00:00:02Z',duracaoMs:1900},meta);
  assert.equal(r.durationMs,1900);assert.equal(r.utcDifferenceMs,2000);assert.equal(r.durationMinusUtcMs,-100);
});
test('marco isolado nao se transforma em duracao zero',()=>{
  const r=normalizeRecent({recordedAtUtc:'2026-11-03T00:00:00Z'},meta);
  assert.equal(r.durationMs,null);assert.equal(r.branch,null);
});
test('medicao de script mantem sua natureza parcial',()=>{
  const r=normalizeRecent({startUtc:'2026-11-03T00:00:00Z',endUtc:'2026-11-03T00:00:01Z',scriptDurationMs:5},{...meta,name:'R144-tempo-script.json'});
  assert.equal(r.durationMs,5);assert.match(r.category,/script/);assert.equal(r.eligibleForFinalFlowRanking,false);
});
test('duracao negativa nao e aceita',()=>assert.throws(()=>normalizeRecent({duracaoMs:-1},meta),/invalida/));
