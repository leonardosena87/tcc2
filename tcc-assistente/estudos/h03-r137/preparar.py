"""Sensibilidade da W20 a malha individual L3 mais fina, em cópias pareadas."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Grelha-W20-H03-R137-SENSIBILIDADE-NAO-EXECUTAR'
module.PAIRS=[
    ('CAD','58-H03-R136-CAD-W20-ANALISE-NAO-EXECUTAR','60-H03-R137-CAD-W20-GRELHA-NAO-EXECUTAR'),
    ('BIM','59-H03-R136-BIM-W20-ANALISE-NAO-EXECUTAR','61-H03-R137-BIM-W20-GRELHA-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
