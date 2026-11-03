"""Reúne cópias de visualização e evidências, verifica e só então publica o ZIP local."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

HERE = Path(__file__).resolve().parent
STUDIES = HERE.parent
BASE = Path("D:/TCC")
DEST = BASE / "entrega-orientador" / "H03-R194-Resultados"


def read(path):
    return path.read_text(encoding="utf-8-sig")


def build(work):
    files = {}

    def include(name, path, expected=None):
        path = Path(path)
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if expected is not None and digest != expected:
            raise ValueError(f"Fonte diverge da revisão registrada: {name}")
        if name in files:
            raise ValueError(f"Nome duplicado: {name}")
        target = work / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        files[name] = {"bytes": len(data), "sha256": digest}

    author = BASE / "outputs/Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR"
    revit = json.loads(read(author / "R160-resultado.json"))
    # A cópia de segurança 0003 conserva exatamente o estado auditado da R160.
    rvt = Path(revit["nativeRevitPath"]).with_suffix(".0003.rvt")
    include("Autoria/Revit/H03-R160.rvt", rvt, revit["nativeRevitSha256"])
    for unit in json.loads(read(author / "R160-CAD-formas-conferidas.json"))["files"]:
        include("Autoria/AutoCAD/" + Path(unit["dwgPath"]).name, unit["dwgPath"], unit["dwgSha256"])
    raw = BASE / "outputs/Intercambio-H03-R161-R160-NAO-EXECUTAR/H03-R160-Revit-SOMENTE-VIGA-PATAMAR-NAO-EXECUTAR.ifc"
    include("Autoria/Revit/Exportacao-nativa-R161.ifc", raw, "4003d78dea0e3c60bd62a31ffbbb4d0ab58058cb3056928a204106b66598e555")
    trial = json.loads(read(STUDIES / "h03-r188/R188-ensaio-gancho-pareado.json"))
    for branch, row in trial["branches"].items():
        include(f"Eberick/{branch}/H03-{branch}-R188-NAO-EXECUTAR.prj", row["experimentalProjectPath"], row["experimentalProjectSha256"])
        include(f"Eberick/{branch}/Relatorio-R188.docx", row["reportPath"], row["reportSha256"])
        if row["nativeReport"]["nativeTotalSeconds"] != 7:
            raise ValueError("Tempo R188 inconsistente")
    for rev in (84, 165, 166, 167, 178, 180, 182, 185, 187, 188, 192, 193):
        name = f"LEIA-ME-R{rev}.md"
        include("Evidencias/" + name, STUDIES / f"h03-r{rev}" / name)
    for rev, name in [(161,"R161-IFC-E-RECEPCAO.md"),(193,"CAD-axiais-barra309-0.png"),
                      (193,"R193-leitura.json"),(188,"R188-ensaio-gancho-pareado.json")]:
        include("Evidencias/" + name, STUDIES / f"h03-r{rev}" / name)
    include("Evidencias/R83-tempo-Revit-fim.json", BASE / "outputs/Autoria-H03-R83-SINCRONIZACAO-GEOMETRICA-NAO-EXECUTAR/R83-tempo-Revit-fim.json")
    include("Evidencias/Protocolo.md", BASE / "PROTOCOLO-COMPARACAO-H03.md")
    window = json.loads(read(author / "R160-candidato-comum.json"))["windowJ4BoxInterpretedM"]
    prism_audit = json.loads(read(STUDIES / "h03-r185/R185-reconciliacao-vigas.json"))
    intersections = {}
    for branch, source in prism_audit["sources"].items():
        if hashlib.sha256(Path(source["path"]).read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError("IFC diferente da referência R178")
        hits = []
        for piece in prism_audit["branches"][branch]["pieces"]:
            if not piece["closedPrismValidated"]:
                raise ValueError("Geometria sem validação prismática")
            beam = piece["signature"]
            lower = [max(window[i], beam[i]) for i in range(3)]
            upper = [min(window[i+3], beam[i+3]) for i in range(3)]
            dims = [round(b-a, 7) for a,b in zip(lower, upper)]
            if min(dims) > 0:
                hits.append(dict(beam=piece["name"], guid=piece["guid"], minM=lower, maxM=upper, dimensionsM=dims))
        if len(hits) != 1 or hits[0]["beam"] != "V16" or hits[0]["dimensionsM"] != [1.6,.15,.30]:
            raise ValueError("Rever a interferência J4 e a figura antes de distribuir")
        intersections[branch] = hits
    geometry = work / "j4-fonte.json"
    geometry.write_text(json.dumps(dict(windowBoxM=window, windowAssumption="Peitoril referido ao piso +0,22 m",
        coordinateSources=prism_audit["sources"], intersections=intersections), indent=2, ensure_ascii=False),encoding="utf-8")
    include("Evidencias/J4-V16.json", geometry)
    include("Resultados.html", HERE / "Resultados.html")
    manifest = json.dumps(files, ensure_ascii=False, indent=2).encode("utf-8")
    archive = work / "H03-R194-revisao-academica.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as z:
        for name in files:
            z.write(work / name, name)
        z.writestr("Manifesto.json", manifest)
    with ZipFile(archive) as z:
        if z.testzip() or set(z.namelist()) != set(files) | {"Manifesto.json"}:
            raise ValueError("Falha na verificação do ZIP")
        for name, entry in json.loads(z.read("Manifesto.json")).items():
            if hashlib.sha256(z.read(name)).hexdigest() != entry["sha256"]:
                raise ValueError(name)
    archive.replace(DEST / archive.name)
    shutil.copy2(HERE / "Resultados.html", DEST / "Resultados.html")
    print(f"{len(files)} arquivos conferidos, além do manifesto. {DEST}")


if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=DEST) as temp:
        build(Path(temp))
