"""Cópias R116 para testar captura com maior aproximação, sem alterar referências."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Faixa-W03-H03-R129-ESTUDO-NAO-EXECUTAR'
module.PAIRS=[('CAD','30-H03-R116-CAD-P2-NAO-EXECUTAR','42-H03-R129-CAD-W03-FAIXA-NAO-EXECUTAR'),
              ('BIM','31-H03-R116-BIM-P2-NAO-EXECUTAR','43-H03-R129-BIM-W03-FAIXA-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
