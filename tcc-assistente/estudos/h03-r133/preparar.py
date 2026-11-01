"""Cópias W15 R131 para sensibilidade de grelha apenas na laje L4/N1."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Grelha-W15-H03-R133-SENSIBILIDADE-NAO-EXECUTAR'
module.PAIRS=[('CAD','46-H03-R131-CAD-W15-ANALISE-NAO-EXECUTAR','52-H03-R133-CAD-W15-GRELHA-NAO-EXECUTAR'),
              ('BIM','47-H03-R131-BIM-W15-ANALISE-NAO-EXECUTAR','53-H03-R133-BIM-W15-GRELHA-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
