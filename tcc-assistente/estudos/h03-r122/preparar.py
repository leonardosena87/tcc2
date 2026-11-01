"""Cópias de consulta da extensão de vigas e cargas do ensaio R121."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT=module.ROOT/'Extensao-W03-H03-R122-CONSULTA-NAO-EXECUTAR'
module.PAIRS=[('CAD','36-H03-R121-CAD-W03-NAO-EXECUTAR','38-H03-R122-CAD-EXTENSAO-NAO-EXECUTAR'),
              ('BIM','37-H03-R121-BIM-W03-NAO-EXECUTAR','39-H03-R122-BIM-EXTENSAO-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
