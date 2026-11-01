"""Ensaio independente da parede W20 sobre L3, sem incorporar a W15 experimental."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1]/'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT/'Linha-W20-H03-R135-ESTUDO-NAO-EXECUTAR'
module.PAIRS = [
    ('CAD', '30-H03-R116-CAD-P2-NAO-EXECUTAR', '56-H03-R135-CAD-W20-LAJE-NAO-EXECUTAR'),
    ('BIM', '31-H03-R116-BIM-P2-NAO-EXECUTAR', '57-H03-R135-BIM-W20-LAJE-NAO-EXECUTAR')]
if __name__ == '__main__':
    module.main()
