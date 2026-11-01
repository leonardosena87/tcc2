"""Cópias da R116 para testar delimitação física de carga sem reaproveitar o ensaio de viga inteira."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Trecho-W03-H03-R126-ESTUDO-NAO-EXECUTAR'
module.PAIRS=[('CAD','30-H03-R116-CAD-P2-NAO-EXECUTAR','40-H03-R126-CAD-W03-PARCIAL-NAO-EXECUTAR'),
              ('BIM','31-H03-R116-BIM-P2-NAO-EXECUTAR','41-H03-R126-BIM-W03-PARCIAL-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
