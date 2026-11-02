"""Controles próprios L3 fina, sem W20, a partir da base preservada R116."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Controle-L3-H03-R138-SEM-W20-NAO-EXECUTAR'
module.PAIRS=[
    ('CAD','30-H03-R116-CAD-P2-NAO-EXECUTAR','62-H03-R138-CAD-L3-SEM-W20-NAO-EXECUTAR'),
    ('BIM','31-H03-R116-BIM-P2-NAO-EXECUTAR','63-H03-R138-BIM-L3-SEM-W20-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
