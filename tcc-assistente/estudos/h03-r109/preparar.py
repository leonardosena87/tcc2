"""Copias R102 para sensibilidade VP1-A, sem substituir o conjunto principal."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1] / 'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT / 'Varanda-H03-R109-SENSIBILIDADE-NAO-EXECUTAR'
module.PAIRS = [
    ('CAD', '16-H03-R102-CAD-QT-VERTICAL-NAO-EXECUTAR', '22-H03-R109-CAD-VARANDA-NAO-EXECUTAR'),
    ('BIM', '17-H03-R102-BIM-QT-VERTICAL-NAO-EXECUTAR', '23-H03-R109-BIM-VARANDA-NAO-EXECUTAR'),
]
if __name__ == '__main__':
    module.main()
