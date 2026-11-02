# Retomada R162 — 02/11/2026

Ler `LEIA-ME-R162.md` antes de editar. Trabalho escrito fora do escopo.

- Revit autoral atual continua R160, com 63 elementos da edificação, escada de 17 espelhos e apenas V16 frontal entre P4/P10. P12/P13 removidos. Interferência J4 pendente, sem autorização para modificar a janela.
- CAD autoral atual continua nas três formas R160. Eberick CAD R161 recebeu nível do patamar e V16, mas falta V15/laje de circulação e escada. L6-N1 Revit tem candidata espacial L5 Eberick; não editar a L6 pelo nome.
- Receptor bruto BIM: `D:\TCC\outputs\R161-R160-IFC-BRUTO-NAO-EXECUTAR`. Preservado, 52 origens, sem lajes/escada nativas no IFC4. A viga de patamar foi renomeada V1, seção 20 × 30, geometria conferida.
- Receptor experimental ativo: `D:\TCC\outputs\R162-R160-VIGAS-NOMINAIS-NAO-EXECUTAR`. Recebeu IFC explicitamente derivado com geometria nominal das 30 vigas. Não é o modelo final BIM de cálculo. Configuração inicial e nove níveis brutos mantidos.
- R162 real: 52 origens reportadas, 33 partes de vigas/64 de pilares; 26 origens de vigas associadas, sem diferenças de topo/altura/largura nas partes associadas. Cinco partes sem associação longitudinal segura; investigar antes de promover resultado.
- Comparação da mesma amostra: 24 origens comuns; oito diferenças de topo/altura no bruto e zero no derivado. Não se concluiu correção integral nem aprovação. As 12 diferenças nominais R161 já tinham topo rebaixado no IFC Revit; não atribuir todas ao Eberick.
- Próximo passo: conferir comprimentos e ligações no receptor derivado; depois preparar cópia para tratar níveis e materiais sem alterar os controles. Integrar escada/lajes/cargas e aplicar revisão equivalente ao CAD. Apoio inferior da escada e J4 continuam pendentes.
- Tempo R162: script 1.905,0525 ms; recepção parcial 275.661 ms; observação de geração IFC4 1.191 ms. Desenvolvimento do código não integralmente medido. Não usar como ranking final.
- Dados e evidências em `D:\TCC\outputs\Intercambio-H03-R162-SECOES-NOMINAIS-NAO-EXECUTAR`; 4 testes Python R162 + ensaios reais separados. R161 teve 26 testes Python. Não houve cálculo estrutural novo.
- Referências R148 CAD/BIM e cópia BIM R161 intactas. Preservar arquivos originais e mudanças locais não relacionadas. Não executar geração R162 sobre saída existente. Não publicar/push sem solicitação.
