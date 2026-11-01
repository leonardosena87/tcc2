"""Cópias pareadas para análise isolada W20, preservando o lançamento R135."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_copies',Path(__file__).parents[1]/'h03-r102/preparar.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = module.ROOT/'Analise-W20-H03-R136-ESTUDO-NAO-EXECUTAR'
module.PAIRS = [
    ('CAD','56-H03-R135-CAD-W20-LAJE-NAO-EXECUTAR','58-H03-R136-CAD-W20-ANALISE-NAO-EXECUTAR'),
    ('BIM','57-H03-R135-BIM-W20-LAJE-NAO-EXECUTAR','59-H03-R136-BIM-W20-ANALISE-NAO-EXECUTAR')]
if __name__=='__main__':
    module.main()
