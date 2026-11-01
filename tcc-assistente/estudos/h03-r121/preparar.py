"""Cópias para conferir o lançamento de uma faixa de parede sem abertura."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1] / 'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT / 'Parede-W03-H03-R121-ESTUDO-NAO-EXECUTAR'
module.PAIRS = [('CAD', '30-H03-R116-CAD-P2-NAO-EXECUTAR', '36-H03-R121-CAD-W03-NAO-EXECUTAR'),
                ('BIM', '31-H03-R116-BIM-P2-NAO-EXECUTAR', '37-H03-R121-BIM-W03-NAO-EXECUTAR')]
if __name__ == '__main__': module.main()
