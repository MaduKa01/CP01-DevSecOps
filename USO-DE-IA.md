# Uso de IA generativa

Atualizado em 28/09/2026.

Ferramenta utilizada: Codex, com supervisão humana. A assistência de IA na elaboração do projeto e nas execuções iniciais é distinguida abaixo das validações realizadas pelos integrantes.

## Material assistido por IA

- Leitura e organização dos requisitos do PDF fornecido pelo professor.
- Plano do grupo e proposta de divisão das atividades.
- Desenvolvimento da aplicação didática, dos cenários vulnerável e corrigido, das configurações Docker, dos scripts auxiliares e do pipeline.
- Pesquisa em documentação oficial e interpretação dos resultados.
- Elaboração e revisão de documentação, roteiros de apresentação e diagrama de arquitetura.
- Apoio à preparação dos ambientes, à identificação de problemas e à correção de testes.
- Conferência dos relatórios da execução manual de 28/09/2026 e redação desta atualização da declaração de uso de IA.

## Execuções iniciais com assistência de IA — 25/09/2026

Foram registradas execuções assistidas por Codex, sob supervisão de Ronaldo:

- Trivy e KICS nos cenários vulnerável e corrigido, com reprovação e aprovação do gate conforme a política HIGH/CRITICAL.
- Nuclei nos dois alvos locais, com uma e zero correspondências no template utilizado.
- SonarQube, incluindo análise do código e reanálise após a substituição de MD5 por SHA-256.
- GitHub Actions em runner Linux, com cenário corrigido aprovado e vulnerável bloqueado, e conferência dos artefatos.
- Testes auxiliares de falha operacional e de prevenção do uso indevido de relatórios antigos pelo executor, além de verificações benignas dos endpoints.
- Conferência de que as credenciais locais do `.env` não constavam nos arquivos publicados.

Esses registros não constituem, por si só, prova de execução manual posterior nem de ensaio completo da apresentação. Os testes do executor também não devem ser confundidos com a execução de um teste negativo específico da janela de duas horas do comprovante.

## Validação em outra máquina — Cauê

A validação do laboratório por Cauê foi concluída em uma máquina Windows, com assistência de Codex e sua supervisão/autorização, conforme os registros em `evidencias/validacao-kaue.md` e `evidencias/comprovante-kaue.json`.

Foram executados os cenários vulnerável e corrigido com Trivy e KICS, gerado o comprovante e verificada a automação complementar. A validação também identificou uma incompatibilidade de um teste auxiliar com Windows, corrigida com simulação dos comandos por `unittest.mock`.

Portanto, a validação por Cauê não deve mais ser indicada como pendente. Trata-se de reprodução em outra máquina com assistência declarada, não de uma execução sem qualquer apoio de IA.

## Execução manual por RONALDO ATTAMAH — 28/09/2026

RONALDO ATTAMAH executou pessoalmente os comandos do laboratório principal descritos no `LAB.md`, em uma nova cópia do repositório no Mac. A sequência apresentada não utilizou `scripts/run_scan.py` para orquestrar os scanners, nem foi executada pelo Codex.

Foram realizados:

1. Clonagem do repositório, conferência do Docker e do Docker Compose e validação da configuração.
2. Download das imagens de Trivy, KICS e do serviço `verify`, além da base de vulnerabilidades do Trivy.
3. Conferência das versões das ferramentas.
4. Execução direta do Trivy e leitura do relatório do cenário vulnerável.
5. Execução direta do KICS no manifesto vulnerável.
6. Execução direta do Trivy e do KICS nos arquivos do cenário corrigido já fornecidos pelo projeto, incluindo a verificação HIGH/CRITICAL do Trivy.
7. Geração do comprovante com `docker compose run --rm verify python scripts/comprovante.py`.

“Execução manual” significa que Ronaldo acionou os comandos diretamente no terminal, seguindo o roteiro. O Docker Compose, as ferramentas e o script de comprovante continuam sendo componentes do projeto previamente elaborado com assistência de IA. A execução manual não altera essa declaração de origem.

### Ambiente observado

- macOS em arquitetura ARM64.
- Docker Desktop 4.63.0.
- Docker Engine/CLI 29.2.1.
- Docker Compose 5.0.2.
- Trivy 0.74.0.
- KICS 2.1.20.
- Base Trivy atualizada em `2026-09-28T13:05:44.359328237Z` e baixada em `2026-09-28T19:57:55.673470678Z`.

### Resultados da execução manual

| Verificação | Cenário vulnerável | Cenário corrigido |
|---|---|---|
| Trivy | 3 MEDIUM em Jinja2 3.1.4 | 0 vulnerabilidades nas dependências declaradas, com Jinja2 3.1.6 |
| KICS | 2 HIGH, 1 MEDIUM e 6 LOW | 0 HIGH/CRITICAL, 1 MEDIUM e 5 LOW |
| Comprovante | Relatórios dos dois cenários consolidados com sucesso | Relatórios dos dois cenários consolidados com sucesso |

Os três achados do Trivy foram `CVE-2024-56201`, `CVE-2024-56326` e `CVE-2025-27516`. Para esta última, o relatório indicou Jinja2 3.1.6 como versão de correção.

Os dois HIGH do KICS foram `Container Is Privileged` e `Privilege Escalation Allowed`. No cenário corrigido, as propriedades correspondentes são `privileged: false` e `allowPrivilegeEscalation: false`. A alteração adicional de `readOnlyRootFilesystem` para `true` removeu um achado LOW.

Os relatórios KICS registraram um arquivo analisado e interpretado em cada cenário, sem falhas de análise de arquivos ou de execução de consultas. Os JSON, os SARIF do KICS e o comprovante foram conferidos e apresentaram resultados consistentes entre si.

### Identificadores da execução

Horários em UTC, conforme os relatórios:

| Registro | Horário |
|---|---|
| Trivy vulnerável | `2026-09-28T20:02:05.070654835Z` |
| KICS vulnerável | `2026-09-28T20:02:28.267065971Z` |
| Trivy corrigido | `2026-09-28T20:05:05.423922127Z` |
| KICS corrigido | `2026-09-28T20:05:06.738325961Z` |

Esses horários correspondem aproximadamente a 17h02 e 17h05 no horário de São Paulo (UTC−3).

Evidências geradas localmente nesta execução:

- `reports/trivy/vulneravel/results.json` e `reports/trivy/corrigido/results.json`.
- `reports/kics/vulneravel/results.json` e `reports/kics/corrigido/results.json`.
- Arquivos `results.sarif` nas duas pastas do KICS.
- `reports/comprovante.json`.
- Saída do terminal preservada por Ronaldo.

Esses arquivos devem ser identificados pela data de geração. Na conferência desta execução, os resumos em `reports/gate/` ainda correspondiam às execuções de 25/09/2026; eles não são evidência de um novo acionamento do executor em 28/09/2026. Os relatórios Trivy em SARIF/SBOM também não foram regenerados pelos comandos manuais apresentados.

### Respostas às perguntas do laboratório

1. O `trivy_created_at` do cenário vulnerável foi `2026-09-28T20:02:05.070654835Z`. A versão indicada para corrigir `CVE-2025-27516` foi Jinja2 3.1.6.
2. O `kics_started_at` do cenário corrigido foi `2026-09-28T20:05:06.738325961Z`. Restaram zero HIGH. As duas propriedades que removeram os HIGH foram `privileged: false` e `allowPrivilegeEscalation: false`.

## Escopo e responsabilidade sobre as evidências

A execução manual de 28/09/2026 comprova a reprodução das etapas técnicas do laboratório principal Trivy/KICS até a geração do comprovante. Ela não é apresentada como nova execução de SonarQube, Nuclei ou GitHub Actions, nem como prova de edição manual das correções durante essa sessão.

Os resultados médios do Trivy não são bloqueantes pela política HIGH/CRITICAL adotada. Os dois HIGH do KICS são os achados bloqueantes do cenário vulnerável. O cenário corrigido atende a essa política, mas mantém os achados MEDIUM e LOW registrados pelo KICS. Zero vulnerabilidades no Trivy refere-se às dependências declaradas e à base utilizada, não à segurança integral da aplicação.

A evidência apresentada não mede um ensaio completo com explicação dos resultados. A revisão editorial por Edmar, a conferência dos slides por PEDRO GONÇALVES, a gravação e o ensaio do grupo devem ter seu estado registrado pelos respectivos responsáveis; esta atualização não presume sua conclusão nem os declara pendentes apenas por ausência de informação nova.

As contribuições humanas e a assistência de IA devem ser descritas conforme os registros disponíveis. Rascunhos, previsões e arquivos históricos não substituem evidências de novas execuções.
