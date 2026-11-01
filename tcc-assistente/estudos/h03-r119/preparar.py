"""Cópias independentes para consulta das cargas de lajes e paredes."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1] / 'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT / 'Lajes-H03-R119-CONSULTA-NAO-EXECUTAR'
module.PAIRS = [('CAD', '30-H03-R116-CAD-P2-NAO-EXECUTAR', '34-H03-R119-CAD-LAJES-NAO-EXECUTAR'),
                ('BIM', '31-H03-R116-BIM-P2-NAO-EXECUTAR', '35-H03-R119-BIM-LAJES-NAO-EXECUTAR')]
if __name__ == '__main__': module.main()
