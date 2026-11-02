"""Cópias de consulta da configuração de análise; PRJs não editados."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Diagnostico-Transmissao-H03-R139-CONSULTA-NAO-EXECUTAR'
module.PAIRS=[
    ('CAD','60-H03-R137-CAD-W20-GRELHA-NAO-EXECUTAR','64-H03-R139-CAD-CONSULTA-NAO-EXECUTAR'),
    ('BIM','61-H03-R137-BIM-W20-GRELHA-NAO-EXECUTAR','65-H03-R139-BIM-CONSULTA-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
