import json
from auditar import OUT

if __name__=='__main__':
    d=json.loads((OUT/'R139-resultado.json').read_text(encoding='utf-8'))
    times='\n'.join('| '+b+' | '+f"{v['session']['duracao_ms']/60000:.6f}"+' |' for b,v in d['branches'].items())
    report=f'''# H03/R139 — processo de análise e vínculos da grelha

Consulta parcial, NÃO EXECUTAR. Não houve alteração estrutural, processamento ou nova exportação SAP.

## O que foi conferido

Abriram-se cópias de consulta 64/CAD e 65/BIM da R137, consultando Estrutura → Configurações → Projeto → Análise, Painéis de lajes e Avançado. Todos os diálogos foram cancelados, sem salvar. Os dois PRJs de consulta permaneceram byte a byte iguais aos inicialmente copiados. Os 35 arquivos-fontes da R137 mantiveram SHA-256. As exportações históricas R137/R138 também foram conferidas pelos hashes registrados antes da leitura.

O processo selecionado é **Grelhas + pórtico espacial** em ambos, sem alteração para modelo integrado. O modelo de dimensionamento dos painéis está em **Completo**, e o espaçamento global das lajes maciças está em 50 cm. Isso coexiste com a opção individual 10 × 10 cm/0° da L3, confirmada na R137/R138; não é divergência da gravação individual.

Os campos numéricos nativos consultados coincidiram entre os ramos. As capturas mostram redução na torção de vigas 85%, redução na torção da grelha 40%, coeficientes de rigidez exibidos de vigas 0,4 EcIc, pilares 0,8 EcIc e lajes 0,3 EcIc; P-Delta e flexibilização de ligação com pilar equivalente marcados. São valores registrados, sem nova validação normativa, justificativa ou alteração. Não se presume que todos atuem sobre cada resultado isolado da grelha. A configuração P-Delta apresenta combinação vertical 1.4G1+1.4G2+1.4Q+1.1A+1.4QT e combinação característica G1+G2+Q+A+QT; sua adequação global ainda depende da revisão das ações e combinações do estudo.

Em Avançado, a precisão numérica mostra erro estimado máximo de 2% e valor absoluto mínimo 200, sem unidade exibida nesse campo. Não se atribuiu unidade ao 200 nem se usou esse parâmetro como tolerância física, normativa ou de aceitação do resíduo. A opção salvar automaticamente após processamento está desmarcada. As escolhas de radio/checkbox foram transcritas visualmente; a árvore de acessibilidade não informa seus estados de forma confiável. Os valores editáveis foram extraídos do texto nativo para comparação.

## Inventário da exportação existente

N1 com W20 e seu controle de mesma malha têm o mesmo inventário de vínculos, também coincidente entre CAD e BIM:

| Item | Quantidade |
|---|---:|
| Nós | 1.738 |
| Molas nodais globais | 11 |
| Linhas explícitas de restrições nodais | 1.716 |
| Nós sem linha explícita nessa tabela | 22 |
| Barras com liberação geral registrada | 249 |
| Linha de vinculação parcial registrada | 1 |

As 11 molas têm componentes não nulas R1/R2, com U1/U2/U3/R3 nulos. Seu valor bruto, coordenadas e IDs constam do JSON. Existem 11 linhas com U3 restringido e 1.705 com U3 livre; nas 1.716 linhas, U1/U2/R3 estão restringidos e R1/R2 livres. Os 22 nós sem linha explícita não foram classificados como defeito, instabilidade ou perda de dados: não se executou SAP, e ainda não se verificou o tratamento completo desses nós. Não se criou restrição para completar artificialmente o arquivo.

A vinculação parcial é da barra 3237, com M2I e M3I registrados. Não foram encontradas tabelas com OFFSET ou INSERT no nome, nem tabelas de resultados de reações. A ausência dessas tabelas no arquivo não comprova inexistência de offsets no modelo interno, que pode ter outra representação, nem que algum momento tenha sido omitido. Os arquivos indicam formato SAP2000 12.0.0 e unidade corrente Kgf, cm, C; isso é o metadado de exportação, não evidência de que essa versão do programa foi executada.

As diferenças de cargas nodais globais do pórtico incluem M1/M2 e foram preservadas no JSON. Portanto, a auditoria R138 não ignorou genericamente todos os momentos nodais. O incremento condicional da R138 já inclui r×F e os pares nodais escritos. A diferença residual com N1 permanece: Mx=−1.356,105675790 e My=661,546155234 kgf·cm. Sem as rotações e reações das molas não se demonstrou se algum vínculo explica esses resíduos. A presença de molas é uma pista para investigação, não uma causa comprovada.

## Fundamentação e interpretação

A [documentação primária da AltoQi sobre os processos de análise](https://suporte.altoqi.com.br/hc/pt-br/articles/360001391833) distingue o cálculo separado dos painéis, com transmissão de suas reações ao pórtico, do modelo espacial integrado. A [descrição dos graus de liberdade](https://suporte.altoqi.com.br/hc/pt-br/articles/360002163594) explica a diferença entre as formulações. Essas informações orientam a leitura das configurações, sem substituir a verificação do caso estudado.

A [orientação sobre o editor de grelha](https://suporte.altoqi.com.br/hc/pt-br/articles/360000302893) descreve vínculos semirrígidos em determinadas ligações a offsets rígidos de pilares. Isso torna pertinente conferir vínculos e efeitos locais; não demonstra que esse mecanismo seja a causa do resíduo encontrado. Nenhum critério foi alterado para obter coincidência, reduzir solicitações ou eliminar avisos.

## Tempos e esforço

| Ramo | Sessão de consulta exploratória (min) |
|---|---:|
{times}

Incluem navegação, leitura e latência de ferramentas. No CAD houve uma rejeição por referência de captura já invalidada por nova leitura AX e uma por ponto fora dos limites do diálogo; ambas ocorreram antes do envio do clique e foram corrigidas com nova captura. Não são erros de transferência do CAD/Revit nem alterações de projeto. Não houve intervenção humana, processamento ou inferência isolada medida. A busca bibliográfica, o inventário e a elaboração dos registros não foram cronometrados separadamente. Não somar essas sessões a subintervalos já contidos, nem utilizá-las para ranking de produtividade final.

## Próxima verificação

Obter rotações e reações G2 da grelha com W20 e do controle, incluindo os momentos nos vínculos, e reconciliar a resultante no mesmo sistema de eixos e unidades. Se necessário, comparar modelos em cópias experimentais pareadas, preservando os resultados anteriores; não alterar unilateralmente o processo de um fluxo. A causa do resíduo continua aberta. Não houve aceitação final da W20, dimensionamento, comprovação de convergência ou liberação estrutural. A monografia e os arquivos de autoria RVT/DWG permaneceram intactos.
'''
    (OUT/'LEIA-ME-R139.md').write_text(report,encoding='utf-8')
