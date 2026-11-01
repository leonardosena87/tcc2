"""Relata o controle sem mudar as conclusões históricas da R133."""
import json
import shutil
from auditar import HERE, OUT

def main():
    data = json.loads((OUT/'R134-resultado.json').read_text(encoding='utf-8'))
    times = '\n'.join(f"| {b} | {r['sessionTime']['wallMs']/60000:.3f} min | {r['processingTimeObservation']['durationMs']/1000:.3f} s |"
                      for b, r in data['branches'].items())
    text = f'''# H03/R134 — controle de mesma malha sem W15

## Resultado e alcance

Concluiu-se o controle que faltava à R133: duas cópias da referência R116, sem a W15, receberam na L4/N1 a mesma malha individual de 10 × 10 cm, ângulo 90°. São os diretórios 54-H03-R134-CAD-GRELHA-SEM-W15-NAO-EXECUTAR e 55-H03-R134-BIM-GRELHA-SEM-W15-NAO-EXECUTAR em D:/TCC/outputs. Não se removeu a parede de um projeto existente: partiu-se da referência sem essa carga, preservando os experimentos anteriores.

Após processar, salvar e fechar, reabriu-se cada projeto antes de exportar as tabelas textuais. Em cada ramo, comparou-se a própria R134 sem W15 à própria R133 com W15. Assim se evita confundir o efeito da mudança de malha com a inclusão da carga. Não se realizou ensaio adicional de malha de 5 cm ou de alinhamento.

| Comparação entre controle e W15, em cada ramo | Evidência nas tabelas exportadas |
|---|---|
| N1 | 2.236 nós e 4.299 barras em ambos; IDs, coordenadas e extremidades ordenadas iguais |
| N1: única tabela diferente | JOINT LOADS - FORCE: dez forças acrescentadas, nenhuma removida |
| Forças acrescentadas | Todas G2, verticais globais, sem momentos nodais adicionais; soma −446,0250 kgf |
| N2 | 443 nós, 794 barras; todas as tabelas iguais |
| Pórtico | 110 nós e 133 barras; IDs e geometria ordenada iguais dentro do próprio ramo |
| Pórtico: diferenças | FRAME LOADS - POINT: 267 linhas removidas e 267 acrescentadas; JOINT LOADS - FORCE: 5 removidas e 5 acrescentadas; todas G2 |

Essas linhas substituídas não são 267/5 operações de correção, elementos com defeito ou ocorrências de perda de transferência. São diferenças de registros de carga após a inclusão da W15, sob a mesma discretização em cada ramo. As tabelas exportadas de seções, materiais e demais configurações não diferem nesse controle. Isso não afirma que toda informação interna do Eberick foi exportada.

As dez forças acrescentadas na N1 coincidem entre CAD e BIM. Reproduziu-se o centro (499,434;493,36)cm e o afastamento de 2,53574cm ante o centro ideal (497,5;495)cm. O controle confirma que essa diferença, na representação N1 exportada, não surgiu por comparar malhas diferentes. Mantêm-se os resíduos de primeiros momentos já registrados na R133. Não foi estabelecido limite de aceitação ou demonstrada convergência.

## Transmissão ao pórtico: interpretação condicional

As cargas pontuais das barras utilizam LOCAL/2 e estações relativas, enquanto as cargas nodais são globais e incluem momentos. A análise preserva I/J: a posição é calculada como r = rI + t(rJ − rI). A inversão das extremidades exige estação complementar para manter a posição física. Não se ordenaram extremos antes de calcular a posição.

A [documentação oficial dos eixos do SAP2000](https://docs.csiamerica.com/help-files/sap/Menus/Assign/Frame/Frame_Local_Axes.htm) explica a orientação automática e sua rotação por ângulo. O [manual de referência CSI, páginas impressas 109–110](https://docs.csiamerica.com/manuals/sap2000/CSiRefer.pdf#page=131), define o sentido +Z do eixo 2 padrão para barras horizontais. Neste ensaio, as 17 barras com cargas pontuais alteradas são horizontais e não possuem registro explícito de rotação na tabela correspondente. A interpretação abaixo **assume que a ausência de atribuição conserva o padrão SAP**. Não se comprovou essa hipótese por importação e execução no SAP2000, nem sua identidade com os eixos internos do Eberick. O cabeçalho exportado declara formato SAP2000 12.0.0; isso não representa programa instalado ou executado.

Sob essa hipótese e somando r × F aos momentos nodais, encontrou-se o mesmo agregado nos dois ramos:

| Incremento interpretado W15 no pórtico | Valor |
|---|---:|
| Fz das cargas pontuais nas barras | −478,9708 kgf |
| Fz das cargas nodais globais | +32,9453 kgf |
| Fz total | −446,0255 kgf |
| Mx em torno da origem | −218.931,455995850 kgf·cm |
| My em torno da origem | +222.724,528326086 kgf·cm |

Ante as dez forças aplicadas na N1, os resíduos são Fz=−0,0005kgf, Mx=+1.119,438004150kgf·cm e My=−35,521523914kgf·cm. A diferença de força é pequena na precisão exportada, mas isso não prova conservação completa de momentos. Não se atribuiu a diferença de Mx/My a arredondamento, excentricidade, trecho rígido ou falha do software: a causa permanece aberta. Não se calculou um centro de forças do agregado com momentos nodais para compará-lo indevidamente ao centro da linha ideal.

São incrementos de **cargas aplicadas ao modelo exportado do pórtico**, não reações finais nos apoios idealizados da superestrutura. Não se conferiram aqui todas as reações ou esforços internos individuais. A W15 continua experimental, sem aceitação final.

## Processamento, tempo e qualidade da evidência

O escopo de processamento foi igual ao da R133: estática linear e deslocamentos do pórtico com rigidez configurada; sem dimensionamento, flechas das lajes, rigidez fissurada ou dinâmica. Ambos terminaram com avisos. O resumo visual dos dois mostrou PP75,69tf, G10,56tf, Q17,11tf, QT1,78tf e total105,14tf; área132,81m² e relação791,65kgf/m², com aviso de relação de carga por área não usual. Na própria R133 com W15, G11,00tf e total105,59tf. As diferenças exibidas de0,44tf e0,45tf são preservadas como leituras arredondadas; não representam integrais exatas distintas.

Os máximos horizontais exibidos são0,20cm; o relativo0,17cm conserva direções diferentes: CAD N1/Y− e BIM TCC-cdd31967-N1/Y+. Gama-Z exibido1,09/1,08/1,06/1,05. Esses números e limites mostrados não constituem aprovação normativa. O topo completo não foi transcrito.

| Ramo | Sessão exploratória | Comando até primeira captura do término |
|---|---:|---:|
{times}

O intervalo do comando está contido na sessão, inclui espera e latência e não mede solver isolado. A sessão CAD contém diagnóstico da captura textual e leitura auxiliar de arquivos; a BIM inclui uma consulta inicial dos arquivos CAD e retomada do submenu Exportar. Não usar esses tempos para ranking final ou ganho de produtividade. A elaboração da auditoria posterior não foi cronometrada separadamente, e tokens/custos/inferência da IA não são conhecidos. Não se registrou intervenção humana nesta etapa.

As imagens foram inspecionadas na interface. A disponibilidade de texto de acessibilidade está explicitada em cada arquivo `*-captura.json`; quando ausente, o UI.txt fica vazio e não sustenta números. `observacoes-visuais.json` é transcrição visual pela IA, distinta de texto extraído. As comparações das tabelas $2k e os agregados numéricos foram calculados pelo código, sem executar SAP2000.

## Preservação e continuidade

Conferiram-se sem alteração os 35 arquivos das fontes R116 e os 35 arquivos das cópias R133. As cópias R134 foram congeladas após processamento, com hashes e caminhos registrados no JSON. A monografia e os modelos de autoria Revit/AutoCAD não foram alterados. Não houve nova importação DWG/IFC.

Este controle resolve a ausência do modelo sem W15 com a mesma malha, apontada na R133, sem alterar o registro histórico daquela revisão. Permanecem abertos a interpretação/transmissão dos momentos, efeitos e reações locais, convergência ou alinhamento da malha e aceitação da W15. A referência R116 permanece preservada; R133/R134 são ensaios específicos, não versões finais liberadas para execução. As outras paredes, aberturas/apoios, reservatório/base/acesso, demais cargas e verificações ELU/ELS continuam pendentes conforme o quadro de fechamento.
'''
    (OUT/'LEIA-ME-R134.md').write_text(text, encoding='utf-8')
    shutil.copyfile(HERE/'observacoes-visuais.json', OUT/'observacoes-visuais.json')

if __name__ == '__main__':
    main()
