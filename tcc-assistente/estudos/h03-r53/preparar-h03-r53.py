"""Prepara ramos independentes R53 e matriz parcial de cargas, preservando R52."""
from pathlib import Path
import json, hashlib, shutil
from datetime import datetime, timezone
root=Path('D:/TCC'); src=root/'outputs/Conferencia-H03-R52-VINCULOS-NAO-EXECUTAR'
out=root/'outputs/Cargas-H03-R53-PARCIAL-NAO-EXECUTAR'; out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=json.loads((src/'R52-manifesto.json').read_text(encoding='utf-8-sig'))['files']
for row in protected: assert sha(Path(row['path']))==row['sha256'], row['path']
for branch in ('CAD','BIM'):
    old=json.loads((src/f'R52-vinculo-{branch}.json').read_text(encoding='utf-8-sig'))
    native=root/f'outputs/H03_{branch}_R53_CARGAS_PARCIAIS_NAO_EXECUTAR';native.mkdir(exist_ok=False)
    rows=[]
    for row in old['frozenFiles']:
        a=Path(row['frozen']);assert sha(a)==row['sha256']
        b=native/a.relative_to(src/f'congelado-{branch}');b.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(a,b);assert sha(b)==row['sha256']
        rows.append(dict(source=str(a),copy=str(b),sha256=sha(b)))
    record=dict(branch=branch,nativeProject=str(native/'Projeto Eberick'/Path(old['nativeProject']).name),files=rows)
    (out/f'R53-preparacao-{branch}.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
matrix=[]
for level,names,q,g,meaning in [('N1',['L1','L2','L3','L4'],1.5,1.0,'Uso residencial; piso 5 cm com peso especifico hipotetico 20 kN/m3'),('N1',['L5'],2.5,1.0,'Faixa de circulacao junto a escada: carga de escada/uso restrito adotada provisoriamente; escada real pendente'),('N1',['L6'],2.5,1.0,'Varanda residencial; guarda-corpo e impermeabilizacao pendentes'),('N2',['L1','L2','L3','L4','L5'],1.0,0.25,'Cobertura de concreto com acesso apenas para manutencao; somente forro acartonado na permanente adicional')]:
    for name in names:matrix.append(dict(level=level,nativeName=name,Q_kNm2=q,G2partial_kNm2=g,interpretation=meaning,nativeApplied=False))
data=dict(revision='H03/R53',createdAtUtc=datetime.now(timezone.utc).isoformat(),matrix=matrix,
    scope='Parcelas uniformes parciais; nao constituem carregamento completo nem autorizacao de processamento conclusivo.',
    sources=[dict(path='D:/TCC/materiais/normas/ABNT NBR 6120-2019.pdf',sha256=sha(root/'materiais/normas/ABNT NBR 6120-2019.pdf'),table='10',pdfPages=[24,25,26,27]),dict(path='D:/TCC/outputs/Cargas-N1-H02-R31-PARCIAL-NAO-EXECUTAR/R31-cargas-lajes.csv',role='Historico; nao transplantado como geometria H03'),dict(url='https://suporte.altoqi.com.br/hc/pt-br/articles/115003144013',role='Campos e copia de cargas nativas')],
    selfWeightReference_kNm2=3.5,selfWeightHandling='Previsto pelo programa; nao duplicado em G2; verificar resultados no processamento.',selfWeightProcessingVerified=False,
    pending=['Paredes por trecho e aberturas','Telhado e caminho de suas reacoes','Reservatorio 1000 L: posicao, apoio, tara e base','Guarda-corpo e borda da varanda','Impermeabilizacao e camadas finais','Escada e reacoes','Vento e combinacoes','Apoios idealizados N0 e ligacoes analiticas','Verificacao ELU/ELS e alturas'],
    noSPT=True,scopeSuperstructureOnly=True,calculationPerformed=False,wholeFlowRankingAllowed=False)
(out/'R53-matriz-planejada.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'R53-protegidos-R52.json').write_text(json.dumps(protected,indent=2)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(out)
