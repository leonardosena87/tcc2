"""Prepara diagnostico pareado exploratorio, com origens R102 preservadas."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1] / 'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT / 'Diagnostico-H03-R104-EXPLORATORIO-NAO-EXECUTAR'
module.PAIRS = [
    ('CAD', '16-H03-R102-CAD-QT-VERTICAL-NAO-EXECUTAR', '18-H03-R104-CAD-DIAGNOSTICO-NAO-EXECUTAR'),
    ('BIM', '17-H03-R102-BIM-QT-VERTICAL-NAO-EXECUTAR', '19-H03-R104-BIM-DIAGNOSTICO-NAO-EXECUTAR'),
]
if __name__ == '__main__':
    module.main()
