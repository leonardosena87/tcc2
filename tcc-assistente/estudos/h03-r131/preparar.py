"""Preserva R130 e prepara análise isolada da linha W15."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Analise-W15-H03-R131-ESTUDO-NAO-EXECUTAR'
module.PAIRS=[('CAD','44-H03-R130-CAD-W15-LAJE-NAO-EXECUTAR','46-H03-R131-CAD-W15-ANALISE-NAO-EXECUTAR'),
              ('BIM','45-H03-R130-BIM-W15-LAJE-NAO-EXECUTAR','47-H03-R131-BIM-W15-ANALISE-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
