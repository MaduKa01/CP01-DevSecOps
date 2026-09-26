# Validação pessoal de Ronaldo — Mac

**Status:** execução pessoal concluída em 26/09/2026; resultados em `evidencias/validacao-ronaldo.md`. Roteiro preservado como referência dos passos; repetição pessoal após o ajuste Nuclei e ensaio humano continuam separados.
**Branch:** `feat/validacao-ronaldo`.
**Base:** `76fbf5353bfa160db6b9f925d9359fd5acf36ed5`, após merge do PR #1 do Cauê.

Objetivo: Ronaldo executar os passos, compreender os resultados e registrar sua experiência.
As execuções anteriores feitas com Codex no Mac não substituem esta etapa pessoal.
O roteiro principal deve ser comparado ao Windows; Nuclei e SonarQube são um complemento separado.

## 1. Abrir a pasta certa e registrar o ambiente

Usar a janela **CP01-DevSecOps** do VS Code. A branch já foi criada localmente; não é preciso criá-la outra vez.
No terminal dessa janela:

```sh
cd /Users/ronaldoattamah/Documents/Codex/2026-09-25/files-mentioned-by-the-user-check/CP01-DevSecOps
git branch --show-current
git rev-parse HEAD
git status --short
sw_vers
uname -m
git --version
python3 --version
docker version
docker compose version
docker compose config --quiet
```

Esperado: branch `feat/validacao-ronaldo`, base indicada acima, Docker com Client e Server,
Compose validado sem mensagem de erro. Os dois arquivos de orientação recém-criados podem aparecer como novos no Git.
Se o Docker não responder, abrir Docker Desktop e aguardar a inicialização antes de continuar.

Registrar as versões efetivamente exibidas. Não copiar as versões do Windows ou de uma execução anterior.

## 2. Preparar imagens e base — fora do cronômetro do laboratório

```sh
docker compose pull trivy kics verify
docker compose run --rm trivy image --download-db-only
```

Como as imagens já foram usadas neste Mac, elas podem estar em cache. Registrar essa condição:
o tempo de preparação não será diretamente comparável ao primeiro download no Windows.

## 3. Iniciar o registro da sessão

Opcional, recomendado para guardar comandos e saídas no macOS:

```sh
mkdir -p work
script -q work/validacao-ronaldo-terminal.log
```

Esse comando inicia uma sessão de terminal gravada em arquivo local ignorado pelo Git.
Executar nela somente os passos do laboratório. Não abrir `.env` ou exibir credenciais durante o registro.

Iniciar o cronômetro do fluxo pessoal:

```sh
VALIDACAO_INICIO=$(date +%s)
date -u
docker compose run --rm trivy --version
docker compose run --rm kics version
```

O tempo pessoal inclui leitura e interpretação. Se parar para conversar ou resolver um problema,
anotar a pausa; não comparar esse total diretamente com os 118,404 segundos de execução automatizada do Cauê.

## 4. Trivy — dependências vulneráveis

```sh
docker compose run --rm trivy fs --skip-db-update --offline-scan --scanners vuln --format json --output /reports/trivy/vulneravel/results.json /workspace/vulneravel/requirements.txt
docker compose run --rm trivy convert /reports/trivy/vulneravel/results.json
```

Esperado na base usada anteriormente: três MEDIUM em Jinja2 3.1.4. Localizar CVE-2025-27516
e a correção 3.1.6. Explicar em voz alta: “SCA identifica vulnerabilidades conhecidas nas dependências”.

Guardar um print do resumo. Se a base atual produzir números diferentes, registrar e investigar;
não alterar a política para reproduzir artificialmente as contagens anteriores.

## 5. KICS — manifesto vulnerável

```sh
docker compose run --rm kics scan -p /workspace/vulneravel/deployment.yaml --type Kubernetes --report-formats json,sarif --output-path /reports/kics/vulneravel --fail-on high,critical --no-progress --no-color
printf 'Saída do KICS: %s\n' "$?"
```

Esperado: 2 HIGH, 1 MEDIUM, 6 LOW; código **50**. Executar o `printf` imediatamente após
o scanner para preservar o código de saída correto. Explicar as duas configurações:
`privileged: true` e `allowPrivilegeEscalation: true`. O manifesto é somente analisado, não implantado.

## 6. Cenário corrigido

```sh
docker compose run --rm trivy fs --skip-db-update --offline-scan --scanners vuln --format json --output /reports/trivy/corrigido/results.json /workspace/corrigido/requirements.txt
docker compose run --rm trivy convert --severity HIGH,CRITICAL --exit-code 1 /reports/trivy/corrigido/results.json
printf 'Saída do gate Trivy: %s\n' "$?"
docker compose run --rm kics scan -p /workspace/corrigido/deployment.yaml --type Kubernetes --report-formats json,sarif --output-path /reports/kics/corrigido --fail-on high,critical --no-progress --no-color
printf 'Saída do KICS: %s\n' "$?"
```

Esperado: Trivy sem achados no conjunto declarado; KICS com zero HIGH/CRITICAL,
um MEDIUM e cinco LOW. Saídas dos dois gates: **0**.
Explicar: “Verde significa atender à política HIGH/CRITICAL; os avisos menores continuam registrados”.

## 7. Comprovante e encerramento do cronômetro

```sh
docker compose run --rm verify python scripts/comprovante.py
printf 'Tempo do fluxo pessoal: %s segundos\n' "$(( $(date +%s) - VALIDACAO_INICIO ))"
cp reports/comprovante.json evidencias/comprovante-ronaldo.json
```

Guardar um print e responder às duas perguntas do LAB.md com os horários desta execução.
Se abriu a gravação com `script`, encerrá-la agora:

```sh
exit
```

Esse `exit` encerra a sessão gravada. Não é necessário fechar a janela do VS Code.
Não publicar o log completo antes de conferir seu conteúdo.

## 8. Automação e testes — medição separada

```sh
python3 scripts/run_scan.py vulneravel --offline
printf 'Saída do executor vulnerável: %s\n' "$?"
python3 scripts/run_scan.py corrigido --offline
printf 'Saída do executor corrigido: %s\n' "$?"
docker compose run --rm verify
python3 -m unittest scripts.test_gate -v
python3 scripts/verify_reports.py
git diff --check
```

Esperado: executor vulnerável **1**, corrigido **0**, verificador aprovado e **2/2 testes**.
Esta etapa regrava os relatórios em `reports/`. O comprovante pessoal da etapa anterior
já estará preservado em `evidencias/comprovante-ronaldo.json`.

## 9. Complemento: Nuclei e SonarQube

Fora do cronômetro de 12 minutos, para Ronaldo compreender também as outras ferramentas.

```sh
docker compose pull nuclei
docker compose --profile demo up -d --build --wait app-vulneravel app-corrigido
python3 scripts/run_dast.py
```

Esperado: uma correspondência Nuclei no vulnerável e zero no corrigido, com validação OK.
Apenas um template próprio e alvos locais participam dessa execução.

O Compose desativa o download automático de templates públicos do Nuclei. Isso evita
esperas de inicialização na rede isolada do laboratório. O script informa quando
começa cada cenário e exibe sua duração ao terminar. Não é necessário repetir o
download da imagem nem reconstruir os alvos para aplicar esse ajuste: basta executar
novamente `python3 scripts/run_dast.py` após o processo anterior terminar.

```sh
docker compose --profile sonar up -d sonarqube
python3 scripts/setup_sonar.py
python3 scripts/run_sonar.py
```

Se o setup avisar que o servidor ainda inicia, aguardar e repetir o setup. O estado atual usa SHA-256;
espera-se o aviso HTTP aberto. O MD5 corrigido é comprovado pelos relatórios históricos.
Não reintroduzir MD5 só para recriar o achado. Não confundir issues encerradas com abertas.

## 10. Registrar, comparar e abrir PR

Após a execução, criar `evidencias/validacao-ronaldo.md` com:

- data, branch, base, versões reais e condição dos caches;
- passos efetivamente executados e códigos de saída;
- contagens, horários do comprovante e prints relevantes;
- tempo do fluxo pessoal, pausas e tempo de ensaio explicado, quando houver;
- dificuldades e correções feitas, ou indicação de que não ocorreram;
- resultados complementares de Nuclei/SonarQube, se executados;
- quais etapas tiveram assistência do Codex.

Atualizar `docs/BASE-PARA-PESQUISA-E-SLIDES.md` somente com os resultados efetivamente obtidos.
Revisar o diff e selecionar os arquivos pertinentes; não usar um commit vazio para marcar participação.
O fluxo final será commit → push de `feat/validacao-ronaldo` → PR para `main` → CI → revisão por Cauê → merge.
Não fazer push direto na `main` para esta validação.

Ao receber as saídas de cada bloco, Codex pode ajudar a interpretá-las, registrar as evidências
e preparar o PR. A validação pessoal só será marcada como concluída depois da execução.
