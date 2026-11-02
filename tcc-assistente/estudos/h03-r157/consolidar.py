"""Extrai o relatório HTML nativo sem promover colisões a erros de projeto."""
import hashlib
import json
import re
import shutil
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R157-VISUAL-NAO-EXECUTAR')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class NativeReport(HTMLParser):
    def __init__(self):super().__init__();self.rows=[];self.row=None;self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='tr':self.row=[]
        elif tag=='td':self.cell=[]
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag=='td' and self.cell is not None:
            self.row.append(' '.join(''.join(self.cell).split()));self.cell=None
        elif tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None

def parse_report(html,expected_project):
    if expected_project not in html:raise ValueError('Relatorio de projeto diferente')
    if 'Fim do relatório de interferência' not in html:raise ValueError('Relatorio incompleto')
    p=NativeReport();p.feed(html);rows=[];keys=set()
    for row in p.rows:
        if not row or not row[0].isdigit():continue
        if len(row)!=3:raise ValueError('Linha irregular')
        a,b=row[1:];ida=re.search(r'\bID\s+(\d+)\b',a);idb=re.search(r'\bID\s+(\d+)\b',b)
        mark=re.search(r'\bMarca\s+([A-Z0-9-]+)\s*:',b)
        if not ida or not idb or not mark or 'TCC-H03-ESCADA17' not in a or int(ida[1])!=473597:
            raise ValueError('Identidade nativa ausente/divergente')
        key=(int(ida[1]),int(idb[1]))
        if key in keys:raise ValueError('Par nativo duplicado')
        keys.add(key);rows.append(dict(nativeReportRow=int(row[0]),stairId=key[0],otherId=key[1],otherMark=mark[1],category=b.split(':')[0].strip(),nativeTextA=a,nativeTextB=b))
    if not rows:raise ValueError('Sem pares nativos')
    return rows

def main():
    target=OUT/'R157-resultado.json'
    if target.exists():raise FileExistsError(target)
    prep=json.loads((OUT/'R157-preparacao.json').read_text(encoding='utf-8'))
    copies=json.loads((OUT/'R157-copias.json').read_text(encoding='utf-8'))
    native=json.loads((OUT/'R157-leitura-nativa-antes-gravar.json').read_text(encoding='utf-8'))
    frozen=json.loads((Path(prep['sourcePath']).parent/'R155-resultado.json').read_text(encoding='utf-8'))
    assert native==frozen['readback'] and native['TotalRisers']==17
    assert sha(Path(prep['sourcePath']))==prep['sourceSha256']
    assert sha(Path(copies['copyPath']))==copies['copySha256']
    assert sha(Path(prep['sourceOriginalR93Path']))==prep['sourceOriginalR93Sha256']
    report=OUT/'R157-interferencias-nativas.html';rows=parse_report(report.read_text(encoding='utf-8'),copies['copyPath'])
    assert {r['otherMark']:r['otherId'] for r in rows}=={'P4-N1':472933,'P10-N1':473097,'V13-N1':472984,'V15-N1':472986,'L6-N1':473020}
    for name in ('R157-escadas-desmarcadas-1.png','R157-reaberta.png','R157-interferencia-config-1.png'):assert (OUT/name).is_file()
    clocks={n:json.loads((OUT/n).read_text(encoding='utf-8')) for n in ('Revit-inicio.json','Revit-fechado-apos-gravar.json','Revit-reaberto-observado.json','Revit-interferencia-inicio.json','Revit-interferencia-observacao.json','Revit-fim.json')}
    parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
    a=clocks['Revit-inicio.json'];b=clocks['Revit-fim.json'];c=clocks['Revit-interferencia-inicio.json'];d=clocks['Revit-interferencia-observacao.json']
    assert a['mono']<clocks['Revit-fechado-apos-gravar.json']['mono']<clocks['Revit-reaberto-observado.json']['mono']<c['mono']<d['mono']<b['mono']
    times=dict(clocks=clocks,sessionElapsedMonotonicMs=b['mono']-a['mono'],sessionElapsedUtcMs=(parse(b['utc'])-parse(a['utc'])).total_seconds()*1000,
        interferenceCommandToObservationMs=d['mono']-c['mono'],interferenceIntervalIncludedInSession=True,
        includesNavigationCaptureWaitingAndReasoning=True,solverCpuTimeUnknown=True,aiInferenceTimeUnknown=True,
        usableForPairedCadBimRanking=False,doNotSumNestedIntervals=True)
    (OUT/'R157-tempos.json').write_text(json.dumps(times,ensure_ascii=False,indent=2),encoding='utf-8')
    result=dict(revision='H03/R157',copyPath=copies['copyPath'],copySha256=copies['copySha256'],r155ByteIdenticalPreserved=True,r93ByteIdenticalPreserved=True,
        geometryChangedByThisRevision=False,stairsCategoryOriginallyUnchecked=True,coordinationAloneDidNotRestoreVisibility=True,
        stairsVisibilityEnabled=True,annotationsHiddenInThisViewOnly=True,visualizationSavedClosedReopened=True,initialVisualReviewPerformed=True,
        fullCompatibilityReviewCompleted=False,nativeReadbackBeforeSaveMatchedR155=True,fullApiReadbackAfterCopyReopenPerformed=False,
        originalAuditCommandLimitedToR155Path=True,nativeInterferenceReportExportedAfterReopen=True,nativeInterferencePairCount=len(rows),pairs=rows,
        reportPath=str(report),reportSha256=sha(report),interferencePairsAreNotAutomaticallyDefects=True,
        connectedSupportAndFinishDetailingStillPending=True,geometryOrLoadsAppliedToCadOrEberick=False,structuralApproval=False,
        humanIntervention='Usuario alterou Disciplina para Coordenacao; categoria Escadas habilitada pelo agente depois da verificacao',
        supersedesPriorVisibilityExplanation='R155/R156 atribuiam a ocultacao a disciplina; R157 constatou tambem categoria Escadas desmarcada',
        officialMethodSource='https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-run-an-interference-check-between-elements-in-Revit.html')
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    current=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json');shutil.copyfile(current,OUT/'R157-apontador-anterior.json')
    j=json.loads(current.read_text(encoding='utf-8'));assert j['activeRevision']=='H03/R153'
    j.update(nativeRevitRevision='H03/R157',nativeRevitCopyPath=copies['copyPath'],nativeStairVisibleAndReopened=True,
        initialVisualReviewPerformed=True,fullCompatibilityReviewCompleted=False,latestVisualEvidencePath=str(target),latestVisualEvidenceSha256=sha(target))
    current.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8');shutil.copyfile(current,OUT/'R157-apontador-atual.json')
    archive()
    print(json.dumps(dict(nativePairs=len(rows),sessionMinutes=times['sessionElapsedMonotonicMs']/60000,commandToObservationMs=times['interferenceCommandToObservationMs'],r155Preserved=True)))

def archive():
    shutil.copyfile(HERE/'LEIA-ME-R157.md',OUT/'LEIA-ME-R157.md')
    for p in OUT.iterdir():
        if p.is_file() and p.suffix.lower() in ('.json','.html','.png','.txt') and 'manifesto' not in p.name:shutil.copyfile(p,HERE/p.name)
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    m=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (OUT,HERE):(folder/'R157-manifesto.json').write_text(json.dumps(m,indent=2),encoding='utf-8')

if __name__=='__main__':main()
