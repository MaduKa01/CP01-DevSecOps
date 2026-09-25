# Laboratório — Grupo 2: Trivy + KICS

**Objetivo:** identificar vulnerabilidades de dependências e configurações inseguras,
comparar correções e entender um gate HIGH/CRITICAL. Duração planejada: 12 minutos,
com downloads feitos antecipadamente. Não é necessário executar a aplicação para SCA/IaC.

## 0. Preparação antes da aula

Pré-requisitos: Git, Docker em execução, Docker Compose e internet durante os downloads.
No Windows, usar o terminal com Docker Desktop/WSL2 configurado. Os comandos Docker abaixo
funcionam sem Bash, Make ou Python instalado no host. Não usar o notebook da empresa sem autorização.

```sh
git clone https://github.com/MaduKa01/CP01-DevSecOps.git
cd CP01-DevSecOps
docker version
docker compose version
docker compose config --quiet
docker compose pull trivy kics verify
docker compose run --rm trivy image --download-db-only
```

**Esperado:** Client e Server no Docker; Compose disponível; configuração sem erros;
imagens baixadas e base de vulnerabilidades preparada. Não apagar o volume de cache antes da aula.

As imagens são fixadas por digest. A base do Trivy recebe atualizações: as contagens abaixo
são as observadas em 25/09/2026. Se a base disponível na preparação mudar, registrar a diferença.
Durante a aula usamos `--skip-db-update --offline-scan` para aproveitar a base já baixada.

## 1. Verificar as versões — 1 minuto

```sh
docker compose run --rm trivy --version
docker compose run --rm kics version
```

**Esperado:** Trivy 0.74.0 e KICS 2.1.20. A turma analisa somente os arquivos em `fixtures/`.
Não é preciso instalar Kubernetes nem executar `kubectl apply`.

## 2. Encontrar a dependência vulnerável com Trivy — 3 minutos

```sh
docker compose run --rm trivy fs --skip-db-update --offline-scan --scanners vuln --format json --output /reports/trivy/vulneravel/results.json /workspace/vulneravel/requirements.txt
docker compose run --rm trivy convert /reports/trivy/vulneravel/results.json
```

**Esperado:** três achados MEDIUM em Jinja2 3.1.4:

| CVE | Versão de correção indicada |
|---|---|
| CVE-2024-56201 | 3.1.5 |
| CVE-2024-56326 | 3.1.5 |
| CVE-2025-27516 | 3.1.6 |

O Trivy identifica a versão afetada a partir do arquivo de dependências. Não demonstra sozinho
exploração ou alcançabilidade no código. A classificação vem da fonte selecionada automaticamente,
GHSA neste resultado; não foi alterada para produzir uma cor específica no pipeline.

Pode aparecer aviso sobre ausência de `site-packages` e detecção de licenças: este comando
analisa vulnerabilidades do arquivo de dependências; não equivale a uma análise completa de licenças.

## 3. Encontrar configuração insegura com KICS — 3 minutos

```sh
docker compose run --rm kics scan -p /workspace/vulneravel/deployment.yaml --type Kubernetes --report-formats json,sarif --output-path /reports/kics/vulneravel --fail-on high,critical --no-progress --no-color
```

**Esperado:** 2 HIGH, 1 MEDIUM e 6 LOW. O processo termina com **código 50**, esperado porque
o KICS encontrou severidades bloqueantes. Não é erro de instalação.

Os dois HIGH são:

- `Container Is Privileged`: `privileged: true`.
- `Privilege Escalation Allowed`: `allowPrivilegeEscalation: true`.

O KICS analisa o manifesto estático. Esses privilégios **não são concedidos aos containers
do Compose**: o arquivo é uma fixture didática e não foi implantado.

## 4. Comparar as correções — 3 minutos

Abrir lado a lado os arquivos em `fixtures/vulneravel/` e `fixtures/corrigido/`.
O estado corrigido usa Jinja2 3.1.6 e define `privileged: false`,
`allowPrivilegeEscalation: false` e `readOnlyRootFilesystem: true`.

```sh
docker compose run --rm trivy fs --skip-db-update --offline-scan --scanners vuln --format json --output /reports/trivy/corrigido/results.json /workspace/corrigido/requirements.txt
docker compose run --rm trivy convert --severity HIGH,CRITICAL --exit-code 1 /reports/trivy/corrigido/results.json
docker compose run --rm kics scan -p /workspace/corrigido/deployment.yaml --type Kubernetes --report-formats json,sarif --output-path /reports/kics/corrigido --fail-on high,critical --no-progress --no-color
```

**Esperado:** Trivy sem vulnerabilidades nas dependências declaradas; KICS sem HIGH/CRITICAL,
mas ainda com 1 MEDIUM e 5 LOW. Os dois gates terminam com código 0.
O gate aceita esse resultado porque sua política bloqueia HIGH/CRITICAL. Os avisos restantes
continuam no relatório para discussão; não foram suprimidos.

O apresentador abre as execuções reais registradas em [pipeline.md](evidencias/pipeline.md):
uma falha no cenário vulnerável e outra aprovada no corrigido. Não é necessário esperar
uma nova execução do GitHub durante os 12 minutos.

## 5. Comprovante e perguntas — 2 minutos

Gerar um comprovante com os horários e resultados da própria execução:

```sh
docker compose run --rm verify python scripts/comprovante.py
```

**Esperado:** resumo dos dois estados, horários de execução e arquivo `reports/comprovante.json`.
O verificador rejeita relatórios com mais de duas horas, para não usar os exemplos já versionados
como se fossem uma execução nova. Salvar uma captura do terminal com esse resumo.
Cada aluno entrega o print e responde:

1. **Qual é o `trivy_created_at` da sua execução vulnerável e qual versão aparece como correção de CVE-2025-27516?**
2. **Qual é o `kics_started_at` da sua execução corrigida, quantos HIGH restaram e quais duas propriedades foram alteradas para remover os HIGH do cenário vulnerável?**

Responder com base na execução feita na própria máquina. Se os resultados divergirem,
anexar a saída e informar a data da base do Trivy.

## Limpeza

Os comandos `run --rm` removem os containers de análise após a execução. Os relatórios
ficam na pasta `reports/` e o cache permanece no volume exclusivo do projeto.
Quem executou os serviços opcionais pode pará-los com:

```sh
docker compose --profile demo --profile sonar down
```

Não usar limpeza global do Docker: outros projetos podem estar em execução.

## Solução de problemas

| Sintoma | Ação |
|---|---|
| Docker não conecta | Abrir Docker Desktop e conferir a seção Server em `docker version` |
| Base Trivy ausente | Repetir `docker compose run --rm trivy image --download-db-only` com internet |
| Download lento | Fazer a preparação antes da aula; não incluir download no tempo de análise |
| KICS retorna 50 no vulnerável | Resultado esperado: ler os dois HIGH |
| KICS falha por outro motivo | Conferir mensagem e relatório; não considerar falha operacional como evidência de vulnerabilidade |
| Resultado corrigido ficou diferente | Guardar a saída e revisar versão/data do banco; não esconder achados novos |
| Permissão ao gravar relatórios no Linux | Conferir propriedade da pasta clonada; não executar o projeto inteiro como root no host |
| `no matching manifest` | Conferir imagem/digest e arquitetura; as imagens do lab principal foram selecionadas com ARM64 e AMD64 |

## Para o grupo: preparação ampliada

SonarQube e Nuclei são demonstrados com as evidências de `reports/`; sua instalação não
faz parte dos pré-requisitos dos colegas para este lab. Comandos complementares estão no README.

O vídeo deve mostrar a execução completa, leitura dos achados, correções e CI vermelho/verde
em 5–8 minutos. A validação por Cauê em outra máquina e a gravação ainda devem ser realizadas.

Fontes dos comandos e formatos: [Trivy CLI](https://www.trivy.dev/docs/latest/guide/references/configuration/cli/trivy_filesystem/),
[Trivy convert](https://trivy.dev/docs/latest/references/configuration/cli/trivy_convert/),
[KICS CLI](https://docs.kics.io/latest/commands/). A composição e os exemplos são próprios do grupo, com assistência declarada em USO-DE-IA.md.
