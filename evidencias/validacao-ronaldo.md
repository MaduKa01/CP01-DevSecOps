# Validação pessoal — Ronaldo Attamah

Data: 26/09/2026 (São Paulo). Branch: `feat/validacao-ronaldo`.
Base inicial: `76fbf5353bfa160db6b9f925d9359fd5acf36ed5`, após o PR #1 de Cauê.

Ronaldo executou os comandos no próprio terminal e forneceu a transcrição. Codex ajudou no roteiro, diagnóstico do Nuclei, conferência dos relatórios e preparação dos documentos/commit. Isso não substitui revisão e ensaio pelos integrantes.

## Ambiente observado

macOS 26.5.2 (25F84), ARM64; Git 2.50.1 (Apple Git-155); Python 3.14.7; Docker Desktop 4.63.0 (220185); Engine/CLI 29.2.1; Compose 5.0.2. Configuração Compose validada. Trivy 0.74.0; KICS 2.1.20. Base Trivy atualizada em 25/09/2026 às 13:09:04 UTC, já baixada às 17:17:23 UTC. Havia cache prévio.

## Execução e resultados

1. Conferiu branch, commit, ambiente e configuração.
2. Preparou imagens Trivy/KICS/verify e banco do Trivy fora do cronômetro. O pull mostrou 4,5 s com imagens já disponíveis; não tratar como instalação do zero.
3. Executou versões e scans manuais, comparou correções e gerou comprovante.
4. Executou os dois cenários pelo executor e validou os relatórios.
5. Executou os dois testes de segurança do gate: 2/2 aprovados.
6. Executou Nuclei nos dois alvos e reanalisou o código com SonarQube.

| Verificação | Resultado |
|---|---|
| Trivy vulnerável | 3 MEDIUM em Jinja2 3.1.4 |
| Trivy corrigido | 0 vulnerabilidades nas dependências declaradas |
| KICS vulnerável | 2 HIGH, 1 MEDIUM, 6 LOW; código 50 |
| KICS corrigido | 0 HIGH/CRITICAL, 1 MEDIUM, 5 LOW; código 0 |
| Executor vulnerável | FAIL, 2 bloqueantes, código 1, errors vazio |
| Executor corrigido | PASS, 0 bloqueantes, código 0, errors vazio |
| Verificadores | Ambos os estados aprovados |
| Testes unitários | 2/2 aprovados; ERROR impresso dentro do cenário negativo é intencional |
| Nuclei | 1 correspondência vulnerável; 0 corrigido; validações OK |
| SonarQube | 1 issue aberta, 1 encerrada, 0 hotspots; scanner 0; processamento SUCCESS |

## Comprovante e respostas

Arquivo: `evidencias/comprovante-ronaldo.json`.

1. Trivy vulnerável criado em `2026-09-26T03:37:17.533430137Z`; correção da CVE-2025-27516: Jinja2 3.1.6.
2. KICS corrigido iniciado em `2026-09-26T03:39:01.604437588Z`; zero HIGH; propriedades alteradas: `privileged: false` e `allowPrivilegeEscalation: false`.

A automação posterior renovou os relatórios em `reports/`, portanto seus timestamps são posteriores aos do comprovante manual. Ambos representam execuções efetivas com as mesmas contagens. A transcrição da execução manual e complementar está em `evidencias/execucao-ronaldo.txt`; o nome do computador foi anonimizado e espaços finais removidos, sem reescrever resultados.

## Tempos e limites de comparação

- Fluxo pessoal registrado: 1.136 segundos (18min56s), incluindo intervalos. Início às 03:20:52 UTC; primeiro scan às 03:37:17 UTC. Não é ensaio contínuo do LAB de 12 minutos.
- Executor vulnerável: soma das etapas 3,144 s; corrigido: 2,539 s. Dados dos dois `reports/gate/*/summary.json`; não incluem downloads nem explicação humana.
- Nuclei original: 180,892 s vulnerável e 180,781 s corrigido, majoritariamente antes das requisições. A execução original foi preservada nos relatórios.
- SonarQube: 15,907 s, sem download e subida inicial do servidor, com histórico e caches existentes.

Não comparar esses números como benchmark Mac versus Windows.

## Dificuldades, assistência e correções

O Nuclei demorava na inicialização na rede isolada. Codex conferiu a documentação, testou `DISABLE_NUCLEI_TEMPLATES_PUBLIC_DOWNLOAD=true` e aplicou a variável ao Compose. Os dois testes diagnósticos sem sobrescrever os relatórios pessoais terminaram em menos de um segundo cada, com os resultados esperados. Também foram adicionadas mensagens de início e duração ao script. A transcrição pessoal fornecida ainda corresponde à execução anterior ao ajuste; não declaramos repetição pessoal após ele.

O `git diff --check` apontou espaços finais nos logs produzidos pelo Docker. Na preparação desta entrega foram removidos apenas os espaços de fim de linha dos logs modificados, mantendo mensagens e resultados. Essa é limpeza editorial de evidências, não mudança na política dos scanners.

## Pendências reais

Ensaio humano em 12 minutos; gravação do plano B; PDF acadêmico final; PPTX e PDF da apresentação; revisão dos materiais e participação individual nos outros laboratórios. O guia de documentação e o roteiro de 28 slides são bases para Edmar e Pedro, não conclusão das entregas deles.
