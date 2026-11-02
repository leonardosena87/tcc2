"""Cópias do cadastro R145 para ensaio parcial de análise estática."""
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('copies', Path(__file__).parents[1] / 'h03-r102/preparar.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.OUT = mod.ROOT / 'Analise-H03-R146-FORRO-N1-NAO-EXECUTAR'
mod.PAIRS = [
    ('CAD','70-H03-R145-CAD-FORRO-N1-NAO-EXECUTAR','72-H03-R146-CAD-FORRO-N1-NAO-EXECUTAR'),
    ('BIM','71-H03-R145-BIM-FORRO-N1-NAO-EXECUTAR','73-H03-R146-BIM-FORRO-N1-NAO-EXECUTAR')]
if __name__ == '__main__':
    mod.main()
