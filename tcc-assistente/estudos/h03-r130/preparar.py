"""Cópias R116 para ensaio isolado da linha W15 sobre laje."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Linha-W15-H03-R130-ESTUDO-NAO-EXECUTAR'
module.PAIRS=[('CAD','30-H03-R116-CAD-P2-NAO-EXECUTAR','44-H03-R130-CAD-W15-LAJE-NAO-EXECUTAR'),
              ('BIM','31-H03-R116-BIM-P2-NAO-EXECUTAR','45-H03-R130-BIM-W15-LAJE-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
