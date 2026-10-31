import test from 'node:test';
import assert from 'node:assert/strict';
import {compareDxf,entities,signature} from '../estudos/h03-r84/auditar-autoria.mjs';

const wrap=body=>'0\nSECTION\n2\nENTITIES\n'+body+'0\nENDSEC\n0\nEOF\n';
const rectangle='0\nLWPOLYLINE\n8\nVIGAS\n90\n4\n70\n1\n10\n0\n20\n0\n10\n6\n20\n0\n10\n6\n20\n0.2\n10\n0\n20\n0.2\n';
const label='0\nTEXT\n8\nNOTAS\n10\n3\n20\n0.4\n40\n0.12\n1\nV1 20x30 cm\n';

test('DXF roundtrip ignores handles but preserves nominal geometry and labels',()=>{
  const before=wrap(rectangle+label),after=wrap(label.replace('8\nNOTAS','5\nABC\n8\nNOTAS')+rectangle);
  const r=compareDxf(before,after);assert.equal(r.equal,true);assert.equal(r.polylines,1);assert.equal(r.texts,1);
});
test('same element count does not conceal a changed beam section label',()=>{
  const before=wrap(rectangle+label),after=before.replace('20x30 cm','20x55 cm');
  assert.equal(compareDxf(before,after).equal,false);
});
test('same rectangle size does not conceal a moved vertex',()=>{
  assert.equal(compareDxf(wrap(rectangle),wrap(rectangle.replace('10\n6\n20\n0\n','10\n6.1\n20\n0\n'))).equal,false);
});
test('duplicate labels are counted instead of collapsed into a set',()=>{
  assert.equal(compareDxf(wrap(rectangle+label),wrap(rectangle+label+label)).equal,false);
});
test('centered text uses its alignment point after native regeneration',()=>{
  const a=label+'72\n1\n73\n2\n11\n3\n21\n0.4\n';
  const b=a.replace('10\n3\n20\n0.4\n','10\n2.3\n20\n0.3\n');
  assert.equal(compareDxf(wrap(a),wrap(b)).equal,true);
  assert.equal(compareDxf(wrap(a),wrap(b.replace('11\n3\n','11\n3.2\n'))).equal,false);
});
test('unsupported arcs, nonplanar entities and incomplete files fail closed',()=>{
  assert.throws(()=>signature(entities(wrap(rectangle+'42\n0.2\n'))[0]),/Arco/);
  assert.throws(()=>signature(entities(wrap(rectangle+'38\n2\n'))[0]),/plano/);
  assert.throws(()=>entities('0\nSECTION\n2\nENTITIES\n'+rectangle),/completa/);
});
