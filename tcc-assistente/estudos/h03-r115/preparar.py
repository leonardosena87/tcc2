"""Copias R109 para ensaio das parcelas P2 sem alterar fontes e resultados R111."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.OUT=module.ROOT/'Telhado-P2-H03-R115-SENSIBILIDADE-NAO-EXECUTAR'
module.PAIRS=[('CAD','22-H03-R109-CAD-VARANDA-NAO-EXECUTAR','28-H03-R115-CAD-P2-NAO-EXECUTAR'),
              ('BIM','23-H03-R109-BIM-VARANDA-NAO-EXECUTAR','29-H03-R115-BIM-P2-NAO-EXECUTAR')]
if __name__=='__main__':module.main()
