"""Funcao nominal_geometry derivada do adaptador historico R95.

Somente geometria nominal ortogonal; nao dimensiona nem aprova ligacoes.
"""
import sys,math
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import numpy as np
import ifcopenshell.util.element as ie
import ifcopenshell.util.placement as ip
TOL=1e-5

def close(a,b):return abs(a-b)<=TOL


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
