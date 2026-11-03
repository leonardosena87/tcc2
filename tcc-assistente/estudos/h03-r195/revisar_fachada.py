"""Revisão de concepção comum. Preserva as medições anteriores e os PRJ de diagnóstico."""
from pathlib import Path
from decimal import Decimal as D
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import sys

ROOT = Path("D:/TCC")
DEST = ROOT / "entrega-orientador/H03-R195-Sem-J4"
OLD = ROOT / "entrega-orientador/H03-R194-Resultados/H03-R194-revisao-academica.zip"
REF = ROOT / "outputs/Compatibilizacao-H03-R68-PORTA-P3-ESTUDO/R68-referencia-arquitetonica-estudo.json"
STUDIES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDIES/"h03-r122"))
from consolidar import parse


def dump(data):
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_safely(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def audit_existing_beam_loads():
    reference = json.loads((STUDIES/"h03-r178/R178-comparacao-CAD-BIM.json").read_bytes())
    branches = {}
    for branch, item in reference["branches"].items():
        branch_result = {}
        for key, count in (("portico", 1), ("escada", 5)):
            src = item["exports"][key]
            raw = Path(src["path"]).read_bytes()
            if digest(raw) != src["sha256"]:
                raise ValueError("Exportação de referência alterada")
            model = parse(raw.decode("cp1252"))
            sections = {r["Frame"]:r["AnalSect"] for r in model["tables"]["FRAME SECTION ASSIGNMENTS"]}
            ids = [i for i,ends in model["frames"].items() if sections[i]=="R20x30B"
                   and all(p[1]==0 and p[2]==177.4 and 440<=p[0]<=655 for p in ends)
                   and ends[0][0]!=ends[1][0]]
            rows = [r for r in model["tables"]["FRAME LOADS - DISTRIBUTED"] if r["Frame"] in ids]
            if len(ids)!=count or len(rows)!=count or {r["Frame"] for r in rows}!=set(ids) or {r["LoadPat"] for r in rows}!={"G1"}:
                raise ValueError("Rever atribuições distribuídas em V16")
            branch_result[key] = dict(exportSha256=src["sha256"], frameIds=ids, nativeUnits=model["units"], distributedRows=rows)
        branches[branch]=branch_result
    return dict(reference="H03/R178", branches=branches,
        scope="Atribuições distribuídas diretas na seção 20x30 da V16. Exclui análise de forças nodais, reações das lajes e cadastro posterior.")


def main():
    source = REF.read_bytes()
    ref = json.loads(source)
    matches = [(floor, op) for floor in ref["floors"] for op in floor["openings"] if op["tag"] == "J4"]
    if len(matches) != 1 or matches[0][1]["id"] != "T-J4-01":
        raise ValueError("Identidade da abertura ambígua")
    floor, opening = matches[0]
    floor["openings"].remove(opening)
    ref.update(revision="H03/R195", parentReferencePath=str(REF), parentReferenceSha256=digest(source),
               parent="H03/R68", scope="Referência arquitetônica do estudo CAD/BIM. T-J4-01 suprimida da fachada por decisão do autor. Planta A0 original preservada.")
    pkg = DEST / "H03-R195-revisao-academica.zip"
    with ZipFile(OLD) as z:
        prev = json.loads(z.read("Manifesto.json"))
        files = {name:z.read(name) for name in prev}
        for name, data in files.items():
            if digest(data) != prev[name]["sha256"]:
                raise ValueError(f"Fonte R194 inconsistente: {name}")
    intersections = json.loads(files["Evidencias/J4-V16.json"])["intersections"]
    if any(len(intersections[b]) != 1 or intersections[b][0]["beam"] != "V16" or
           intersections[b][0]["dimensionsM"] != [1.6,.15,.3] for b in ("CAD","BIM")):
        raise ValueError("Rever faixa de sobreposição")
    strip = json.loads((ROOT / "outputs/Compatibilizacao-H03-R70-W08-J4-ESTUDO/R70-W08-J4.json").read_bytes())["conditionalMasonryTakeoff"]
    width = D(str(round(strip["knownLengthExcludingColumnsM"], 4)))
    unit = D(str(strip["areaWeightHypothesisKNm2"]))
    bottom, roof = D(str(strip["baseFinishedHypothesisM"])), D(str(strip["roofSoffitM"]))
    hit = intersections["CAD"][0]
    beam_bottom, beam_top = D(str(hit["minM"][2])), D(str(hit["maxM"][2]))
    area_lower = width * (beam_bottom - bottom)
    area_upper = width * (roof - beam_top)
    gross_opening = D(str(round(strip["openingAreaM2"], 4)))
    added_area = gross_opening - D(str(hit["dimensionsM"][0])) * (beam_top-beam_bottom)
    study = dict(revision="H03/R195", adoptedFor=["CAD","BIM"], removedOpening=opening["id"],
        resolvedClash="V16/J4", nature="Revisão arquitetônica comum, excluída do retrabalho específico de cada software.",
        widthM=float(width), wallThicknessM=.15, hypothesisKNPerM2=float(unit), lowerAreaM2=float(area_lower),
        upperAreaM2=float(area_upper), netPanelM2=float(area_lower+area_upper),
        netPanelWeightKN=float(unit*(area_lower+area_upper)), addedMasonryM2=float(added_area),
        addedMasonryWeightKN=float(unit*added_area), upperWeightKN=float(unit*area_upper),
        upperLoadIfFullySupportedOnV16_KNPerM=float(unit*(roof-beam_top)), calculatedNativeLineLoad=None,
        assumptions="Pano livre de 1,95 m, do piso +0,22 ao intradorso +6,09 m. Desconto de V16 em toda a largura. Incremento compara o mesmo modelo com e sem J4. Exclui esquadria removida, vergas e acabamento sobre concreto.",
        disposition="Triagem geométrica. Definir como cada pano descarrega, conferir cargas já cadastradas e eventuais apoios intermediários antes do lançamento.",
        eberickReprocessed=False)
    study["baselineBeamLoadAudit"]=audit_existing_beam_loads()
    report = files["Resultados.html"].decode().replace("H03/R194", "H03/R195")
    start, end = report.index("<h2>Compatibilização da fachada"), report.index("<h2>Condições para o encerramento")
    report = report[:start] + """<h2>Fachada da escada · revisão adotada</h2>
<p>Por decisão do autor, a fachada passa a ser estudada sem a janela J4. A viga V16 permanece no patamar, entre os pilares existentes. A alteração vale para os dois fluxos. O conflito geométrico fica encerrado por mudança de concepção. As observações e os cronômetros históricos conservam suas revisões de origem.</p>
<p>Adotando a parede de bloco cerâmico com 15 cm acabados e a composição de estudo de 1,565 kN/m², o fechamento acrescenta 4,64 m² de alvenaria, equivalentes a 7,26 kN. Dos 5,12 m² do vão anterior, 0,48 m² já coincidiam com concreto. A estimativa cobre apenas a alvenaria.</p>
<p>Entre as faces dos pilares, a faixa superior à V16 tem 4,316 m de altura até o intradorso de referência. Se toda essa faixa se apoiar na viga, sua contribuição potencial será 6,75 kN/m. A faixa inferior precisa de verificação de apoio própria. Os arquivos Eberick incluídos preservam os ensaios R188 anteriores a esta decisão.</p>
<p>Nas exportações analíticas R178 de ambos os receptores, a V16 possui apenas atribuições distribuídas diretas G1 no pórtico e na grelha da escada. A busca identificou um trecho da viga no pórtico e cinco na grelha por ramo. A próxima conferência deve abranger ações nodais, reações de outros elementos e a eventual distribuição da carga W08 antes de aplicá-la.</p>
""" + report[end:]
    report = report.replace("Resolver a interferência V16/J4 com orientação arquitetônica.", "Conferir o caminho das cargas da fachada W08 sem a J4 nos dois receptores.")
    report = report.replace("Autoria contém o RVT, os três DWGs e o IFC bruto.", "Autoria contém o RVT estrutural sem a referência gráfica J4, as três formas DWG e o IFC estrutural histórico R161.")
    files["Autoria/Revit/H03-R195-SEM-J4.rvt"] = files.pop("Autoria/Revit/H03-R160.rvt")
    files["Historico/J4-V16-antes-R194.json"] = files.pop("Evidencias/J4-V16.json")
    for name, data in {"Resultados.html":report.encode(), "R195-referencia-arquitetonica.json":dump(ref),
                       "R195-parede-W08.json":dump(study)}.items():
        files[name] = data
        write_safely(DEST/name,data)
    files["Vista-Revit-R195.png"] = (DEST/"Vista-Revit-R195.png").read_bytes()
    files["Manifesto.json"] = dump({name:dict(sha256=digest(data),bytes=len(data)) for name,data in files.items()})
    tmp = pkg.with_suffix(".tmp")
    with ZipFile(tmp,"w",ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name,data)
    with ZipFile(tmp) as z:
        if z.testzip() or any(digest(z.read(k)) != v["sha256"] for k,v in json.loads(z.read("Manifesto.json")).items()):
            raise ValueError("Falha na conferência do ZIP")
    tmp.replace(pkg)
    pointer = ROOT / "dados-pesquisa/escada-h03-atual.json"
    current = json.loads(pointer.read_bytes())
    backup = DEST / "ponteiro-antes-R195.json"
    if not backup.exists():
        backup.write_bytes(pointer.read_bytes())
    current.update(currentBeamWindowJ4ConflictPending=False, activeArchitectureRevision="H03/R195",
        activeArchitectureReferencePath=str(DEST/"R195-referencia-arquitetonica.json"),
        activeArchitectureReferenceSha256=digest(dump(ref)), windowJ4RemovedFromStudy=True,
        activeRevitStudyPath=str(DEST/"H03-R195-SEM-J4.rvt"), latestAcademicPackagePath=str(pkg),
        revisedW08TakeoffPath=str(DEST/"R195-parede-W08.json"), revisedW08AppliedToEberick=False)
    write_safely(pointer,dump(current))
    print(study["addedMasonryM2"],study["addedMasonryWeightKN"],study["netPanelM2"],study["netPanelWeightKN"],pkg)


if __name__ == "__main__":
    main()
