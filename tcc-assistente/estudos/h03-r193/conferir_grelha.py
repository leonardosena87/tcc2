"""Localiza as leituras da grelha CAD R192 nas referências analíticas R178."""
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
OUT = Path("D:/TCC/outputs/Escada-H03-R193-LEITURA-GRELHA-NAO-EXECUTAR")
sys.path.insert(0, str(HERE.parent / "h03-r122"))
from consolidar import parse, sha

# Transcrição da janela Valores, preservando a ordem e a unidade exibidas.
SAMPLES = {
    "309": ("barra309", [86.52, 87.97]),
    "315": ("base-vizinha", [-1.44, 0.00]),
    "321": ("base-centro", [-1.44, 0.00]),
    "327": ("base-outra-lateral", [60.50, 61.94]),
    "304": ("proximo-patamar", [38.65, 40.09]),
}


def main():
    records = json.loads((HERE.parent / "h03-r178/R178-comparacao-CAD-BIM.json").read_text(encoding="utf-8"))
    trial = json.loads((HERE.parent / "h03-r192/R192-resultado.json").read_text(encoding="utf-8"))
    project = Path(trial["projectPath"])
    if sha(project) != trial["projectSha256"]:
        raise ValueError("PRJ R192 alterado")
    branches = {}
    for branch in ("CAD", "BIM"):
        export = records["branches"][branch]["exports"]["escada"]
        path = Path(export["path"])
        if sha(path) != export["sha256"]:
            raise ValueError(f"Exportação R178 alterada em {branch}")
        model = parse(path.read_text(encoding="cp1252"))
        connections = model["tables"]["CONNECTIVITY - FRAME"]
        frames = {}
        for key in SAMPLES:
            ends = model["frames"][key]
            edge_z = 177.4 if key == "304" else 20.0
            edge_index, = [i for i, p in enumerate(ends) if p[2] == edge_z]
            row, = [r for r in connections if r["Frame"] == key]
            joint = row[("JointI", "JointJ")[edge_index]]
            frames[key] = dict(endsCm=ends, edgeJointId=joint, edgeCoordinatesCm=model["joints"][joint],
                sameJointFrameIds=[r["Frame"] for r in connections if joint in (r["JointI"], r["JointJ"])],
                directRestraints=[r for r in model["tables"]["JOINT RESTRAINT ASSIGNMENTS"] if r["Joint"] == joint],
                directSprings=[r for r in model["tables"]["JOINT SPRING ASSIGNMENTS 1 - UNCOUPLED"] if r["Joint"] == joint])
        supports = []
        for key in ("163", "164"):
            row, = [r for r in connections if r["Frame"] == key]
            low, high = sorted([row["JointI"], row["JointJ"]], key=lambda j: model["joints"][j][2])
            lower, upper = model["joints"][low], model["joints"][high]
            if lower[:2] != upper[:2] or (lower[2], upper[2]) != (0,20):
                raise ValueError("Geometria inesperada no marcador de apoio")
            fix, = [r for r in model["tables"]["JOINT RESTRAINT ASSIGNMENTS"] if r["Joint"] == low]
            if any(fix[d] != "YES" for d in ("U1","U2","U3","R1","R2","R3")):
                raise ValueError("Restrição inesperada na base do marcador")
            supports.append(dict(frame=key, lowJoint=low, highJoint=high, lowerCm=lower, upperCm=upper,
                restraintsAtLowJoint=fix, connectedAtHighJoint=[r["Frame"] for r in connections
                if high in (r["JointI"],r["JointJ"])]))
        branches[branch] = dict(source=str(path), sha256=export["sha256"], frames=frames, idealizedEndSupports=supports)
    for key in SAMPLES:
        if branches["CAD"]["frames"][key]["endsCm"] != branches["BIM"]["frames"][key]["endsCm"]:
            raise ValueError(f"Extremidades diferentes entre referências R178 na barra {key}")
    samples = {}
    for key, (suffix, values) in SAMPLES.items():
        file = OUT / f"CAD-axiais-{suffix}-0.png"
        samples[key] = dict(displayedValuesKNPerM=values, evidence=file.name, sha256=sha(file))
    result = dict(revision="H03/R193", inspectedBranch="CAD", readOnly=True,
        sourceProject=str(project), sourceProjectSha256=sha(project), geometryReferenceRevision="H03/R178",
        diagram="Elástico - Axiais", combination="1.4G1+1.4G2+1.4Q+0.7QT", legendMinMaxKNPerM=[-165.05,87.97],
        samples=samples, geometryReferences=branches, observedEndRestraint309="Engastado",
        displayedLocalStiffnessMultipliers309=dict(flexion=1,torsion=1,axial=1),
        geometryMatchIsCrossRevision=True, fullCombinationEnvelopeInspected=False,
        sampleShowsGoverningAnchorageLength=False, BIMForcesMeasured=False, structuralApproval=False)
    (OUT / "R193-leitura.json").write_text(json.dumps(result, ensure_ascii=False, indent=2),encoding="utf-8")
    print(f"{len(samples)} barras localizadas nos dois arquivos de referência. PRJ R192 preservado.")


if __name__ == "__main__":
    main()
