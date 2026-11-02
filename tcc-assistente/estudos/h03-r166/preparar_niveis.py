"""Variante experimental R166: nove níveis IFC -> três níveis estruturais.

Preserva geometrias mundiais, identidades, propriedades e materiais dos elementos.
Não altera cotas da arquitetura nem substitui o exportador nativo do Revit.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'h03-r162'))
from preparar_derivado import read,sha,cloud,metadata,schema_issues,ifcopenshell
import ifcopenshell.geom
from ifcopenshell.api.spatial.assign_container import assign_container
from ifcopenshell.api.root.remove_product import remove_product
from ifcopenshell.util.unit import calculate_unit_scale

OUT=Path('D:/TCC/outputs/Intercambio-H03-R166-NIVEIS-ESTRUTURAIS-NAO-EXECUTAR')
SOURCE=Path('D:/TCC/outputs/Intercambio-H03-R164-CONTINUIDADE-PILARES-NAO-EXECUTAR/H03-R160-R164-DERIVADO-VIGAS-E-4-PILARES-NAO-EXECUTAR.ifc')
TARGET=OUT/'H03-R160-R166-DERIVADO-3-NIVEIS-NAO-EXECUTAR.ifc'
EXPECTED_SOURCE='c3ef584960752b7a21341aa6388797b56bbdbeceb4844b85d981a84dc55e0218'


def stable_metadata(model):
    m=metadata(model)
    m.pop('levels')
    for row in m['products'].values():row.pop('containment')
    return m


def plan_levels(model):
    scale=calculate_unit_scale(model);levels=model.by_type('IfcBuildingStorey')
    if len(levels)!=9:raise ValueError('Entrada não corresponde ao controle de nove níveis')
    keep={}
    for name,elevation in [('N0',.2),('N1',3.2),('N2',6.39)]:
        found=[s for s in levels if abs(s.Elevation*scale-elevation)<1e-7]
        if len(found)!=1:raise ValueError('Nível estrutural ausente/ambíguo: '+name)
        keep[name]=found[0]
    old={s.GlobalId:s for s in levels if s not in keep.values()}
    remap=[]
    for rel in model.by_type('IfcRelContainedInSpatialStructure'):
        storey=rel.RelatingStructure
        if storey.GlobalId not in old:continue
        elevation=storey.Elevation*scale
        # Somente o caso observado: escada na base virtual e viga no patamar.
        classes=[o.is_a() for o in rel.RelatedElements]
        if abs(elevation-.17)<1e-7 and classes==['IfcStair']:target=keep['N0']
        elif abs(elevation-1.7741176470588232)<1e-7 and classes==['IfcBeam']:target=keep['N1']
        else:raise ValueError('Conteúdo inesperado no nível auxiliar; não redistribuir automaticamente')
        remap.append((list(rel.RelatedElements),target,storey.Name))
    return keep,old,remap


def main():
    t0=time.perf_counter()
    if TARGET.exists():raise FileExistsError('Não sobrescrever variante existente')
    assert sha(SOURCE)==EXPECTED_SOURCE
    model=ifcopenshell.open(str(SOURCE));assert model.schema=='IFC2X3'
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    before_meta=stable_metadata(model);before_issues=schema_issues(model)
    shapes={o.GlobalId:cloud(o,settings) for o in model.by_type('IfcElement') if o.Representation and not o.is_a('IfcStair')}
    keep,old,remap=plan_levels(model)
    levels_before=[dict(guid=s.GlobalId,name=s.Name,elevationRaw=s.Elevation) for s in model.by_type('IfcBuildingStorey')]
    remapped=[]
    for products,target,old_name in remap:
        remapped.extend(dict(guid=o.GlobalId,tag=o.Tag,ifcClass=o.is_a(),oldContainer=old_name,newContainer=target.Name) for o in products)
        assign_container(model,products=products,relating_structure=target)
    for storey in old.values():
        assert not storey.ContainsElements
        remove_product(model,product=storey)
    assert len(model.by_type('IfcBuildingStorey'))==3
    assert stable_metadata(model)==before_meta
    model.header.file_description.description=list(model.header.file_description.description)+['TCC R166 DERIVADO: 3 niveis estruturais; geometrias mundiais preservadas; NAO EXECUTAR']
    model.header.file_name.name=TARGET.name
    OUT.mkdir(parents=True,exist_ok=True);model.write(str(TARGET))
    reopened=ifcopenshell.open(str(TARGET))
    assert stable_metadata(reopened)==before_meta
    after_issues=schema_issues(reopened);assert after_issues==before_issues
    comparisons=[]
    for guid,old_shape in shapes.items():
        new=cloud(reopened.by_guid(guid),settings)
        same_cloud=old_shape['pointsSha256']==new['pointsSha256']
        maximum=max(abs(old_shape[side][i]-new[side][i]) for side in ('minM','maxM') for i in range(3))
        assert same_cloud and maximum<1e-8
        comparisons.append(dict(guid=guid,pointCloudPreserved=same_cloud,maxBoxDeltaM=maximum))
    assert sha(SOURCE)==EXPECTED_SOURCE
    result=dict(revision='H03/R166',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        sourcePath=str(SOURCE),sourceSha256=EXPECTED_SOURCE,targetPath=str(TARGET),targetSha256=sha(TARGET),
        sourceUnchanged=True,notNativeRevitExport=True,nativeProjectsNotEdited=True,
        levelsBefore=levels_before,levelsAfter=[dict(guid=s.GlobalId,name=s.Name,elevationRaw=s.Elevation) for s in reopened.by_type('IfcBuildingStorey')],
        remappedContainers=remapped,worldMeshedElementCount=len(shapes),worldGeometriesPreserved=True,
        elementIdentitiesPropertiesMaterialsPreserved=True,schemaIssuesBefore=before_issues,schemaIssuesAfter=after_issues,
        landingBeamAssignedToN1WithWorldTopM=1.7741176470588232,landingBeamReceiverElevationNotYetVerified=True,
        stairVirtualBaseRemainsWorldZ017=True,stairLowerSupportNotResolved=True,materialMechanicalPropertiesNotRepaired=True,
        receiverImportPerformed=False,structuralApproval=False,elapsedScriptMs=(time.perf_counter()-t0)*1000,
        elapsedIsNotFullBimFlow=True,geometryComparisons=comparisons)
    (OUT/'R166-derivado-conferencia.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,(dict,list))},ensure_ascii=False))


if __name__=='__main__':main()
