"""Adapta geometria IFC retangular à proposta revisada; não calcula estruturas.

Somente vigas horizontais ortogonais e pilares verticais sem aberturas.
Preserva IFC original, GUIDs, Tags, materiais e elementos sem divergência.
IfcOpenShell deve estar instalado ou em TCC_IFC_DEPS. Nunca sobrescreve entrada.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, sys, time
if os.environ.get('TCC_IFC_DEPS'):
    sys.path.insert(0, os.environ['TCC_IFC_DEPS'])
import numpy as np
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element as ie
import ifcopenshell.util.placement as ip
import ifcopenshell.util.unit as iu
import ifcopenshell.validate

TOL = 1e-5  # metros, comparação numérica; não tolerância construtiva
CLASSES = {'column': 'IfcColumn', 'beam': 'IfcBeam', 'slab': 'IfcSlab'}
NOTICE = 'ESBOCO ACADEMICO NAO DIMENSIONADO - NAO EXECUTAR'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def close(a,b):
    return abs(a-b) <= TOL

def axis_points(item, matrix, scale, stack=()):
    """Lê eixos lineares diretos/mapeados; recusa casos não implementados."""
    if len(stack)>8 or item.id() in stack:
        raise ValueError('Eixo com referência cíclica ou profundidade excessiva.')
    if item.is_a('IfcMappedItem'):
        nested=matrix@ip.get_mappeditem_transformation(item)
        return [p for child in item.MappingSource.MappedRepresentation.Items
                for p in axis_points(child,nested,scale,(*stack,item.id()))]
    if item.is_a('IfcTrimmedCurve') and item.BasisCurve.is_a('IfcLine'):
        points=[]
        for trim in (item.Trim1,item.Trim2):
            cartesian=[p for p in trim if p.is_a('IfcCartesianPoint')]
            if len(cartesian)!=1:
                raise ValueError('Eixo linear sem extremo cartesiano; leitura paramétrica não implementada.')
            points.append(cartesian[0])
    elif item.is_a('IfcPolyline'):
        points=item.Points
    else:
        raise ValueError('Representação de eixo não suportada: '+item.is_a())
    result=[]
    for point in points:
        a=list(point.Coordinates);a += [0.]*(3-len(a))
        p=((matrix@np.array(a+[1.]))[:3]*scale).tolist()
        if not all(math.isfinite(v) for v in p):
            raise ValueError('Eixo com coordenada não finita.')
        result.append(p)
    return result

def references(model, proposal, registry):
    if proposal.get('schema') != 'tcc-esboco/1' or proposal.get('units') != 'm' or proposal.get('reviewed') is not True:
        raise ValueError('A proposta precisa declarar formato, metros e revisão.')
    if proposal['runId'] != registry['runId']:
        raise ValueError('Registro Revit e proposta pertencem a execuções distintas.')
    expected={e['id']:e for e in proposal['elements']}
    tags={str(e['revitId']):e['id'] for e in registry['elements']}
    if len(expected)!=len(proposal['elements']) or len(tags)!=len(registry['elements']) or set(tags.values())!=set(expected):
        raise ValueError('Identificação duplicada ou incompleta na referência.')
    objects={}
    for cls in CLASSES.values():
        for obj in model.by_type(cls):
            mark=tags.get(obj.Tag)
            if mark not in expected or mark in objects or obj.is_a()!=CLASSES[expected[mark]['kind']]:
                raise ValueError(f'Correspondência de classe/identidade inválida: {obj.GlobalId}/{obj.Tag}')
            objects[mark]=obj
    if set(objects)!=set(expected):
        raise ValueError('O IFC não contém exatamente os elementos previstos.')
    return expected,objects

def audit(model, expected, objects):
    scale=iu.calculate_unit_scale(model)
    if not math.isfinite(scale) or scale<=0:
        raise ValueError('Escala de unidade inválida.')
    settings=ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS,True)
    rows=[]
    for mark,obj in objects.items():
        x=expected[mark]
        shape=ifcopenshell.geom.create_shape(settings,obj)
        points=np.asarray(shape.geometry.verts,dtype=float).reshape(-1,3)
        if not len(points) or not np.isfinite(points).all():
            raise ValueError(f'Geometria vazia ou não finita: {mark}')
        low=points.min(axis=0).tolist();high=points.max(axis=0).tolist()
        checks={'classe':obj.is_a()==CLASSES[x['kind']]}
        detail={}
        if x['kind']=='column':
            wanted=[x['x']-x['b']/2,x['y']-x['h']/2,x['z0'],x['x']+x['b']/2,x['y']+x['h']/2,x['z1']]
            checks['secao_posicao_altura']=all(close(a,b) for a,b in zip(low+high,wanted))
        elif x['kind']=='slab':
            wanted=[x['x'],x['y'],x['z']-x['h'],x['x2'],x['y2'],x['z']]
            checks['painel_espessura_cota']=all(close(a,b) for a,b in zip(low+high,wanted))
        else:
            cross=1 if abs(x['x2']-x['x'])>abs(x['y2']-x['y']) else 0
            center=x['y'] if cross==1 else x['x']
            checks['secao_e_cota']=close(low[cross],center-x['b']/2) and close(high[cross],center+x['b']/2) and close(low[2],x['z']-x['h']) and close(high[2],x['z'])
            matrix=ip.get_local_placement(obj.ObjectPlacement)
            endpoints=[]
            for rep in obj.Representation.Representations:
                if rep.RepresentationIdentifier!='Axis':continue
                for item in rep.Items:
                    endpoints.extend(axis_points(item,matrix,scale))
            wanted=[[x['x'],x['y'],x['z']],[x['x2'],x['y2'],x['z']]]
            checks['eixo']=len(endpoints)==2 and all(any(all(close(a,b) for a,b in zip(p,q)) for q in endpoints) for p in wanted)
            detail['axisEndpointsM']=endpoints
        rows.append({'id':mark,'revitId':obj.Tag,'ifcGuid':obj.GlobalId,'class':obj.is_a(),'bboxM':{'min':low,'max':high},'checks':checks,**detail})
    active=[{'name':s.Name,'elevationM':ip.get_storey_elevation(s)*scale} for s in model.by_type('IfcBuildingStorey') if any(x in objects.values() for x in ie.get_decomposition(s))]
    elevations=sorted(x['elevationM'] for x in active)
    wanted=sorted({x['z0'] for x in expected.values() if x['kind']=='column'}|{x['z'] for x in expected.values() if x['kind'] in ('beam','slab')})
    if len(elevations)!=len(wanted) or not all(close(a,b) for a,b in zip(elevations,wanted)):
        raise ValueError('Níveis ativos não correspondem à proposta.')
    return {'lengthUnitToMeters':scale,'comparisonToleranceM':TOL,'counts':{cls:len(model.by_type(cls)) for cls in CLASSES.values()},'matchedElements':len(rows),'activeStoreys':active,'geometryCorrespondsToProposal':all(all(r['checks'].values()) for r in rows),'errors':[{'id':r['id'],'failed':[k for k,v in r['checks'].items() if not v]} for r in rows if not all(r['checks'].values())],'elements':rows}

def nominal_geometry(model,obj,x,scale):
    if x['kind'] not in ('beam','column') or obj.HasOpenings:
        raise ValueError(f'Geometria não suportada para adaptação: {x["id"]}')
    if ie.get_psets(obj,qtos_only=True):
        raise ValueError('Quantitativos existentes exigem tratamento explícito; adaptação recusada.')
    body=next(r for r in obj.Representation.Representations if r.RepresentationIdentifier=='Body')
    context=body.ContextOfItems
    if obj.ObjectPlacement.is_a()!='IfcLocalPlacement':
        raise ValueError('Colocação não suportada.')
    origin=np.array([x['x'],x['y'],x.get('z0',x.get('z'))],dtype=float)/scale
    world=np.eye(4);world[:3,3]=origin
    if x['kind']=='beam':
        dx,dy=x['x2']-x['x'],x['y2']-x['y']
        if not (close(dx,0) or close(dy,0)):
            raise ValueError('Somente viga horizontal ortogonal é suportada.')
        length=math.hypot(dx,dy)
        if length<=TOL:raise ValueError('Viga degenerada.')
        world[:3,0]=[dx/length,dy/length,0]
        world[:3,1]=[-dy/length,dx/length,0]
    else:length=x['z1']-x['z0']
    if length<=0 or x['b']<=0 or x['h']<=0:raise ValueError('Dimensão inválida.')
    old_placement=obj.ObjectPlacement
    old_representation=obj.Representation
    parent=old_placement.PlacementRelTo
    relative=np.linalg.inv(ip.get_local_placement(parent))@world if parent else world
    def point(coords):return model.createIfcCartesianPoint(tuple(float(v) for v in coords))
    def direction(coords):return model.createIfcDirection(tuple(float(v) for v in coords))
    placement=model.createIfcAxis2Placement3D(point(relative[:3,3]),direction(relative[:3,2]),direction(relative[:3,0]))
    obj.ObjectPlacement=model.createIfcLocalPlacement(parent,placement)
    profile=model.createIfcRectangleProfileDef('AREA',None,model.createIfcAxis2Placement2D(point([0,0]),None),float(x['b']/scale),float(x['h']/scale))
    if x['kind']=='beam':
        solid_position=model.createIfcAxis2Placement3D(point([0,0,-x['h']/2/scale]),direction([1,0,0]),direction([0,1,0]))
    else:
        solid_position=model.createIfcAxis2Placement3D(point([0,0,0]),direction([0,0,1]),direction([1,0,0]))
    solid=model.createIfcExtrudedAreaSolid(profile,solid_position,direction([0,0,1]),float(length/scale))
    new_body=model.createIfcShapeRepresentation(context,'Body','SweptSolid',[solid])
    reps=[new_body]
    if x['kind']=='beam':
        axis_context=next(r.ContextOfItems for r in obj.Representation.Representations if r.RepresentationIdentifier=='Axis')
        polyline=model.createIfcPolyline([point([0,0,0]),point([length/scale,0,0])])
        reps.insert(0,model.createIfcShapeRepresentation(axis_context,'Axis','Curve3D',[polyline]))
    styles=[s for item in body.Items for s in getattr(item,'StyledByItem',())]
    if styles:model.createIfcStyledItem(solid,styles[0].Styles,None)
    obj.Representation=model.createIfcProductDefinitionShape(None,None,reps)
    # Representações/colocações substituídas não podem ficar com inversos obrigatórios vazios.
    ie.remove_deep2(model,old_representation)
    if not model.get_inverse(old_placement):ie.remove_deep2(model,old_placement)

def schema_errors(model):
    logger=ifcopenshell.validate.json_logger()
    ifcopenshell.validate.validate(model,logger)
    return [{'level':s['level'],'attribute':s.get('attribute'),'instance':str(s.get('instance')),'message':s['message']} for s in logger.statements]

def cleanup_empty_references(model):
    removed=[]
    # A normalização anterior dos níveis deixou relações/colocações sem objeto.
    for relation in list(model.by_type('IfcRelDefinesByProperties')):
        if not relation.RelatedObjects:
            prop=relation.RelatingPropertyDefinition
            removed.append({'stepId':relation.id(),'class':relation.is_a(),'reason':'RelatedObjects vazio'})
            model.remove(relation)
            if not model.get_inverse(prop):ie.remove_deep2(model,prop)
    for placement in list(model.by_type('IfcLocalPlacement')):
        if not model.get_inverse(placement):
            removed.append({'stepId':placement.id(),'class':placement.is_a(),'reason':'Colocação sem qualquer referência inversa'})
            ie.remove_deep2(model,placement)
    return removed

def remove_empty_storeys(model, elevations_m):
    """Remove só metadados de níveis explicitamente escolhidos e comprovadamente vazios."""
    from ifcopenshell.api.root import remove_product
    scale=iu.calculate_unit_scale(model)
    chosen=[]
    for elevation in elevations_m:
        candidates=[s for s in model.by_type('IfcBuildingStorey')
                    if close(ip.get_storey_elevation(s)*scale,elevation)]
        if len(candidates)!=1 or candidates[0] in chosen:
            raise ValueError('Nível solicitado ausente, ambíguo ou repetido.')
        storey=candidates[0]
        if ie.get_decomposition(storey) or storey.ContainsElements or storey.IsDecomposedBy:
            raise ValueError('Recusada remoção de nível com conteúdo ou decomposição.')
        for rel in model.get_inverse(storey):
            permitted=(rel.is_a('IfcRelAggregates') and storey in rel.RelatedObjects) or (
                rel.is_a('IfcRelDefinesByProperties') and storey in rel.RelatedObjects)
            if not permitted:
                raise ValueError('Nível possui relação não prevista: '+rel.is_a())
        chosen.append(storey)
    originals={p.id():str(p) for p in model.by_type('IfcProduct') if p not in chosen}
    removed=[{'guid':s.GlobalId,'name':s.Name,'elevationM':ip.get_storey_elevation(s)*scale}
             for s in chosen]
    for storey in chosen:
        remove_product(model,product=storey)
    if any(str(model.by_id(i))!=record for i,record in originals.items()):
        raise ValueError('A normalização alterou outro produto; não salvar esta instância.')
    return removed

def adapt(source,proposal_path,registry_path,output):
    start=time.perf_counter()
    source,proposal_path,registry_path,output=map(Path,(source,proposal_path,registry_path,output))
    if output.exists() or output.resolve()==source.resolve():raise ValueError('A saída precisa ser nova e distinta da entrada.')
    hashes={str(p):sha(p) for p in (source,proposal_path,registry_path)}
    proposal=json.loads(proposal_path.read_text(encoding='utf-8-sig'));registry=json.loads(registry_path.read_text(encoding='utf-8-sig'))
    model=ifcopenshell.open(str(source));expected,objects=references(model,proposal,registry)
    schema_before=schema_errors(model)
    before=audit(model,expected,objects)
    originals={mark:str(obj) for mark,obj in objects.items()}
    materials={mark:str(ie.get_material(obj)) for mark,obj in objects.items()}
    changes=[]
    for error in before['errors']:
        mark=error['id'];obj=objects[mark]
        old=next(r for r in before['elements'] if r['id']==mark)
        nominal_geometry(model,obj,expected[mark],before['lengthUnitToMeters'])
        changes.append({'id':mark,'revitId':obj.Tag,'ifcGuid':obj.GlobalId,'failedBefore':error['failed'],'before':old,'nominalProposal':expected[mark],'operation':'Reconstrução explícita de colocação, seção retangular, sólido e eixo pela proposta revisada; sem uniões booleanas.'})
    after=audit(model,expected,objects)
    if not after['geometryCorrespondsToProposal']:raise ValueError('A adaptação não passou na auditoria geométrica.')
    cleanup=cleanup_empty_references(model)
    schema_after=schema_errors(model)
    if schema_after:raise ValueError(f'A saída possui {len(schema_after)} erros de esquema IFC.')
    changed={r['id'] for r in changes}
    assert all(str(obj)==originals[mark] for mark,obj in objects.items() if mark not in changed)
    assert all(str(ie.get_material(obj))==materials[mark] for mark,obj in objects.items())
    output.parent.mkdir(parents=True,exist_ok=True)
    model.write(str(output))
    reread=ifcopenshell.open(str(output));refs,objs=references(reread,proposal,registry);reopened=audit(reread,refs,objs)
    assert reopened['geometryCorrespondsToProposal']
    assert not schema_errors(reread)
    assert all(sha(p)==h for p,h in hashes.items())
    report={'schema':'tcc-ifc-nominal-adapter/1','generatedAt':datetime.now(timezone.utc).isoformat(),'status':NOTICE,'runId':proposal['runId'],'source':str(source),'sourceSha256':hashes[str(source)],'proposalSha256':hashes[str(proposal_path)],'registrySha256':hashes[str(registry_path)],'output':str(output),'outputSha256':sha(output),'ifcSchema':reread.schema,'software':f'IfcOpenShell {ifcopenshell.version}','changes':changes,'before':before,'after':reopened,'unchangedElementRecords':len(objects)-len(changes),'materialsPreserved':True,'identityPreserved':True,'sourceFilesPreserved':True,'technicalProcessSeconds':time.perf_counter()-start,'timingScope':'Preparação técnica do adaptador; não é duração completa do fluxo nem resultado comparativo de produtividade.','limitations':['Geometria aferida por caixa envolvente e eixo; não valida conectividade analítica, apoios ou continuidade no Eberick.','Reconstrução nominal pode produzir interseções intencionais; arquivo não destinado a quantitativo líquido de concreto.','C25 não comprovado; materiais genéricos preservados, sem atribuição fictícia de resistência.','RVT e saída nativa IFC não foram modificados; este IFC derivado requer ensaio próprio no Eberick.','Lajes não são automaticamente convertidas pelo assistente ensaiado; carregamentos e dimensionamento não realizados.'],'eberickNativeConversionVerified':False,'structuralCalculationPerformed':False}
    report.update({'schemaValidationBefore':schema_before,'schemaCleanup':cleanup,'schemaValidationAfter':schema_after,'schemaValidationPassed':True})
    output.with_suffix('.adaptacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('source','proposal','registry','output'):parser.add_argument('--'+arg,required=True,type=Path)
    args=parser.parse_args()
    result=adapt(args.source,args.proposal,args.registry,args.output)
    print(json.dumps({'output':result['output'],'changedElements':len(result['changes']),'beforeFlags':len(result['before']['errors']),'afterFlags':len(result['after']['errors']),'matchedElements':result['after']['matchedElements'],'structuralCalculationPerformed':False},ensure_ascii=False,indent=2))
