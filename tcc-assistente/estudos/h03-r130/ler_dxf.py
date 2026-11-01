"""Leitura restrita de entidades ASCII DXF; rejeita geometria inesperada."""
from pathlib import Path
from decimal import Decimal

def entities(path):
    lines=Path(path).read_text(encoding='utf-8-sig').splitlines()
    if len(lines)%2:
        raise ValueError('DXF com pares incompletos')
    pairs=[(int(lines[i].strip()),lines[i+1].strip()) for i in range(0,len(lines),2)]
    active=False;current=None;result=[]
    for i,(code,value) in enumerate(pairs):
        if code==0 and value=='SECTION':
            active=i+1<len(pairs) and pairs[i+1]==(2,'ENTITIES')
        if not active:
            continue
        if code==0:
            if current is not None:result.append(current)
            current=None
            if value=='ENDSEC':active=False
            elif value not in ['SECTION']:current=[(code,value)]
        elif current is not None:
            current.append((code,value))
    return result

def values(entity,code):
    return [v for c,v in entity if c==code]

def one(entity,code):
    result=values(entity,code)
    if len(result)!=1:raise ValueError(f'Código {code}: multiplicidade inesperada')
    return result[0]

def wall_line(path):
    rows=[e for e in entities(path) if values(e,8)==['CR-Paredes']]
    lines=[e for e in rows if one(e,0)=='LINE']
    labels=[e for e in rows if one(e,0)=='MTEXT']
    if len(lines)!=1 or len(labels)!=1 or len(rows)!=2:
        raise ValueError('Não há linha W15 única no nível CR-Paredes')
    e=lines[0]
    start=[Decimal(one(e,c)) for c in [10,20,30]]
    end=[Decimal(one(e,c)) for c in [11,21,31]]
    return {'startRaw':[str(v) for v in start],'endRaw':[str(v) for v in end],
            'label':one(labels[0],1),'lineHandle':one(e,5)}

if __name__=='__main__':
    import json,sys
    print(json.dumps(wall_line(sys.argv[1]),indent=2))
