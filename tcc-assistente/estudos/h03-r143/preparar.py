"""Cópias independentes para delimitar W05 em viga, sem editar PRJ."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.OUT=mod.ROOT/'Paredes-Vigas-H03-R143-NAO-EXECUTAR'
mod.PAIRS=[
    ('CAD','30-H03-R116-CAD-P2-NAO-EXECUTAR','68-H03-R143-CAD-W05-NAO-EXECUTAR'),
    ('BIM','31-H03-R116-BIM-P2-NAO-EXECUTAR','69-H03-R143-BIM-W05-NAO-EXECUTAR')]
if __name__=='__main__':mod.main()
