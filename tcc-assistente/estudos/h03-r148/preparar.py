"""Cópias R146 para triagem de dimensionamento sob cargas ainda parciais."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.OUT=mod.ROOT/'Dimensionamento-H03-R148-PARCIAL-NAO-EXECUTAR'
mod.PAIRS=[
 ('CAD','72-H03-R146-CAD-FORRO-N1-NAO-EXECUTAR','74-H03-R148-CAD-DIM-PARCIAL-NAO-EXECUTAR'),
 ('BIM','73-H03-R146-BIM-FORRO-N1-NAO-EXECUTAR','75-H03-R148-BIM-DIM-PARCIAL-NAO-EXECUTAR')]
if __name__=='__main__':mod.main()
