# DevSecOps — Plano de trabalho do grupo 2

**Integrantes:** Ronaldo, Cauê, Edmar e Pedro.  
**Responsável pela coordenação:** Ronaldo.  
**Repositório:** [MaduKa01/CP01-DevSecOps](https://github.com/MaduKa01/CP01-DevSecOps).  
**Apresentação:** segunda-feira, 28/09/2026, às 19h.  
**Meta interna:** concluir os commits e publicar a versão final até sábado, 26/09, às 19h.  
**Entrega dos arquivos:** domingo, 27/09, pelo canal indicado pelo professor.

## O que vamos entregar

- **Pesquisa:** PDF com 15–25 páginas de conteúdo, fonte 11 ou 12, espaçamento 1,5 e ABNT; mínimo de 10 fontes, sendo pelo menos 4 primárias.
- **Apresentação:** 20–30 slides, em PPTX e PDF, com duração máxima de 30 minutos. Nossa proposta é trabalhar com 26 slides.
- **Laboratório:** atividade de até 12 minutos para a turma executar Trivy e KICS, com ambiente Docker, roteiro e resultados esperados.
- **Repositório único:** código, configurações, README, LAB.md, documento, slides, relatórios e evidências.
- **Plano B:** vídeo de 5–8 minutos ou GIF da execução completa.

As quatro ferramentas do grupo são **SonarQube CE (SAST), Trivy (SCA), KICS (IaC) e Nuclei (DAST)**. Todas entram na pesquisa e na apresentação; Trivy e KICS formam a atividade conduzida com a turma.

## Onde cada um vai atuar

| Integrante | Responsabilidade principal | Entregas |
|---|---|---|
| **Ronaldo** | Coordenar a execução e integrar o projeto | Repositório, aplicação de demonstração, ambiente Docker, configuração das ferramentas e pipeline com bloqueio por severidade; revisão final das evidências |
| **Cauê** | Validar a execução e organizar o laboratório | Teste em outra máquina, revisão do LAB.md, conferência dos achados e tempos, duas perguntas de verificação e gravação do plano B; apoio aos testes das quatro ferramentas |
| **Edmar** | Organizar e redigir a documentação | Sumário, pesquisa das quatro ferramentas, referências, formatação ABNT, integração das evidências recebidas e PDF final; consolidação do USO-DE-IA.md com informações de todos |
| **Pedro** | Construir a apresentação e organizar o ensaio | PPTX e PDF, diagramas e quadro comparativo, inserção das evidências, roteiro de fala e controle do tempo; apoio à revisão visual da documentação |

Ronaldo e Cauê fornecem relatórios, imagens, comandos validados e explicações dos resultados. Edmar e Pedro usam esse material para concluir texto e slides. As dúvidas e inconsistências devem ser resolvidas antes da exportação final.

## Como avançar sem esperar a conclusão dos testes

**Edmar pode começar imediatamente** pelo sumário, fundamentos e pesquisa das quatro ferramentas. Para cada uma, cobrir: mantenedor, licença, origem e atividade; funcionamento; o que detecta e não detecta; instalação e comandos; regras e supressões; integração com CI/CD, IDE e pre-commit; SARIF, Code Scanning e DefectDojo; limitações e cenário de uso. Incluir também SAST versus SCA, posição no pipeline, shift-left e SBOM.

**Pedro pode começar imediatamente** pelo modelo visual e organização dos slides: abertura e conceitos; quatro ferramentas; laboratório; comparativo e limitações; conclusão e perguntas. Reservar espaços para os resultados reais, sem preencher contagens ou tempos ainda não medidos.

**Ronaldo inicia** a preparação do Docker, do repositório e dos exemplos vulnerável/corrigido. Em seguida, configura o pipeline e reúne as evidências das ferramentas.

**Cauê prepara** sua máquina para clonar o projeto e executar o roteiro de forma independente. Registra erros, passos ambíguos e duração; depois ajuda a revisar os três achados e grava o fluxo validado.

## Cronograma combinado

| Quando | Resultado esperado |
|---|---|
| **Sexta, 25/09** | Repositório e ambiente iniciados; primeiras execuções; sumário do documento e estrutura dos slides prontos |
| **Sábado, manhã** | Laboratório e pipeline validados; relatórios e três achados disponíveis para documento e slides |
| **Sábado, até 17h — meta de revisão** | Texto, slides, LAB.md e vídeo prontos para conferência conjunta |
| **Sábado, até 19h — fechamento** | Ajustes concluídos, contribuições de todos registradas, arquivos finais e repositório publicados |
| **Domingo, 27/09** | Entrega oficial, conferência de acesso aos arquivos e ensaio completo |
| **Segunda, 28/09, às 19h** | Apresentação e condução do laboratório |

O horário de sábado é nossa meta interna. O PDF pede publicação do repositório em D-2 e exige pelo menos 24 horas de antecedência para a turma preparar o ambiente.

## Divisão proposta da apresentação

Todos apresentam e ajudam a turma durante o laboratório. A distribuição será ajustada no ensaio para equilibrar as falas.

| Integrante | Parte a preparar |
|---|---|
| **Edmar** | Abertura, fundamentos e SonarQube |
| **Ronaldo** | Trivy e primeira parte do laboratório |
| **Cauê** | KICS e segunda parte do laboratório |
| **Pedro** | Nuclei, quadro comparativo, limitações e conclusão |

**Tempo total:** 3 minutos de abertura, 10 sobre as quatro ferramentas, 12 de laboratório, 3 de comparativo/conclusão e 2 de perguntas.

## Critérios que precisamos conferir juntos

- O laboratório funciona em outra máquina e cabe em 12 minutos, após a preparação antecipada.
- O pipeline falha com achados HIGH/CRITICAL e passa após correção real; há evidências das duas execuções.
- Três achados têm evidência, classificação de verdadeiro/falso positivo, justificativa, CWE e correção proposta.
- Os relatórios originais estão versionados; capturas de tela complementam esses arquivos.
- LAB.md tem pré-requisitos, comandos copiáveis, resultados esperados e duas perguntas de verificação.
- As quatro ferramentas estão cobertas; tempos, limitações e resultados apresentados foram verificados.
- Textos, imagens e comandos de terceiros têm fonte. O uso de IA está declarado em USO-DE-IA.md, com a validação realizada.
- Cada integrante registra suas próprias contribuições reais no repositório. Documento e slides também são contribuições.
- Todos conseguem explicar o conjunto do trabalho, pois o professor pode perguntar sobre qualquer parte.
- Varreduras ativas ficam restritas ao alvo autorizado em ambiente local isolado.

**Atenção aos pontos:** laboratório 35, pesquisa 25, apresentação 20, repositório 10 e participação individual 10. Há desconto por exceder o tempo, atrasar a entrega ou não publicar o repositório com antecedência.

**Responsabilidade individual adicional:** cada um precisa executar os laboratórios dos outros dois grupos e entregar o print final e as respostas às perguntas de verificação.

## Organização dos arquivos

- `docs/`: documento-fonte, referências e PDF final — Edmar.
- `slides/`: apresentação PPTX e PDF — Pedro.
- `reports/` e `evidencias/`: resultados e análises — Ronaldo e Cauê.
- `LAB.md` e plano B: roteiro, verificação e gravação — Cauê, com revisão de Ronaldo.
- `README.md`, aplicação, Docker e pipeline: integração do projeto — Ronaldo.

Ao concluir uma tarefa, informar ao grupo **o que foi entregue, onde está o arquivo e se existe alguma pendência**. Assim, texto, slides e laboratório permanecem consistentes até o fechamento.
