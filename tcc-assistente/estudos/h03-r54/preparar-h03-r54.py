"""Copia os ramos R53 proprios para estudo de apoios idealizados R54."""
from pathlib import Path
import hashlib,json,shutil
root=Path('D:/TCC');src=root/'outputs/Cargas-H03-R53-PARCIAL-NAO-EXECUTAR';out=root/'outputs/Apoios-H03-R54-NAO-EXECUTAR';out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((src/'R53-manifesto.json').read_text(encoding='utf-8'))['files']
for r in manifest:assert sha(Path(r['path']))==r['sha256'],r['path']
(out/'R54-protegidos-R53.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
for branch in ('CAD','BIM'):
    d=json.loads((src/f'R53-estado-{branch}.json').read_text(encoding='utf-8'))
    dst=root/f'outputs/H03_{branch}_R54_APOIOS_NAO_EXECUTAR';dst.mkdir(exist_ok=False);files=[]
    for r in d['frozenFiles']:
        a=Path(r['frozen']);assert sha(a)==r['sha256'];b=dst/a.relative_to(src/f'congelado-{branch}');b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
        assert sha(b)==r['sha256'];files.append(dict(source=str(a),copy=str(b),sha256=sha(b)))
    result=dict(branch=branch,nativeProject=str(dst/'Projeto Eberick'/Path(d['nativeProject']).name),files=files,
        studyHypothesis=dict(support='Rotulado',barHeightMode='Fixo',barHeightCm=10,depthDfCm=0,realFoundationDesigned=False,soilPropertiesKnown=False,analyticalBaseCoordinatesVerified=False,auxiliaryBarSensitivityVerified=False),
        excludeFromSuperstructureQuantities=['Cadastros auxiliares de fundacao','Barras auxiliares abaixo de N0'],
        references=['https://suporte.altoqi.com.br/hc/pt-br/articles/360012152833','https://suporte.altoqi.com.br/hc/pt-br/articles/115002375753'],status='Preparado; alteracoes nativas ainda nao realizadas.')
    (out/f'R54-preparacao-{branch}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(out)
