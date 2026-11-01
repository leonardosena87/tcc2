"""Copias de consulta para conferir referencias verticais sem editar os PRJs."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1] / 'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT / 'Altimetria-H03-R113-CONSULTA-NAO-EXECUTAR'
module.PAIRS = [
    ('CAD', '24-H03-R111-CAD-VARANDA-NAO-EXECUTAR', '26-H03-R113-CAD-ALTIMETRIA-NAO-EXECUTAR'),
    ('BIM', '25-H03-R111-BIM-VARANDA-NAO-EXECUTAR', '27-H03-R113-BIM-ALTIMETRIA-NAO-EXECUTAR'),
]
if __name__ == '__main__':
    module.main()
