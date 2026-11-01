"""Controle sem W15 para comparar a malha de 10 cm com a R133."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1]/'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT/'Controle-Grelha-H03-R134-SEM-W15-NAO-EXECUTAR'
module.PAIRS = [
    ('CAD', '30-H03-R116-CAD-P2-NAO-EXECUTAR', '54-H03-R134-CAD-GRELHA-SEM-W15-NAO-EXECUTAR'),
    ('BIM', '31-H03-R116-BIM-P2-NAO-EXECUTAR', '55-H03-R134-BIM-GRELHA-SEM-W15-NAO-EXECUTAR')]
if __name__ == '__main__':
    module.main()
