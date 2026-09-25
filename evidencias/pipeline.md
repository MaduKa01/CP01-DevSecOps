# CI vermelho e verde — execuções reais

Ambas as execuções usam o commit `c736a606f384d0bd3d05a66aa7e200e8737642b7`,
as mesmas imagens fixadas e a mesma política HIGH/CRITICAL. A diferença é a fixture
selecionada: os arquivos antes/depois estão versionados no mesmo commit.
Essa comparação não pretende ser uma sequência de dois commits distintos de IaC.

| Cenário | Execução | Resultado comprovado |
|---|---|---|
| Corrigido | [Run 36167707788](https://github.com/MaduKa01/CP01-DevSecOps/actions/runs/36167707788) | SUCCESS; zero HIGH/CRITICAL; relatórios preservados |
| Vulnerável | [Run 36167909434](https://github.com/MaduKa01/CP01-DevSecOps/actions/runs/36167909434) | FAILURE no gate; dois HIGH do KICS; etapa de artifacts concluiu com sucesso |

Os resumos brutos estão em:

- `reports/ci/36167707788/gate/corrigido/summary.json`.
- `reports/ci/36167909434/gate/vulneravel/summary.json`.
- `evidencias/github-runs.json`: estado dos runs e de cada etapa, consultado via API.

A execução vermelha tem `status: FAIL`, `blocking_findings: 2`, `errors: []` e
`exit_code: 1` no executor. Portanto, a falha foi causada pela política de segurança,
não por indisponibilidade do scanner. O KICS retorna 50 para esses achados; o executor
converte a decisão combinada para 1. Erros operacionais produzem 2.

O Trivy encontrou apenas MEDIUM nesse exemplo. Eles continuam no relatório completo e
não bloqueiam essa política. O estado corrigido ainda tem avisos menores de IaC.
O verde não é uma declaração de que toda a aplicação ou infraestrutura está segura.

## Reprodução

1. Abrir Actions → Security gate → Run workflow.
2. Selecionar `main` e `vulneravel`: esperar falha na etapa do gate.
3. Repetir com `corrigido`: esperar sucesso.
4. Conferir os artifacts e o arquivo `gate/<cenario>/summary.json`.

O workflow também roda em pushes para `main` e pull requests, usando o estado corrigido.
Não há `continue-on-error`, supressões ou alteração de limiar para produzir verde.
Os artifacts têm retenção de 30 dias; suas evidências essenciais também foram versionadas no Git.

## SAST como evidência complementar

O commit `00a3726` contém o checksum MD5 identificado pelo SonarQube.
O commit `c736a60` troca-o por SHA-256, e a reanálise marca S4790 como FIXED.
SonarQube e Nuclei são evidências complementares, não etapas deste gate SCA/IaC.
