import json
from auditar import HERE,OUT,sha

if __name__=='__main__':
    data=json.loads((OUT/'R132-resultado.json').read_text(encoding='utf-8'))
    rows='\n'.join(f"| {b} / {s} | {v['duracao_ms']/60000:.3f} min |" for b,item in data['branches'].items() for s,v in item['sessions'].items())
    md=f'''# H03/R132 — representação analítica da W15

As doze exportações textuais nativas permitem comparar separadamente cada ramo com sua referência R116. Não se executou SAP2000. A consulta utilizou cópias 48/49 para W15 e 50/51 para a referência, preservando os 70 arquivos de origem e os quatro PRJs consultados.

## Achado principal

Na grelha N1, a única tabela alterada em cada ramo é JOINT LOADS - FORCE. A referência não possui cargas nodais G2 nessa tabela; com a W15 aparecem exatamente as duas linhas abaixo, idênticas CAD/BIM:

| Nó | X (cm) | Y (cm) | Z (cm) | Fz (kgf) | Momentos nodais |
|---|---:|---:|---:|---:|---|
| 136 | 463,86 | 468,75 | 320,00 | −223,0125 | zero |
| 158 | 511,59 | 468,75 | 320,00 | −223,0125 | zero |

A soma é −446,025 kgf, coerente com a integral nominal 4,46025 kN pela convenção de exibição observada na R125. Esta relação não é conversão SI exata. São forças aplicadas à grelha, **não reações de apoio**.

A linha desenhada e relida R130 vai de (450;495) a (545;495)cm e tem centro (497,5;495)cm. A resultante das forças exportadas fica em (487,725;468,75)cm. O desvio é ΔX=−9,775cm e ΔY=−26,25cm, distância de aproximadamente28,011cm.

Portanto, conservar a soma da força **não comprova conservar seu ponto de aplicação**. Sem momentos nodais adicionais, os primeiros momentos dessas duas forças na grelha diferem dos de uma linha uniforme na posição indicada:

| Momento em torno da origem | Linha ideal com mesma força | Forças exportadas | Diferença |
|---|---:|---:|---:|
| Mx (kgf·cm) | −220782,375 | −209074,21875 | +11708,15625 |
| My (kgf·cm) | +221897,43750 | +217537,543125 | −4359,894375 |

O cálculo utiliza r×F e as coordenadas globais exportadas. Não compara momentos resistentes nem esforços internos. A diferença foi identificada no modelo exportado; não foi demonstrada a equivalência exata dessa representação com todo o tratamento interno do programa. O impacto nos esforços/flechas e a adequação da aproximação exigem ensaio de sensibilidade.

## Relação com a comparação CAD/BIM

As coordenadas e seis componentes de carga nodal coincidem nos dois ramos. A linha W15 foi acrescentada no Eberick após importar DWG/IFC. O achado pertence à discretização/modelagem comum no receptor; **não demonstra defeito de transferência em um dos fluxos**.

Dentro de cada ramo, a geometria exportada N1 é preservada entre referência e W15; só aparecem as duas forças nodais. Em N2 nenhuma tabela mudou. No pórtico mudaram as tabelas FRAME LOADS - POINT e JOINT LOADS - FORCE, cujo detalhamento bruto é conservado no JSON; não se afirmou equivalência de reações individuais nesta etapa.

Os controles da exportação incluíram pórtico, grelhas N1/N2, seções e coeficientes redutores. Os arquivos são dados exportados para auditoria, não uma validação independente em outro calculador. A W15 continua ensaio parcial, sem aceite final do modelo local.

## Tempos observados

| Consulta | Sessão |
|---|---:|
{rows}

Os tempos incluem abertura, menus, definição de pasta, exportação, capturas e fechamento. A consulta BIM/W15 teve uma retomada de submenu. Não houve novo processamento, não são tempos puros nem ranking. Estes intervalos não se sobrepõem às sessões R130/R131 já encerradas.

## Próximo ensaio

Testar refinamento individual da grelha L4, com os mesmos valores nos dois ramos, preservando cargas e seções. Conferir novamente soma das forças, centro de aplicação, primeiros momentos e resultados. A hipótese de que a malha cause o deslocamento observado ainda precisa ser testada; não será tratada como causa comprovada apenas pela proximidade dos nós.

A documentação oficial permite ajustar o espaçamento por laje no botão Grelha do diálogo Laje ([AltoQi, discretização](https://suporte.altoqi.com.br/hc/pt-br/articles/115004786894)) e reposicionar a grelha ([AltoQi, posicionamento](https://suporte.altoqi.com.br/hc/pt-br/articles/17024104817303)). Trata-se de procedimento do software, não de aprovação normativa ou de recomendação universal de malha.

Não houve edição da monografia, das fontes Revit/AutoCAD ou das referências anteriores. Cargas remanescentes, tanque, escada, vento/combinações, dimensionamento e verificações ELU/ELS continuam pendentes.
'''
    target=OUT/'LEIA-ME-R132.md'
    if target.exists():raise FileExistsError(target)
    target.write_text(md,encoding='utf-8')
    print('Relatorio gerado')
