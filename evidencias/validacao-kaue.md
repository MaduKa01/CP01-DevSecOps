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
| Docker Engine acessível | Pendente |
| WSL 2 pronto para iniciar containers | Pendente |

A máquina ainda não tinha Docker Desktop nem WSL. Esses itens são pré-requisitos
declarados pelo `LAB.md`, portanto o tempo de instalação não entra na medição dos
12 minutos. O Windows solicitou reinicialização após habilitar o WSL. Como havia
uma chamada em andamento, a reinicialização foi adiada.

Antes da reinicialização, o Compose conseguiu validar a sintaxe do projeto, mas o
Docker Engine ainda não estava em execução. O `wsl --status` também informou que a
Plataforma da Máquina Virtual/virtualização precisava ser ativada. Esse ponto será
reavaliado depois da reinicialização antes de concluir se é necessário ajuste no
firmware.

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

## Próximas etapas

1. Reiniciar o Windows quando a chamada terminar.
2. Confirmar WSL, Docker Client e Docker Server com `docker version`.
3. Executar a preparação descrita na seção 0 de `LAB.md`.
4. Iniciar o cronômetro somente depois dos downloads.
5. Executar os estados vulnerável e corrigido e gerar o comprovante.
6. Registrar tempos, divergências e respostas às duas perguntas do laboratório.
7. Repetir o fluxo após qualquer correção de documentação.

