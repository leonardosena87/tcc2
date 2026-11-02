"""Compara nuvens de vertices antes/depois; nao prova equivalencia de solidos."""
import hashlib
import json
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from auditar_exportacao import OUT,IFC,read,sha,ifcopenshell
import ifcopenshell.geom


def triangulated_metrics(verts,faces):
    _,inverse=np.unique(np.round(verts,8),axis=0,return_inverse=True)
    welded=inverse[faces]
    edges=Counter();orientation=Counter()
    for face in welded:
        for x,y in zip(face,np.roll(face,-1)):
            edge=tuple(sorted((int(x),int(y))));edges[edge]+=1
            orientation[edge]+=1 if x<y else -1
    closed=bool(edges) and all(n==2 for n in edges.values()) and all(n==0 for n in orientation.values())
    volume=abs(float(np.einsum('ij,ij->i',verts[faces[:,0]],np.cross(verts[faces[:,1]],verts[faces[:,2]])).sum()/6)) if closed else None
    area=float(np.linalg.norm(np.cross(verts[faces[:,1]]-verts[faces[:,0]],verts[faces[:,2]]-verts[faces[:,0]]),axis=1).sum()/2)
    return dict(triangulatedClosedOrientedEdgeCheck=closed,triangulatedSignedVolumeAbsoluteM3=volume,triangulatedAreaM2=area)


def signatures(model):
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    records={}
    for cls in ('IfcColumn','IfcBeam','IfcSlab','IfcStairFlight'):
        for obj in model.by_type(cls):
            key=(cls,str(obj.Tag))
            if key in records:raise ValueError('Identidade duplicada no mesmo arquivo')
            shape=ifcopenshell.geom.create_shape(settings,obj)
            verts=np.asarray(shape.geometry.verts).reshape(-1,3)
            if not np.isfinite(verts).all():raise ValueError('Vertices nao finitos')
            points=sorted(set(tuple(p) for p in np.round(verts,8)))
            faces=np.asarray(shape.geometry.faces).reshape(-1,3)
            records[key]=dict(guid=obj.GlobalId,pointsSha256=hashlib.sha256(json.dumps(points,separators=(',',':')).encode()).hexdigest(),
                minM=verts.min(0).tolist(),maxM=verts.max(0).tolist(),uniqueRoundedVertices=len(points),
                **triangulated_metrics(verts,faces))
    return records


def main():
    old_audit_path=Path('D:/TCC/outputs/Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR/R159-IFC-auditoria.json')
    old_audit=read(old_audit_path);new_audit=read(OUT/'R161-IFC-auditoria.json')
    old=Path(next(p for p in old_audit['sources'] if p.lower().endswith('.ifc')))
    assert sha(old)==old_audit['sources'][str(old)]
    assert sha(IFC)==new_audit['sources'][str(IFC)]
    files=[old,IFC,old_audit_path,OUT/'R161-IFC-auditoria.json'];before={str(p):sha(p) for p in files}
    a=signatures(ifcopenshell.open(str(old)));b=signatures(ifcopenshell.open(str(IFC)))
    removed=sorted(set(a)-set(b));added=sorted(set(b)-set(a));common=sorted(set(a)&set(b))
    changed=[dict(ifcClass=k[0],tag=k[1],before=a[k],after=b[k]) for k in common if a[k]['pointsSha256']!=b[k]['pointsSha256']]
    assert removed==[('IfcColumn','473797'),('IfcColumn','473798')] and not added
    assert ('IfcBeam','473802') in [(c['ifcClass'],c['tag']) for c in changed]
    assert before=={str(p):sha(p) for p in files}
    result=dict(revision='H03/R161',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sources=before,
        sourceHashesUnchangedAfterRead=True,removed=[dict(ifcClass=c,tag=t) for c,t in removed],added=added,
        commonProductCount=len(common),unchangedPointCloudCount=len(common)-len(changed),changedPointClouds=changed,
        additionalChangedProductTags=[c['tag'] for c in changed if c['tag']!='473802'],
        causeOfAdditionalGeometryChangesNotIsolated=True,
        roundingDecimalsM=8,pointCloudEqualityDoesNotProveSurfaceSolidOrAnalyticalEquivalence=True,
        stairFlightsPointCloudsUnchanged=all(a[k]['pointsSha256']==b[k]['pointsSha256'] for k in common if k[0]=='IfcStairFlight'),
        rawIfcFilesUnmodified=True,structuralApproval=False)
    (OUT/'R161-IFC-comparacao-R159-R160.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('removed','commonProductCount','unchangedPointCloudCount','stairFlightsPointCloudsUnchanged')}))


if __name__=='__main__':main()
