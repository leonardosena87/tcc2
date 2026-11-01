"""Prepara copias R109 para sensibilidade de processamento da varanda."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1] / 'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT / 'Analise-H03-R111-VARANDA-NAO-EXECUTAR'
module.PAIRS = [
    ('CAD', '22-H03-R109-CAD-VARANDA-NAO-EXECUTAR', '24-H03-R111-CAD-VARANDA-NAO-EXECUTAR'),
    ('BIM', '23-H03-R109-BIM-VARANDA-NAO-EXECUTAR', '25-H03-R111-BIM-VARANDA-NAO-EXECUTAR'),
]
if __name__ == '__main__':
    module.main()
