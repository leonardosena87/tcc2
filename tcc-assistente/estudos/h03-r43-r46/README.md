# H03/R43–R46: recepção dos dois fluxos no Eberick

Registro acadêmico de 28/10/2026. **NÃO DIMENSIONADO — NÃO EXECUTAR.** Os arquivos nativos de trabalho e as evidências completas permanecem em `D:/TCC`; esta pasta mantém os instrumentos e resultados pertinentes no repositório. Não contém normas protegidas, RVT/DWG/PRJ, credenciais ou dependências instaladas.

Estado observado: referências CAD com 62 contornos recebidos em dois pavimentos, sem lançamento estrutural nativo; ramo BIM com 22 trechos de pilares e 29 vigas lógicas recebidos e conferidos geometricamente após adaptação explícita do IFC. A saída BIM apresenta 32 sólidos de viga, zero lajes e oito erros de esquema em metadados IFC. As 11 lajes, ações e vínculos permanecem pendentes. Não se realizou cálculo estrutural da H03.

Os resultados são observações de um caso exploratório. Não há ranking ou tempo total defensável dos fluxos. Consultar o protocolo para distinguir as próximas medições controladas dos intervalos já obtidos. O trabalho escrito não foi alterado nesta etapa.

## Reprodução no ambiente do estudo

Os scripts assumem a estrutura local `D:/TCC`, seus IFCs/DXFs de evidência e os arquivos históricos de auditoria R17. O auditor IFC usa IfcOpenShell em `D:/TCC/work/ifc/deps`; não instala dependências nem opera os programas gráficos. Não são executáveis independentes dos dados locais.

Com o Python do ambiente, executar as cópias em `D:/TCC/work`:

```text
python D:/TCC/work/auditar-cad-h03-r45.py
python D:/TCC/work/auditar-h03-r46.py
python D:/TCC/work/conferir-reabertura-h03-r46.py
```

O segundo script lê a primeira exportação do Eberick no caminho indicado. Após nova exportação, preservar a leitura inicial antes de repeti-lo; ele grava relatórios de auditoria. O terceiro compara a exportação posterior à reabertura com a geometria inicial preservada. A reabertura propriamente dita foi efetuada no Eberick, não simulada por esses scripts.

## Validação executada

Executaram-se as auditorias contra os arquivos reais recebidos: 62 contornos e 66 conteúdos de texto CAD; 22/22 trechos de pilares e 29/29 vigas lógicas BIM; persistência de classes, nomes, GUIDs e caixas envolventes após reabertura e nova exportação. Os controles em memória detectaram retirada/duplicação de parte de viga, alteração de altura, perda de contorno/texto e escala incorreta. Esses controles são testes do instrumento, separados das ações reais nos programas.

Não houve chamada real à IA nesses scripts. Não se verificou portabilidade em outro computador, conectividade analítica, armaduras, ELU/ELS ou conformidade normativa final. O índice operacional completo está em `D:/TCC/CONTINUAR-AQUI-H03-2026-10-28.md`.
