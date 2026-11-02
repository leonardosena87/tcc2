"""Cópias fechadas R148 para diagnosticar o erro D16, sem alterar armaduras."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
mod.OUT=mod.ROOT/'Diagnostico-H03-R150-D16-NAO-EXECUTAR'
mod.PAIRS=[
 ('CAD','74-H03-R148-CAD-DIM-PARCIAL-NAO-EXECUTAR','76-H03-R150-CAD-CONSULTA-D16-NAO-EXECUTAR'),
 ('BIM','75-H03-R148-BIM-DIM-PARCIAL-NAO-EXECUTAR','77-H03-R150-BIM-CONSULTA-D16-NAO-EXECUTAR')]
if __name__=='__main__':mod.main()
