import json
from auditar import OUT

if __name__=='__main__':
    d=json.loads((OUT/'R137-resultado.json').read_text(encoding='utf-8'))
    visual={'method':'Transcrição visual pela IA das imagens, não extração automática nem leitura nativa dos números do resumo.',
        'branches':{b:{'image':b+'-resumo-analise-2.jpg','verticalLoadsDisplayedTf':{'PP':'75.69','G2':'12.30','Q':'17.11','QT':'1.78','total':'106.88'},
        'areaM2':'132.81','loadPerAreaKgfM2':'804.78','warning':'Relação de carga por área não usual para edifícios',
        'horizontalCm':{'X+':'0.20','X-':'0.20','Y+':'0.20','Y-':'0.20'},'relativeCm':'0.17',
        'relativeDirection':'N1/Y-' if b=='CAD' else 'TCC-cdd31967-N1/Y+',
        'gammaZDisplayed':{'X+':'1.10','X-':'1.08','Y+':'1.06','Y-':'1.05'},'fullTopDisplacementTranscribed':False} for b in ['CAD','BIM']}}
    (OUT/'observacoes-visuais.json').write_text(json.dumps(visual,ensure_ascii=False,indent=2),encoding='utf-8')
    times='\n'.join('| '+b+' | '+f"{v['session']['duracao_ms']/60000:.6f}"+' | '+f"{v['processingObservation']['duracao_ms']/1000:.3f}"+' |' for b,v in d['branches'].items())
    report=f'''# H03/R137 — sensibilidade da W20 à malha da L3

Estudo parcial, NÃO EXECUTAR. Não constitui dimensionamento nem liberação estrutural.

## Alteração e verificação

Em cópias independentes 60/CAD e 61/BIM da R136, alterou-se somente a discretização individual da L3/N1 de 50 × 50 para 10 × 10 cm, mantendo o ângulo 0°. A laje permaneceu maciça, h=14 cm, elevação 0, Q=1,5 kN/m², revestimento=1,0 kN/m² e ambiente Externo. As duas configurações de malha foram conferidas em diálogo nativo após salvar, fechar e reabrir. No BIM também se conferiu novamente a carga extra 4,71065 kN/m e carga automática de parede zero; no CAD essa leitura específica é da R135, sem nova leitura do diálogo de carga nesta revisão.

Não se moveu a W20/S58: hipótese de segmento (810;10) a (810;380) cm, comprimento 3,70 m. Sua integral nominal é 17,429405 kN, sob a hipótese de peso/altura registrada na R135. Trata-se somente do S58, sem aberturas, sem incluir os trechos de extremidade sobre vigas e sem validar a parede inteira. A convenção observada R125 de 100 kgf/kN foi mantida para a comparação de escrita; ela não equivale à conversão SI exata.

Houve dificuldade de seleção do rótulo CAD, sobreposto à W20 e à anotação. Tentou-se ocultar CR-Paredes, mas a linha continuou aparecendo; após ampliação e seleção abriu-se a L3. Não se provou a causa da dificuldade nem que a ocultação a resolveu. A visibilidade do nível foi restaurada, retornando o perfil Geral, antes da gravação. O nome local CAD-nivel-parede-oculto-configurado é inadequado: a captura ainda mostrava a caixa marcada. Esse grupo e CAD-croqui-parede-oculta permanecem locais, excluídos do conjunto público. Não são evidência de carga removida.

## Resultados das seis tabelas exportadas

| Indicador N1 | R136 — malha original | R137 — L3 refinada |
|---|---:|---:|
| Nós totais | 467 | 1.738 |
| Barras totais | 838 | 3.325 |
| Forças nodais G2 | 8 | 37 |
| Fz escrita (kgf) | −1.742,9408 | −1.742,9405 |
| Centro X;Y (cm) | 784,17;195,005 | 810;195 |
| Distância ao centro nominal (cm) | 25,83000048 | 0 |

As 37 linhas nodais G2, incluindo IDs, forças e coordenadas, coincidiram entre os ramos. Na precisão escrita, Fz e os primeiros momentos em relação à origem coincidem com o nominal: Mx=−339.873,39750 kgf·cm e My=1.411.781,80500 kgf·cm. A resultante em N1 deixou de apresentar o deslocamento observado na malha original. Isso descreve a exportação deste ensaio; não demonstra convergência da solução, equivalência completa entre modelo interno e exportado, exatidão física ou aceitação de efeitos locais.

A N2 permaneceu com 443 nós e 794 barras, sem diferença em nenhuma tabela de cada ramo. O pórtico permaneceu com 110 nós e 133 barras e os mesmos extremos I/J ordenados; houve alteração de 395 para 728 registros pontuais entre os conjuntos removido/adicionado e de nove registros nodais em cada conjunto. Essas diferenças acompanham a mudança de malha e não isolam a W20. Não representam quantidade de correções, defeitos ou ações de usuário.

Ainda não existe nesta revisão o controle próprio com L3 10 × 10 cm sem W20. A R134 refinava L4 e não serve para esse controle. Portanto, não se calculou um incremento isolado do pórtico e não se validou a transmissão local aos apoios. Não se executou SAP2000: apenas se leu a exportação de texto gerada pelo Eberick.

## Processamento e qualidade da evidência

Ambos foram processados com avisos no mesmo escopo: análise estática linear e deslocamentos do pórtico com rigidez configurada, sem dimensionamento, flechas das lajes, análise fissurada ou dinâmica. O resumo visual exibiu total 106,88 tf, área 132,81 m², relação 804,78 kgf/m² e aviso de relação não usual; γz exibido 1,10/1,08/1,06/1,05. O arredondamento 1,10 não prova igualdade do valor interno ao limite ou aprovação normativa. Não foi transcrito o quadro completo de deslocamentos do topo.

Os números do resumo foram transcritos visualmente das imagens identificadas em observacoes-visuais.json. O texto de acessibilidade pode mostrar um diálogo anterior; não foi tratado como extração numérica desse resumo. Na retomada mudou-se o adaptador de controle para cua_repl. Duas tentativas por índice retornaram elemento indisponível e uma captura com emit:false foi rejeitada antes de capturar; a execução prosseguiu por coordenadas e capturas explícitas. São ocorrências do controle da IA, sem atribuição a perda de informação do modelo.

Os 35 arquivos-fontes da R136 mantiveram seus hashes. As duas árvores R137 fechadas foram congeladas e verificadas (16 arquivos CAD e 19 BIM). O teste ZIP verificou a integridade dos dois PRJs; não valida seu conteúdo estrutural. Os caminhos e hashes das seis exportações e as contagens das diferenças por tabela constam em R137-resultado.json; os registros completos permanecem nos arquivos exportados, permitindo reproduzir a auditoria.

## Tempos e esforço

| Ramo | Sessão exploratória (min) | Comando até término observado (s) |
|---|---:|---:|
{times}

O segundo intervalo está contido no primeiro: não somar. O tempo CAD inclui diagnóstico prolongado de seleção e retomada de ferramenta. O encerramento da sessão BIM foi marcado ao concluir a exportação; a leitura adicional da W20 e o fechamento vieram depois, com horários nas capturas. A preparação de scripts, auditoria, redação e arquivamento não foi medida separadamente. Não houve intervenção humana nesta etapa. Não se isolou tempo de inferência, tokens, energia ou custo da IA. Essas sessões exploratórias não permitem ranking de produtividade ou economia percentual entre os fluxos finais.

## Continuidade

Criar controles pareados próprios sem W20 com a mesma malha L3 10 × 10 cm/0°, processar o mesmo escopo, salvar/reabrir/exportar e conferir igualdade da geometria ordenada antes de interpretar incrementos. Depois avaliar reações locais e sensibilidade adicional. A W20 ainda não foi aceita como solução final. Permanecem outras paredes e aberturas, reservatório, cobertura, combinações, ELU/ELS completo e a rodada prospectiva de tempos. Não se alterou a monografia nem os arquivos de autoria RVT/DWG nesta etapa.
'''
    (OUT/'LEIA-ME-R137.md').write_text(report,encoding='utf-8')
