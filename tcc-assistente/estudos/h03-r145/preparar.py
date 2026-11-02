"""Cópias pareadas para acrescentar forro sob as quatro lajes internas N1."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.OUT=mod.ROOT/'Forro-N1-H03-R145-NAO-EXECUTAR'
mod.PAIRS=[
 ('CAD','30-H03-R116-CAD-P2-NAO-EXECUTAR','70-H03-R145-CAD-FORRO-N1-NAO-EXECUTAR'),
 ('BIM','31-H03-R116-BIM-P2-NAO-EXECUTAR','71-H03-R145-BIM-FORRO-N1-NAO-EXECUTAR')]
if __name__=='__main__':mod.main()
