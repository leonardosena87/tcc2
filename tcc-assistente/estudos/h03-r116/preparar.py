"""Copias R115 para sensibilidade estatica e ELS-DEF com P2, sem dimensionamento."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1] / 'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT / 'Analise-H03-R116-P2-NAO-EXECUTAR'
module.PAIRS = [
    ('CAD', '28-H03-R115-CAD-P2-NAO-EXECUTAR', '30-H03-R116-CAD-P2-NAO-EXECUTAR'),
    ('BIM', '29-H03-R115-BIM-P2-NAO-EXECUTAR', '31-H03-R116-BIM-P2-NAO-EXECUTAR'),
]
if __name__ == '__main__':
    module.main()
