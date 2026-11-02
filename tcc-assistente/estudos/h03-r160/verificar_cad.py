"""Confere o retorno DXF do DWG salvo, fechado e reaberto no AutoCAD.

Não calcula volumes resistentes, cargas ou capacidade estrutural.
"""
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,'D:/TCC/work/dxf-deps')
import ezdxf

OUT=Path('D:/TCC/outputs/Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def compare(expected,actual,tolerance=1e-9):
    if len(expected)!=len(actual):raise ValueError('Contagem de faces divergente')
    if {f['id'] for f in expected}!={f['id'] for f in actual}:raise ValueError('Identidades divergentes')
    if len({f['id'] for f in actual})!=len(actual):raise ValueError('Identidade duplicada')
    index={f['id']:f for f in actual};maximum=0
    for e in expected:
        a=index[e['id']]
        if a['layer']!=e['layer']:raise ValueError('Camada divergente: '+e['id'])
        if len(a['vertices'])!=4 or len(e['vertices'])!=4:raise ValueError('Face irregular')
        choices=[]
        for vertices in (a['vertices'],list(reversed(a['vertices']))):
            for k in range(4):
                rotated=vertices[k:]+vertices[:k]
                delta=[abs(v-w) for p,q in zip(e['vertices'],rotated) for v,w in zip(p,q)]
                if any(not math.isfinite(x) for x in delta):raise ValueError('Coordenada não finita')
                choices.append(max(delta))
        best=min(choices)
        if best>tolerance:raise ValueError('Coordenada/topologia divergente: '+e['id'])
        maximum=max(maximum,best)
    return maximum
