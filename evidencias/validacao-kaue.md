# Validação independente do laboratório — Kauê

Data de início: 25/09/2026  
Branch: `feat/validacao-lab`  
Base validada: `c0e56ee87477e375562182d47374256e0dbc8ee4`

## Objetivo

Executar o roteiro de `LAB.md` em uma segunda máquina, sem orientação adicional,
registrar dificuldades reais e conferir se a atividade prática cabe em 12 minutos
depois da preparação dos downloads.

## Ambiente de validação

- Windows 64-bit, build 26200.9457.
- Git 2.55.0.windows.3.
- Python 3.14.7.
- WSL 2.7.14, instalado durante a preparação.
- Docker Desktop 4.92.0, Docker CLI 29.8.0 e Docker Compose 5.5.1.
- Branch criada com autoria `kaue-code-3011 <kauelima000@icloud.com>`.

## Preflight realizado

| Verificação | Resultado |
|---|---|
| Repositório na base indicada por Ronaldo | OK |
| Árvore de trabalho limpa antes da validação | OK |
| Autoria Git de Kauê configurada | OK |
| `docker compose config --quiet` | OK, código 0 |
| Cliente Docker e plugin Compose instalados | OK |
| Docker Engine acessível | OK, Server 29.8.0 |
| WSL 2 pronto para iniciar containers | OK |

A máquina ainda não tinha Docker Desktop nem WSL. Esses itens são pré-requisitos
declarados pelo `LAB.md`, portanto o tempo de instalação não entra na medição dos
12 minutos. O Windows solicitou reinicialização após habilitar o WSL. Como havia
uma chamada em andamento, a reinicialização foi adiada e realizada depois.

Antes da reinicialização, o Compose conseguiu validar a sintaxe do projeto, mas o
Docker Engine ainda não estava em execução. O `wsl --status` também informou que a
Plataforma da Máquina Virtual/virtualização precisava ser ativada. Esse ponto será
reavaliado depois da reinicialização antes de concluir se é necessário ajuste no
firmware. Depois da reinicialização, o WSL 2 e a distribuição interna
`docker-desktop` iniciaram corretamente, sem necessidade de alteração no firmware.

## Execução real do LAB.md

A preparação ficou fora do cronômetro, conforme o roteiro:

- download das imagens Trivy, KICS e verify: 15,308 segundos;
- download da base do Trivy, com aproximadamente 117 MiB: 23,589 segundos;
- `docker compose config --quiet`: código 0.

O fluxo cronometrado, desde a conferência das versões até a geração do comprovante,
levou 1 minuto e 58,404 segundos. Esse é o tempo de execução automatizada e não
inclui o tempo de um apresentador explicar os achados. Mesmo assim, demonstra margem
operacional para o limite de 12 minutos.

Resultados observados nesta máquina:

| Etapa | Resultado |
|---|---|
| Trivy vulnerável | 3 MEDIUM em Jinja2 3.1.4 |
| Correção da CVE-2025-27516 | Jinja2 3.1.6 |
| KICS vulnerável | 2 HIGH, 1 MEDIUM e 6 LOW; código 50 esperado |
| Trivy corrigido | 0 vulnerabilidades nas dependências declaradas |
| KICS corrigido | 0 HIGH/CRITICAL, 1 MEDIUM e 5 LOW; código 0 |
| Comprovante | Gerado com código 0 |

Horários do comprovante:

- Trivy vulnerável: `2026-09-25T18:55:43.174267524Z`.
- KICS corrigido: `2026-09-25T18:56:24.27598912Z`.

Respostas às perguntas do laboratório:

1. O `trivy_created_at` vulnerável foi
   `2026-09-25T18:55:43.174267524Z`; a correção indicada para
   CVE-2025-27516 foi Jinja2 3.1.6.
2. O `kics_started_at` corrigido foi `2026-09-25T18:56:24.27598912Z`;
   restaram zero HIGH. As propriedades alteradas para remover os dois HIGH foram
   `privileged: false` e `allowPrivilegeEscalation: false`.

Como validação complementar fora do cronômetro, `scripts/run_scan.py` também foi
executado nos dois estados. O vulnerável retornou 1 por dois bloqueantes, o
corrigido retornou 0, e o container `verify` aprovou os dois relatórios. O fluxo
completo levou 25,535 segundos.

## Dificuldade encontrada e correção

O teste `scripts/test_gate.py` usava um arquivo executável fake no formato Unix
para simular o comando `docker`. Por isso, um dos dois testes falhava no Windows
com `FileNotFoundError`, embora passasse no runner Linux do GitHub Actions.

O teste foi alterado para carregar `run_scan.py` isoladamente e simular sua função
de execução com `unittest.mock`, sem depender de um executável específico do
sistema operacional. Depois da alteração:

- 2 de 2 testes do gate passaram no Windows;
- `scripts/verify_reports.py` validou os relatórios versionados;
- a sintaxe Python e `git diff --check` passaram.

Essa verificação dos relatórios existentes não substitui uma nova execução dos
scanners nesta máquina.

## Conclusão e próximas etapas

Depois da preparação correta do ambiente, os comandos e resultados do `LAB.md`
foram claros e reproduzíveis no Windows. Não foi necessária correção no roteiro
principal. A dificuldade concreta encontrada foi a portabilidade do teste auxiliar,
já corrigida nesta branch.

Ainda falta:

1. Fazer um ensaio humano com leitura e explicação dos resultados dentro de 12 minutos.
2. Gravar o plano B de 5–8 minutos seguindo `evidencias/plano-b.md`.
3. Registrar localização, duração e data da gravação.
4. Publicar a branch e abrir o Pull Request depois da revisão final.
