# H03/R144 — escada: compatibilização de cotas e alternativa autorizada para estudo

O corte AA da arquitetura original indica pisos acabados +0,22 m e +3,25 m, patamar +1,70 m, pisada 28 cm e espelho 18,5 cm. O texto bruto do PDF apresenta “185” pelo meio centímetro sobrescrito; a leitura visual confirmou 18,5 cm, não 185 cm. A altura total 3,03 m não é múltipla dessa medida: o primeiro desnível 1,48 m corresponderia a oito espelhos, enquanto o segundo 1,55 m não fecha em quantidade inteira igual. Trata-se de incompatibilidade entre cotas e medida anotada; não se afirma execução física defeituosa ou medição de obra.

Prepararam-se duas alternativas geométricas, sem alterar o PDF, RVT, DWG, PRJ ou monografia. A alternativa A tem 17 espelhos uniformes de 17,823529… cm, oito no primeiro lance e nove no segundo, patamar acabado +1,645882… m. A alternativa B tem 18 de 16,833333… cm e patamar +1,735 m. Os valores exatos servem ao estudo; não são tolerâncias executivas. As projeções de 1,96/2,24 m na A usam a convenção de sete/oito pisadas a 28 cm, com patamar/piso como última subida. Ainda não se verificou se essa convenção coincide com cada extremidade física da arquitetura.

**O usuário autorizou estudar a alternativa A nesta sessão.** A geometria ainda precisa de conferência em planta e corte, largura útil, altura livre, vínculos e acabamentos. A autorização de estudo não equivale à aprovação estrutural nem à atualização já executada dos aplicativos.

## Cargas e modelagem

No exemplar local da ABNT NBR 6120:2019 consultaram-se a Tabela 10 (página PDF 27, impressa 21), a nota t (PDF 32), o item 6.3 (PDF 33) e a Tabela 12 (PDF 34). Para escada residencial dentro da unidade autônoma, a referência de carga variável distribuída é 2,5 kN/m². A nota t distingue o caso de carga concentrada de 2,5 kN para degrau isolado, verificado separadamente da carga variável distribuída, e a alternância em trechos em balanço quando aplicável. Para a barreira privativa a referência horizontal é 1,0 kN/m, perpendicular ao eixo da barreira e a 1,10 m do piso acabado. Não se aplicaram esses casos nem se fixou redução ou simultaneidade automática. A categoria residencial não dispensa peso próprio, guarda-corpo e ligações.

A documentação da AltoQi orienta usar nível intermediário para patamar fora dos pavimentos principais e contorno apropriado. O exemplo autoportante exige continuidade efetiva entre lances e patamar; simples contorno por barras não cria apoio por si. A escolha autoportante é alternativa a avaliar, não solução já dimensionada: https://suporte.altoqi.com.br/hc/pt-br/articles/115002281074 e https://suporte.altoqi.com.br/hc/pt-br/articles/115003584493 .

O plano acabado +1,646 m não deve ser copiado diretamente como plano estrutural. O N0 analítico está em +0,20 m e N1 em +3,20 m; os acabamentos da arquitetura são +0,22/+3,25 m. A espessura de acabamento do patamar e a referência geométrica da laje inclinada precisam ser compatibilizadas. Não se usou esse descompasso para recalcular espelhos silenciosamente. L5 continua sendo faixa horizontal do hall, não o conjunto dos lances e do patamar intermediário.

## Evidências e limites

A figura própria apresenta esquemas desdobrados, sem escala em planta. Os recortes originais e páginas normativas ficam em D:/TCC/work/r144-escada, fora do repositório público; o JSON referencia as fontes por SHA-256. Nenhum peso ou reação foi inventado para completar a lista de cargas. A espessura resistente e os apoios permanecem pendentes. O intervalo do script cobre apenas extração, cálculo e geração do esquema; não é tempo do fluxo CAD/BIM ou esforço total da IA.
