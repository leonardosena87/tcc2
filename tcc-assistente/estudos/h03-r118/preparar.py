"""Copias para consulta de armadura sem editar ou salvar propriedades."""
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('prepare_copies', Path(__file__).parents[1] / 'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT / 'Armadura-H03-R118-CONSULTA-NAO-EXECUTAR'
module.PAIRS = [('CAD', '30-H03-R116-CAD-P2-NAO-EXECUTAR', '32-H03-R118-CAD-ARMADURA-NAO-EXECUTAR'),
                ('BIM', '31-H03-R116-BIM-P2-NAO-EXECUTAR', '33-H03-R118-BIM-ARMADURA-NAO-EXECUTAR')]
if __name__ == '__main__': module.main()
