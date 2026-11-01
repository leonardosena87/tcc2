"""Cópias para consultar exportações analíticas W15 e referência R116."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Distribuicao-W15-H03-R132-CONSULTA-NAO-EXECUTAR'
module.PAIRS=[
 ('CAD-W15','46-H03-R131-CAD-W15-ANALISE-NAO-EXECUTAR','48-H03-R132-CAD-W15-CONSULTA-NAO-EXECUTAR'),
 ('BIM-W15','47-H03-R131-BIM-W15-ANALISE-NAO-EXECUTAR','49-H03-R132-BIM-W15-CONSULTA-NAO-EXECUTAR'),
 ('CAD-BASE','30-H03-R116-CAD-P2-NAO-EXECUTAR','50-H03-R132-CAD-BASE-CONSULTA-NAO-EXECUTAR'),
 ('BIM-BASE','31-H03-R116-BIM-P2-NAO-EXECUTAR','51-H03-R132-BIM-BASE-CONSULTA-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
