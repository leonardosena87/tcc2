import test from 'node:test';
import assert from 'node:assert/strict';
import {normalize,relate} from './consolidar.mjs';
const meta=(name='CAD-sessao-tempo.json')=>({revision:137,name,source:'fixture',sha256:'fixture'});

test('preserva duração portuguesa e divergência UTC sem forçar igualdade',()=>{
  const r=normalize({inicio_utc:'2026-11-01T23:00:00Z',fim_utc:'2026-11-01T23:00:10Z',duracao_ms:9999.7},meta());
  assert.equal(r.durationMs,9999.7);assert.equal(r.utcDifferenceMs,10000);
  assert.ok(Math.abs(r.durationMinusUtcMs+0.3)<1e-8);assert.equal(r.eligibleForFinalFlowRanking,false);
});
test('consulta sem duração declara derivação UTC e preserva ausência sem fuso',()=>{
  const r=normalize({inicio_utc:'2026-11-02T00:00:00Z',fim_utc:'2026-11-02T00:01:00Z'},meta('CAD-consulta-fim.json'));
  assert.equal(r.durationMs,60000);assert.match(r.durationOrigin,/diferença/);
  assert.equal(normalize({inicio_utc:'2026-11-02T00:00:00',fim_utc:'2026-11-02T00:01:00'},meta()).durationMs,null);
  assert.equal(normalize({duracao_ms:0},meta()).durationMs,0);
  assert.throws(()=>normalize({duracao_ms:-1},meta()),/inválida/);
});
test('intervalo de observação pertence à sessão e recuperação não recebe rateio',()=>{
  const parent=normalize({inicio_utc:'2026-11-01T23:00:00Z',fim_utc:'2026-11-01T23:10:00Z',duracao_ms:600000},meta());
  const child=normalize({inicio_utc:'2026-11-01T23:02:00Z',fim_primeira_observacao_utc:'2026-11-01T23:03:00Z',duracao_ms:60000},meta('CAD-processamento-tempo.json'));
  const shared=normalize({inicio_utc:'2026-11-01T23:10:00Z',fim_utc:'2026-11-01T23:11:00Z',duracao_ms:60000},meta('recuperacao-capturas-tempo.json'));
  const overlaps=relate([parent,child,shared]);
  assert.deepEqual(child.parentIntervalIds,[parent.id]);assert.equal(overlaps.length,1);
  assert.equal(shared.branch,null);assert.equal(child.pureSolverTime,false);
});
test('formato R133 converte segundos declarados sem perder limite inicial',()=>{
  const r=normalize({utc:'2026-11-01T19:58:04.471Z',endUtc:'2026-11-01T19:58:39.764Z',elapsedSeconds:35.2927715},meta('CAD-processamento-tempo.json'));
  assert.equal(r.startUtc,'2026-11-01T19:58:04.471Z');assert.equal(r.durationMs,35292.7715);
  assert.equal(r.utcDifferenceMs,35293);assert.equal(r.isolatedAIInferenceMs,null);
});
