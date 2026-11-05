"""Ensaio linear da grelha 3D exportada em propriedades genéricas, em suas unidades declaradas.

Barras de Euler–Bernoulli, eixos locais CSI, cargas uniformes e liberações por condensação.
Não reproduz o modelo global, P-Delta, cisalhamento deformável nem o solver do Eberick.
"""
import math
import sys
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.linalg import block_diag
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'h03-r122'))
from consolidar import parse, number

CASES = ('G1','G2','Q','QT')
DOFS = ('U1','U2','U3','R1','R2','R3')


def element(a, b, s, mat, angle, shear_factor=None):
    line = np.array(b) - a
    length = np.linalg.norm(line)
    e1 = line / length
    ref = np.array([1.,0.,0.]) if np.linalg.norm(e1[:2]) < 1.e-9 else np.array([0.,0.,1.])
    e2 = ref - ref.dot(e1)*e1
    e2 /= np.linalg.norm(e2)
    e3 = np.cross(e1,e2)
    angle = math.radians(angle)
    basis = np.array([e1, math.cos(angle)*e2+math.sin(angle)*e3, -math.sin(angle)*e2+math.cos(angle)*e3])
    k = np.zeros((12,12))
    if s['Shape'] != 'General':
        raise ValueError('Usar exportação genérica.')
    for i,j,rigidity in [(0,6,number(mat['E1'])*number(s['Area'])*number(s['AMod'])),
                          (3,9,number(mat['G12'])*number(s['TorsConst'])*number(s['JMod']))]:
        k[np.ix_([i,j],[i,j])] = rigidity/length * np.array([[1,-1],[-1,1]])
    for ix,sign,prop,mod in [([1,5,7,11],1,'I33','I3Mod'),([2,4,8,10],-1,'I22','I2Mod')]:
        v=6*length*sign
        d=length**2
        ei=number(mat['E1'])*number(s[prop])*number(s[mod])
        phi=0 if shear_factor is None else 12*ei/(shear_factor*number(s['Area'])*number(mat['G12'])*d)
        k[np.ix_(ix,ix)] = (ei/(length**3*(1+phi))
                             *np.array([[12,v,-12,v],[v,(4+phi)*d,-v,(2-phi)*d],[-12,-v,12,-v],[v,(2-phi)*d,-v,(4+phi)*d]]))
    return k,block_diag(basis,basis,basis,basis),length


def consistent(q,L):
    f=np.zeros(12)
    f[:3]=f[6:9]=q*L/2
    f[5]=q[1]*L**2/12
    f[4]=-q[2]*L**2/12
    f[10:12]=-f[4:6]
    return f


def condense(k, f, released):
    """Condensa graus liberados, preservando a rigidez e as cargas de entrada."""
    k, f = k.copy(), f.copy()
    if released:
        influence = np.linalg.solve(k[np.ix_(released, released)], k[released, :]).T
        f -= influence @ f[released]
        k -= influence @ k[released, :]
        k[released, :] = 0
        k[:, released] = 0
        f[released, :] = 0
    return k, f


def solve(path, shear_factor=None, expected_v1_area_cm2=600, v1_bounds_cm=(451,539)):
    m=parse(path.read_text(encoding='cp1252'))
    t=m['tables']
    def by(table,key):return {r[key]:r for r in t[table]}
    node_index={key:i for i,key in enumerate(m['joints'])}
    nd=6*len(node_index)
    sec=by('FRAME SECTION PROPERTIES 01 - GENERAL','SectionName')
    mats=by('MATERIAL PROPERTIES 02 - BASIC MECHANICAL PROPERTIES','Material')
    assign=by('FRAME SECTION ASSIGNMENTS','Frame')
    axes=by('FRAME LOCAL AXES ASSIGNMENTS 1 - TYPICAL','Frame')
    release=by('FRAME RELEASE ASSIGNMENTS 1 - GENERAL','Frame')
    forces=np.zeros((nd,len(CASES)))
    loads=defaultdict(lambda: np.zeros((3,len(CASES))))
    for r in t['FRAME LOADS - DISTRIBUTED']:
        assert (r['CoordSys'],r['DistType'],r['Type'],r['RelDistA'],r['RelDistB'])==('LOCAL','RelDist','Force','0','1')
        assert r['FOverLA']==r['FOverLB']
        loads[r['Frame']][int(r['Dir'])-1,CASES.index(r['LoadPat'])]+=number(r['FOverLA'])
    for r in t['JOINT LOADS - FORCE']:
        assert r['CoordSys']=='GLOBAL'
        i=node_index[r['Joint']]*6
        forces[i:i+6,CASES.index(r['LoadPat'])]+=[number(r[k]) for k in ('F1','F2','F3','M1','M2','M3')]
    rows=[];cols=[];vals=[]; members={}
    for r in t['CONNECTIVITY - FRAME']:
        key=r['Frame']; a,b=m['frames'][key]
        dof=np.concatenate([6*node_index[j]+np.arange(6) for j in (r['JointI'],r['JointJ'])])
        s=sec[assign[key]['AnalSect']]
        k,rot,L=element(a,b,s,mats[s['Material']],number(axes.get(key,{}).get('Angle','0')),shear_factor)
        f=np.column_stack([consistent(col,L) for col in loads[key].T])
        rel=release.get(key,{})
        free=[i for i,kname in enumerate([name+end for end in 'IJ' for name in ('P','V2','V3','T','M2','M3')]) if rel.get(kname)=='YES']
        k, f = condense(k, f, free)
        kg=rot.T@k@rot
        rows.extend(np.repeat(dof,12));cols.extend(np.tile(dof,12));vals.extend(kg.ravel())
        forces[dof]+=rot.T@f
        if a[1:]==b[1:]==(321.58,20.) and v1_bounds_cm[0]<=min(a[0],b[0]) and max(a[0],b[0])<=v1_bounds_cm[1]:
            assert a[0]<b[0] and number(s['Area'])==expected_v1_area_cm2
            assert np.all(loads[key][2]==0) and axes.get(key,{}).get('Angle','0')=='0'
            members[key]=(dof,k,rot,f,a,b)
    K=coo_matrix((vals,(rows,cols)),shape=(nd,nd)).tocsc()
    fixed=set()
    for r in t['JOINT RESTRAINT ASSIGNMENTS']:
        fixed.update(6*node_index[r['Joint']]+j for j,key in enumerate(DOFS) if r[key]=='YES')
    for r in t['JOINT SPRING ASSIGNMENTS 1 - UNCOUPLED']:
        assert r['CoordSys']=='GLOBAL'
        for j,key in enumerate(DOFS):
            spring=number(r[key])
            if spring:
                assert spring>=1e19
                fixed.add(6*node_index[r['Joint']]+j)
    free=np.array([i for i in range(nd) if i not in fixed and K[i,i]>0])
    empty=[i for i in range(nd) if i not in fixed and K[i,i]==0]
    assert not empty or not np.any(forces[empty])
    d=np.zeros_like(forces)
    d[free]=splu(K[free,:][:,free]).solve(forces[free])
    resid=K@d-forces
    rel_res=float(np.max(np.abs(resid[free]))/max(np.max(np.abs(forces)),1))
    if rel_res>1e-5:raise ValueError(f'Resíduo relativo {rel_res}')
    output=[]
    for key,(dof,k,rot,f,a,b) in sorted(members.items(),key=lambda p:p[1][4][0]):
        end=k@rot@d[dof]-f
        output.append(dict(frame=key,x_cm=[a[0],b[0]],case_end_local={c:end[:,i].round(6).tolist() for i,c in enumerate(CASES)}))
    assert len(output)==5 and sum(v['x_cm'][1]-v['x_cm'][0] for v in output)==v1_bounds_cm[1]-v1_bounds_cm[0]
    return dict(relative_residual=rel_res,segments=output)
