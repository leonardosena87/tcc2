"""Consolida aplicação e releitura Revit; não aprova o cálculo estrutural."""
import hashlib
import json
import re
import shutil
from collections import Counter
from datetime import datetime,timezone
from html.parser import HTMLParser
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))

class Rows(HTMLParser):
    def __init__(self):super().__init__();self.rows=[];self.row=None;self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='tr':self.row=[]
        elif tag=='td':self.cell=[]
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag=='td' and self.cell is not None:self.row.append(' '.join(''.join(self.cell).split()));self.cell=None
        elif tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None

def main():
    prep=read(OUT/'R159-preparacao.json');create=read(OUT/'R159-criacao-nativa.json');native=create['Readback']
    reread_path=sorted(OUT.glob('R159-releitura-nativa-*.json'))[-1];reread=read(reread_path)
    assert native==reread and native['Count']==65 and native['RetainedCount']==60
    assert len(native['Elements'])==65 and all(e['MaterialFckMPa']==25 for e in native['Elements'])
    assert Counter(e['Kind'] for e in native['Elements'])==dict(column=24,beam=30,slab=11)
    stair=native['Stair'];assert stair['TotalRisers']==17 and [r['Risers'] for r in stair['Runs']]==[9,8]
    assert all(abs(r['WidthM']-.9)<1e-6 and r['MaterialFckMPa']==25 for r in stair['Runs'])
    assert stair['LandingMaterialFckMPa']==25 and stair['LowerSupportUnresolved']
    copy=Path(prep['copyPath']);source=Path(prep['sourcePath']);closed=read(OUT/'R159-fechado-apos-criacao.json')
    assert sha(copy)==closed['copySha256'].lower() and sha(source)==prep['sourceSha256']
    assert sha(Path(prep['candidatePath']))==prep['candidateSha256']
    report=OUT/'R159-interferencias-nativas.html';html=report.read_text(encoding='utf-8')
    assert create['Document'] in html and 'Fim do relatório de interferência' in html
    parser=Rows();parser.feed(html);pairs=[];lookup={e['Id']:e['Mark'] for e in native['Elements']}
    for row in parser.rows:
        if not row or not row[0].isdigit():continue
        assert len(row)==3
        a,b=[int(re.search(r'\bID\s+(\d+)\b',c)[1]) for c in row[1:]]
        assert a==stair['Id'] and b in lookup
        pairs.append(dict(stairId=a,otherId=b,otherMark=lookup[b],nativeTextA=row[1],nativeTextB=row[2],automaticallyClassifiedAsDefect=False))
    assert len({(r['stairId'],r['otherId']) for r in pairs})==len(pairs)
    assert len(pairs)==1 and pairs[0]['otherMark']=='V16-ESC-PAT'
    failures=[read(p) for p in sorted(OUT.glob('R159-falha-*.json'))]
    assert len(failures)==3 and all(f['Saved'] is False for f in failures)
    cad=read(OUT/'R159-CAD-formas-conferidas.json');assert cad['uniqueBuildingElementCount']==65 and cad['allThreeSavedClosedReopened']
    for f in cad['files']:assert sha(Path(f['dwgPath']))==f['dwgSha256']
    original93=Path('D:/TCC/outputs/Materiais-H03-R93-ALINHAMENTO-NAO-EXECUTAR/H03-R93-Revit.rvt')
    assert sha(original93)=='82b58856ae7c40bbc4427b5603bdfc3ec74d5eefec76960b909a7424d0748db2'
    result=dict(revision='H03/R159',recordedAtUtc=datetime.now(timezone.utc).isoformat(),copyPath=str(copy),copySha256=sha(copy),
        sourceR157PreservedByteIdentical=True,originalR93PreservedByteIdentical=True,nativeCreatedSavedClosedReopenedReadbackMatched=True,
        candidateSha256=prep['candidateSha256'],readbackPath=str(reread_path),readbackSha256=sha(reread_path),readback=reread,
        nativeSuccessfulCommandMs=create['CommandMs'],commandTimeIsNotFlowTime=True,failedSoftwareAttempts=len(failures),failedAttemptsAreNotIfcReceptionDefects=True,
        warnings=create['Warnings'],guardOrHandrailDesignCompleted=False,nativeInterferenceReportPath=str(report),nativeInterferenceReportSha256=sha(report),
        nativeInterferencePairCount=len(pairs),nativeInterferencePairs=pairs,landingBeamContactNeedsAnalyticalAndConnectionVerification=True,
        nativeRevitGeometryComparedToCandidate=True,cadFormsVerified=True,cadAndRevitStairClosedSolidEquivalenceProved=False,
        ifcExportAndReceptionVerified=False,eberickProjectsUpdated=False,stairLowerSupportResolved=False,fullCompatibilityReviewCompleted=False,
        structuralDimensioningOrApproval=False,pairedFlowComparisonCompleted=False,
        sessionTiming=read(OUT/'R159-conferencia-fim.json'),interferenceTiming=read(OUT/'R159-interferencia-observacao.json'),
        timeIntervalsMayBeNestedDoNotSum=True,usableForPairedRanking=False)
    target=OUT/'R159-resultado-nativo.json';target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    current=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json');j=read(current)
    assert j['activeRevision']=='H03/R153' and j['nativeRevitRevision'] in ('H03/R157','H03/R159')
    before=OUT/'R159-apontador-antes-releitura.json'
    if not before.exists():shutil.copyfile(current,before)
    j.update(nativeRevitRevision='H03/R159',nativeRevitCopyPath=str(copy),nativeRevitReadbackEvidence=str(target),nativeRevitReadbackEvidenceSha256=sha(target),
        nativeRevitCreatedSavedReopened=True,landingBeamNativePlacementConfirmed=True,landingBeamRevitR159PlacementConfirmed=True,landingBeamEberickPlacementConfirmed=False,
        latestCandidateImplementationEvidencePath=str(target),latestCandidateImplementationEvidenceSha256=sha(target),
        fullCompatibilityReviewCompleted=False,landingBeamStructuralDimensioningCompleted=False,stairIntegratedInCalculationModel=False)
    current.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8');shutil.copyfile(current,OUT/'R159-apontador-apos-releitura.json')
    archive()
    print(json.dumps(dict(nativeReopenedExactMatch=True,retained=60,structuralElements=65,stairs=17,clashPairs=len(pairs),commandMs=create['CommandMs'])))

def archive():
    shutil.copyfile(HERE/'LEIA-ME-R159.md',OUT/'LEIA-ME-R159.md')
    for p in OUT.iterdir():
        if p.is_file() and p.suffix.lower() in {'.json','.png','.html','.dxf','.scr','.addin'} and 'manifesto' not in p.name:shutil.copyfile(p,HERE/p.name)
    entries=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (OUT,HERE):(folder/'R159-manifesto.json').write_text(json.dumps(entries,indent=2),encoding='utf-8')

if __name__=='__main__':main()
