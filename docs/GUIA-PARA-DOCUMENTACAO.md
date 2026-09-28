# Guia para documentação e reprodução do projeto — Grupo 2

Responsável pelo documento: Edmar. Coordenação: Ronaldo. Validação independente: Cauê. Apresentação: Pedro.
Atualizado em 26/09/2026. Este é o material de apoio para escrever a pesquisa e reproduzir o projeto desde o início; o PDF acadêmico final ainda precisa ser produzido e revisado.

Repositório: https://github.com/MaduKa01/CP01-DevSecOps
Branch desta entrega: `feat/validacao-ronaldo`. Os caminhos citados abaixo são relativos à raiz do repositório.

## 1. O que estamos demonstrando

O projeto compara dois estados de uma aplicação didática e dos seus arquivos de configuração. No estado vulnerável há dependência desatualizada, permissões inseguras em um manifesto e exposição simulada de informações. No corrigido, os problemas escolhidos são removidos e as ferramentas são executadas novamente.

| Categoria | Ferramenta do grupo | Entrada analisada no projeto | Precisa da aplicação rodando? |
|---|---|---|---|
| SAST | SonarQube Community | Código próprio em `app/server.py` | Não; precisa do servidor de análise |
| SCA | Trivy | Versões em `requirements.txt` | Não |
| IaC | KICS | Arquivo Kubernetes `deployment.yaml` | Não |
| DAST | Nuclei | Endpoint `/debug` das aplicações locais | Sim |

SAST procura problemas no código que escrevemos. SCA identifica componentes de terceiros e vulnerabilidades conhecidas associadas às versões. IaC examina configurações declaradas antes da implantação. DAST observa respostas da aplicação em execução. As quatro categorias se complementam.

O laboratório conduzido com a turma usa **Trivy + KICS**, duas categorias diferentes, em até 12 minutos após os downloads. Nuclei e SonarQube são demonstrações complementares. O pipeline automatiza somente Trivy e KICS; não afirmar que os quatro scanners estão no GitHub Actions.

## 2. Requisitos do trabalho e destino no documento

Fonte: PDF do professor fornecido ao grupo, especialmente páginas 7–11 e 14–16. O nome do arquivo menciona CP02, mas o conteúdo se identifica como Check Point 01; manter a nomenclatura acordada com a disciplina.

- Pesquisa: PDF com 15–25 páginas de conteúdo, fonte 11 ou 12, espaçamento 1,5 e referências no padrão ABNT; pelo menos 10 fontes, quatro primárias.
- Para **cada ferramenta**: identificação; fundamento técnico; instalação/uso; integrações; avaliação crítica. A seção 11 deste guia detalha o que ainda pesquisar.
- Seções transversais: SAST versus SCA, pipeline, shift-left, SBOM e quadro comparativo.
- Prática: LAB.md reproduzível, duas categorias, gate HIGH/CRITICAL, vermelho e verde reais, três achados com CWE/triagem/correção, execução em outra máquina e plano B gravado de 5–8 minutos ou GIF completo.
- Apresentação: 20–30 slides, PPTX e PDF, até 30 minutos, todos com fala.
- Repositório único acessível ao professor/turma, relatórios versionados, contribuições reais distribuídas e declaração de IA.
- Participação individual: executar os laboratórios dos outros dois grupos e entregar comprovantes.

Apresentação informada: segunda-feira, 28/09/2026, às 19h. O PDF exige publicação pelo menos 24h antes e apresenta D-2 como marco de liberação. A meta interna é sábado, 26/09, às 19h; domingo, 27/09, às 19h é o limite de 24h. O PDF não afirma literalmente que qualquer commit posterior é proibido: exige disponibilidade antecipada do repositório e roteiro. Para evitar divergências, congelar a versão preparada para a turma e registrar correções necessárias com transparência. Penalidades declaradas: −2 pontos/minuto excedido, −5/dia de atraso e −10 por publicação sem antecedência mínima.

## 3. Preparar uma máquina do zero

### 3.1 Instalar as ferramentas

1. Instalar Git pelo [site oficial](https://git-scm.com/downloads). Abrir um terminal novo e conferir `git --version`.
2. Instalar Docker Desktop para [Mac](https://docs.docker.com/desktop/setup/install/mac-install/) ou [Windows](https://docs.docker.com/desktop/setup/install/windows-install/). No Mac, escolher Apple Silicon ou Intel conforme a máquina. No Windows, usar containers Linux e o backend WSL 2; concluir reinicializações solicitadas. Abrir Docker Desktop e esperar o motor iniciar.
3. No Windows, conferir `wsl --version` e `wsl --status`. Se WSL ainda não estiver instalado, seguir o instalador oficial; Cauê utilizou `wsl --install --no-distribution`, reiniciou e então validou o Docker. Essa instalação pode pedir privilégios administrativos.
4. Para os scripts complementares, instalar [Python](https://www.python.org/downloads/) 3.10 ou superior. O laboratório principal usa Python dentro do container e dispensa Python no computador da turma.
5. Reservar internet e espaço em disco para baixar imagens e a base de vulnerabilidades antes da aula. SonarQube acrescenta consumo de memória; seu container tem limite de 3 GB no Compose. A validação foi feita em Mac com 18 GB físicos. Isso é ambiente observado, não mínimo universal certificado.

Não instalar Jinja2 vulnerável no sistema da máquina. As dependências pertencem aos exemplos/containers. Não é necessário instalar Kubernetes, Java ou os scanners diretamente no computador.

### 3.2 Obter o projeto

Em uma pasta destinada ao trabalho, executar:

```sh
git clone https://github.com/MaduKa01/CP01-DevSecOps.git
cd CP01-DevSecOps
git switch feat/validacao-ronaldo
git branch --show-current
git rev-parse HEAD
docker version
docker compose version
docker compose config --quiet
```

Esperado: branch correta; identificador do commit; Docker com **Client e Server**; Compose disponível; última linha sem erro. O comando `config --quiet` valida a configuração, mas não prova que o motor Docker está ativo. Se já houver um clone com trabalho local, não clonar por cima nem descartar alterações; atualizar esse clone com orientação do grupo. Após o merge, a turma poderá usar `main`, conferindo o commit publicado.

Opcional: abrir essa pasta em uma nova janela do editor. Todos os comandos seguintes devem ser executados na pasta `CP01-DevSecOps`.

### 3.3 Entender os arquivos antes de executar

| Local | Função |
|---|---|
| `docker-compose.yml` | Define imagens, redes, volumes e serviços; versões e digests fixados |
| `app/server.py` e `app/Dockerfile` | Aplicação Python e construção das duas imagens |
| `fixtures/vulneravel/` e `fixtures/corrigido/` | Dependências e manifesto antes/depois |
| `nuclei/debug-exposure.yaml` | Teste HTTP próprio com marcadores específicos |
| `scripts/` | Execução, verificação e geração de comprovantes |
| `.github/workflows/security.yml` | Gate no GitHub Actions |
| `reports/` | Relatórios reais: JSON, SARIF, logs e SBOM conforme a ferramenta |
| `evidencias/` | Interpretação, comprovantes, problemas e execuções anteriores |
| `USO-DE-IA.md` | Como a assistência de IA foi utilizada e verificada |

Os alvos DAST ficam em rede Docker interna, sem portas publicadas. O painel SonarQube fica em `http://127.0.0.1:19000`. Os manifestos Kubernetes são arquivos de estudo: **não executar `kubectl apply`**. Não direcionar scanners ativos a terceiros.

### 3.4 Preparar os downloads, fora do cronômetro

```sh
docker compose pull trivy kics verify
docker compose run --rm trivy image --download-db-only
```

A primeira linha baixa os scanners e o verificador; a segunda prepara o banco do Trivy no volume `trivy-cache`. O volume evita novos downloads em cada execução. Imagens fixadas não congelam o banco de vulnerabilidades: registrar data do banco junto aos resultados.

## 4. Laboratório principal passo a passo

Os comandos Docker são iguais no Mac e no PowerShell. Para consultar imediatamente o código de saída, usar `echo $?` no Mac/Linux e `$LASTEXITCODE` no PowerShell. Não inserir outro comando antes dessa consulta.

### Passo 1 — Verificar versões

```sh
docker compose run --rm trivy --version
docker compose run --rm kics version
```

Esperado: Trivy 0.74.0 e KICS 2.1.20. Fotografar/capturar também a data da base do Trivy. `run --rm` cria um container temporário e o remove quando o comando termina.

### Passo 2 — Encontrar a dependência afetada

```sh
docker compose run --rm trivy fs --skip-db-update --offline-scan --scanners vuln --format json --output /reports/trivy/vulneravel/results.json /workspace/vulneravel/requirements.txt
docker compose run --rm trivy convert /reports/trivy/vulneravel/results.json
```

`fs` analisa arquivos; `--scanners vuln` seleciona vulnerabilidades; `--skip-db-update --offline-scan` reutiliza a base preparada; `--output` salva evidência. `/workspace` e `/reports` são caminhos internos montados pelo Compose; os arquivos aparecem nas pastas locais correspondentes. `convert` apresenta o JSON de forma legível.

Resultado observado: Jinja2 3.1.4 com três MEDIUM, CVE-2024-56201, CVE-2024-56326 e CVE-2025-27516. As duas primeiras indicam correção em 3.1.5; a última em 3.1.6. O estado corrigido utiliza 3.1.6. A detecção de versão afetada não é prova de exploração.

### Passo 3 — Encontrar os problemas do manifesto

```sh
docker compose run --rm kics scan -p /workspace/vulneravel/deployment.yaml --type Kubernetes --report-formats json,sarif --output-path /reports/kics/vulneravel --fail-on high,critical --no-progress --no-color
```

`-p` define o arquivo; `--type` seleciona a tecnologia; JSON e SARIF são formatos de saída; `--fail-on` aplica o limiar do gate.

Esperado: **2 HIGH, 1 MEDIUM e 6 LOW**, com código **50**. Isso é bloqueio de segurança esperado. Os HIGH são `Container Is Privileged` e `Privilege Escalation Allowed`. Eles pertencem ao arquivo de exemplo, não à configuração efetiva dos containers deste Compose.

### Passo 4 — Explicar e analisar a correção

Comparar os dois diretórios de fixtures no editor:

| Arquivo/propriedade | Vulnerável | Corrigido |
|---|---|---|
| `requirements.txt` | Jinja2 3.1.4 | Jinja2 3.1.6 |
| `privileged` | true | false |
| `allowPrivilegeEscalation` | true | false |
| `readOnlyRootFilesystem` | false | true |

```sh
docker compose run --rm trivy fs --skip-db-update --offline-scan --scanners vuln --format json --output /reports/trivy/corrigido/results.json /workspace/corrigido/requirements.txt
docker compose run --rm trivy convert --severity HIGH,CRITICAL --exit-code 1 /reports/trivy/corrigido/results.json
docker compose run --rm kics scan -p /workspace/corrigido/deployment.yaml --type Kubernetes --report-formats json,sarif --output-path /reports/kics/corrigido --fail-on high,critical --no-progress --no-color
```

Esperado: Trivy sem vulnerabilidades nas dependências declaradas; KICS com **0 HIGH/CRITICAL, 1 MEDIUM e 5 LOW**; gates com código 0. A correção de raiz gravável remove um LOW. Os demais avisos continuam visíveis; não foram suprimidos.

### Passo 5 — Gerar o comprovante pessoal

```sh
docker compose run --rm verify python scripts/comprovante.py
```

Esperado: resumo dos dois estados e `reports/comprovante.json`. O script exige relatórios recentes, de até duas horas, para evitar apresentar exemplos antigos como execução nova. Copiar o arquivo para um nome individual em `evidencias/` e salvar um print do terminal.

Responder com o próprio output:

1. Qual é o `trivy_created_at` vulnerável e qual versão corrige a CVE-2025-27516?
2. Qual é o `kics_started_at` corrigido, quantos HIGH restaram e quais duas propriedades removeram os HIGH?

Registrar separadamente downloads, execução dos comandos, pausas e ensaio explicado. Não usar o tempo automatizado como se fosse o tempo de condução da turma.

## 5. Automação, arquivos de saída e CI

Fora do cronômetro do LAB, executar no Mac/Linux:

```sh
python3 scripts/run_scan.py vulneravel --offline
python3 scripts/run_scan.py corrigido --offline
docker compose run --rm verify
python3 -m unittest scripts.test_gate -v
python3 scripts/verify_reports.py
```

No Windows, substituir `python3` por `python` se esse for o comando instalado. Executar cada linha separadamente; a primeira falha é intencional.

| Saída do executor | Significado |
|---|---|
| 1 / FAIL | Achados HIGH/CRITICAL; vulnerável tem dois HIGH do KICS |
| 0 / PASS | Nenhum achado acima do limiar; avisos menores continuam |
| 2 / ERROR | Falha operacional ou relatório inválido; não é evidência de vulnerabilidade |

O executor salva JSON, SARIF, SBOM CycloneDX do Trivy e resumos em `reports/gate/`. SARIF facilita intercâmbio de resultados de análise; o SBOM é um inventário, não certificado de segurança. O workflow publica artifacts; não foi configurado envio SARIF para GitHub Code Scanning nem integração com DefectDojo.

O teste imprime um cenário `ERROR` intencional para conferir que relatórios ausentes não produzem falso verde. O resultado final esperado do conjunto é **2 testes aprovados**.

O GitHub Actions executa em pull requests e pushes em `main`, usando o corrigido; o botão manual permite escolher cenário. Apenas subir uma branch não dispara esse workflow, até abrir um PR ou acioná-lo manualmente. O gate bloqueia HIGH/CRITICAL, preservando evidências mesmo quando o job falha. Não há deploy automático.

Evidências anteriores, ambas no commit `c736a60`, com fixtures diferentes:

- [Verde — run 36167707788](https://github.com/MaduKa01/CP01-DevSecOps/actions/runs/36167707788).
- [Vermelho — run 36167909434](https://github.com/MaduKa01/CP01-DevSecOps/actions/runs/36167909434).
- Relatórios preservados em `reports/ci/` e interpretação em `evidencias/pipeline.md`.

## 6. Complemento DAST: Nuclei

```sh
docker compose pull nuclei
docker compose --profile demo up -d --build --wait app-vulneravel app-corrigido
python3 scripts/run_dast.py
```

A construção instala as dependências dentro das imagens; `--wait` espera os alvos saudáveis. O script testa cada alvo com `nuclei/debug-exposure.yaml`, sem Interactsh e com download de templates públicos desativado. A configuração desse download segue a [documentação Nuclei](https://docs.projectdiscovery.io/opensource/nuclei/running).

Esperado: uma correspondência no vulnerável e zero no corrigido, ambos com validação OK. `/debug` retorna configuração fictícia no vulnerável e 404 no corrigido. A severidade MEDIUM foi definida pelo grupo no template. A ausência de correspondência só valida esse teste específico.

Ronaldo encontrou espera de aproximadamente 180 segundos por cenário antes do scan; a execução terminou corretamente. O ajuste no Compose desativou a busca automática de templates públicos e os testes diagnósticos subsequentes terminaram em menos de um segundo por cenário. A saída pessoal enviada corresponde à execução anterior ao ajuste: não atribuir a Ronaldo uma nova medição que ele não registrou. Evidência: `evidencias/diagnostico-nuclei-ronaldo.md`.

## 7. Complemento SAST: SonarQube

```sh
docker compose pull sonarqube sonar-scanner
docker compose --profile sonar up -d sonarqube
python3 scripts/setup_sonar.py
python3 scripts/run_sonar.py
```

Se o servidor ainda iniciar, consultar `docker compose logs sonarqube`, esperar a prontidão e repetir o setup antes da análise. O setup cria credenciais locais no `.env`, ignorado pelo Git. Não copiar o `.env` para a documentação, prints, commits ou mensagens. O painel é `http://127.0.0.1:19000`; usuário `admin`, senha gerada localmente.

A versão do servidor utilizada é Community 26.9.0.129388. O scanner fixado roda como AMD64; no Mac ARM64 depende de emulação. O servidor usa H2 para avaliação local. Relatórios são exportados para `reports/sonarqube/`.

Na máquina de Ronaldo, o histórico contém S4790 (MD5) encerrada após trocar por SHA-256 e S5332 (HTTP) aberta; reanálise pessoal: **1 aberta, 1 encerrada, 0 hotspots, 15,907 s**. Em uma instalação realmente nova, o histórico não existe: esperar o aviso HTTP no código atual, sem exigir uma issue MD5 encerrada. O antes/depois histórico está em `reports/sonarqube-antes/` e no commit `c736a60`; não reintroduzir o MD5 só para recriar o alerta.

O MD5 era checksum sem função de autenticação. A regra detectou o algoritmo, mas impacto explorável não foi demonstrado. HTTP é condição real, aceita apenas no isolamento didático; não classificar o alerta como falso positivo por causa disso. O retorno zero do scanner indica análise concluída, não aprovação universal de segurança.

## 8. Comparação das validações reais

| Item | Cauê — Windows | Ronaldo — Mac |
|---|---|---|
| Data | 25/09/2026 | 26/09/2026 |
| Sistema | Windows 64-bit, WSL 2.7.14 | macOS 26.5.2, ARM64 |
| Docker Desktop / Engine | 4.92.0 / 29.8.0 | 4.63.0 / 29.2.1 |
| Compose / Git / Python | 5.5.1 / 2.55.0 / 3.14.7 | 5.0.2 / 2.50.1 / 3.14.7 |
| Trivy vulnerável → corrigido | 3 MEDIUM → 0 | 3 MEDIUM → 0 |
| KICS vulnerável | 2 HIGH, 1 MEDIUM, 6 LOW | 2 HIGH, 1 MEDIUM, 6 LOW |
| KICS corrigido | 0 HIGH, 1 MEDIUM, 5 LOW | 0 HIGH, 1 MEDIUM, 5 LOW |
| Testes do gate | 2/2 | 2/2 |
| Tempo do fluxo LAB | 118,404 s automatizados | 1.136 s = 18min56s, com intervalos |
| Automação complementar | 25,535 s no fluxo relatado | 3,144 s + 2,539 s, soma das etapas por cenário |
| Dificuldade real | Teste dependia de executável Unix | Nuclei demorava na inicialização |
| Correção | Simulação com unittest.mock | Desativar download público; mostrar início/duração |

Os ambientes, caches e métodos diferem: **não concluir que Mac é mais rápido que Windows**. O cronômetro de Ronaldo iniciou às 03:20:52 UTC; o primeiro scan Trivy foi às 03:37:17 UTC. O total com pausas não é um ensaio contínuo. O LAB guiado de 12 minutos ainda precisa de ensaio humano.

Os dados de Windows vêm do relato/comprovante de Cauê; os do Mac vêm do output enviado por Ronaldo e dos relatórios locais. O comprovante Mac foi salvo após a sequência manual; os relatórios Trivy/KICS foram depois renovados pela automação. Por isso seus horários diferem, embora as contagens coincidam.

## 9. Três achados que o texto deve analisar

| Achado | Evidência e CWE | Triagem | Correção e comprovação |
|---|---|---|---|
| CVE-2025-27516 no Jinja2 | Requirements 3.1.4; Trivy; CWE-1336 | Versão afetada confirmada; exploração não realizada | Atualizar para 3.1.6; scan corrigido sem o achado |
| Container privilegiado | `privileged: true`; KICS; CWE-269 | Verdadeiro positivo na configuração estática | false; regra desaparece no corrigido |
| Escalada permitida | `allowPrivilegeEscalation: true`; KICS; CWE-269 | Verdadeiro positivo na configuração estática | false junto de privileged false; segundo HIGH removido |

Usar `evidencias/achados.md` para justificativas e fontes. Foram classificados 0 falsos positivos nos três achados principais revisados (0/3), não uma taxa global comprovada das ferramentas. Outros avisos não tiveram triagem completa. O Trivy usou a severidade da fonte selecionada automaticamente; não mudar MEDIUM para HIGH para melhorar a narrativa.

## 10. Dificuldades e interpretação de mensagens

| Mensagem/sintoma | Interpretação e ação |
|---|---|
| Docker mostra Client, mas não Server | Abrir Docker Desktop; no Windows conferir WSL e reinicialização |
| Trivy sem banco em modo offline | Preparar o banco com internet antes de repetir |
| Aviso `site-packages` | Detecção de licenças foi pulada; a varredura de vulnerabilidades do requirements continuou |
| `No enabled scanners found` em convert | Aviso de apresentação do relatório; conferir JSON e tabela de vulnerabilidades, não presumir scan ausente |
| KICS 50 no vulnerável | Bloqueio esperado pelos dois HIGH |
| Teste imprime ERROR e termina OK | Cenário negativo intencional do teste; conferir resultado final dos dois testes |
| `trailing whitespace` em logs | Espaços finais produzidos pelo Docker, não falha do scanner; nesta entrega foram removidos apenas esses espaços |
| Nuclei fica na tela inicial | Conferir o ajuste de download público e o relatório; evitar iniciar execuções simultâneas que gravem nos mesmos arquivos |
| SonarQube ainda não responde | Esperar inicialização, consultar logs e repetir setup |
| Comprovante rejeita relatório antigo | Refazer os scans na própria máquina; não alterar horários manualmente |
| Contagens diferentes em outra data | Registrar data/versão da base e revisar os novos achados sem ocultá-los |

Para parar apenas este projeto, preservando os dados:

```sh
docker compose --profile demo --profile sonar down
```

Não usar limpeza global do Docker nem remover os volumes durante o ensaio.

## 11. Como transformar este guia na pesquisa de 15–25 páginas

Sugestão: 22 páginas de conteúdo, além dos elementos pré/pós-textuais conforme a orientação da disciplina.

| Seção | Páginas sugeridas | O que escrever |
|---|---:|---|
| Introdução e objetivos | 1 | Problema, grupo, recorte e resultados buscados |
| Fundamentação e pipeline | 2 | SAST/SCA/IaC/DAST, shift-left e por que runtime continua necessário |
| Método e ambiente | 2 | Alvos próprios, isolamento, versões, caches, autoria/IA e limites |
| SonarQube | 2 | Identificação, técnica, uso, integrações e avaliação própria |
| Trivy | 2 | Mesmos itens; base de vulnerabilidades e SBOM |
| KICS | 2 | Mesmos itens; regras e políticas de configuração |
| Nuclei | 2 | Mesmos itens; template, matchers e alcance da cobertura |
| Reprodução do laboratório | 3 | Passos, comandos essenciais, resultados e comprovante |
| Achados e correções | 2 | Os três casos com CWE e triagem fundamentada |
| Validações e CI | 2 | Windows/Mac, branches, vermelho/verde e dificuldades |
| Quadro comparativo e limites | 1 | Complementaridade, custos operacionais, formatos e limites |
| Conclusão | 1 | O que foi comprovado e próximos controles necessários |

Para cada ferramenta, Edmar deve preencher uma ficha com **mantenedor, licença exata da edição usada, ano, linguagem, atividade recente, data/versão da última release consultada e comunidade**. Registrar data de acesso. Distinguir a versão fixada no laboratório da release mais recente; não assumir que produtos Community e comerciais têm a mesma licença/capacidade.

Depois descrever técnica com fonte (não atribuir taint analysis, AST, fuzzing ou outras técnicas só porque aparecem no enunciado), categorias de falhas, limites, instalação, flags, formatos, regras próprias e como revisar/suprimir falsos positivos. No nosso experimento não houve supressões. Sobre CI/IDE/pre-commit/SARIF/Code Scanning/DefectDojo, distinguir **suporte documentado** de **integração efetivamente implementada**. Não inventar resultados de linguagens ou vulnerabilidades que não foram testadas.

### Fontes primárias iniciais para a pesquisa

Estes links são pontos de partida; selecionar as páginas específicas usadas, conferir a edição/versão, completar autoria/título/data/acesso e formatar segundo ABNT. Uma lista de URLs não substitui citações no texto. Cobrir no mínimo 10 fontes efetivamente utilizadas, quatro primárias; todas abaixo são publicadas pelos projetos/organizações responsáveis.

1. [SonarQube Community Build — documentação](https://docs.sonarsource.com/sonarqube-community-build/).
2. [Código e licença SonarQube](https://github.com/SonarSource/sonarqube).
3. [Trivy — documentação](https://trivy.dev/docs/latest/).
4. [Código e releases Trivy](https://github.com/aquasecurity/trivy).
5. [KICS — comandos](https://docs.kics.io/latest/commands/).
6. [Código e licença KICS](https://github.com/Checkmarx/kics).
7. [Nuclei — execução e templates](https://docs.projectdiscovery.io/opensource/nuclei/running).
8. [Código e releases Nuclei](https://github.com/projectdiscovery/nuclei).
9. [Advisory Jinja2 — CVE-2025-27516](https://github.com/pallets/jinja/security/advisories/GHSA-cpwx-vrp4-4pq7).
10. [MITRE — CWE-269](https://cwe.mitre.org/data/definitions/269.html).
11. [MITRE — CWE-1336](https://cwe.mitre.org/data/definitions/1336.html).
12. [CycloneDX — especificação](https://cyclonedx.org/specification/overview/).
13. [GitHub — documentação Actions](https://docs.github.com/en/actions).
14. [KICS — regra de container privilegiado](https://docs.kics.io/latest/queries/kubernetes-queries/dd29336b-fe57-445b-a26e-e6aa867ae609/).

As fichas bibliográficas e de identificação precisam de pesquisa editorial adicional. Este guia fornece a reprodução e as evidências do grupo; não se apresenta como pesquisa acadêmica final pronta.

## 12. Pacote de evidências e trabalho restante

- `evidencias/validacao-ronaldo.md`, `comprovante-ronaldo.json` e `execucao-ronaldo.txt`: execução pessoal no Mac.
- `evidencias/validacao-kaue.md` e `comprovante-kaue.json`: reprodução Windows.
- `reports/`: arquivos que sustentam os números; `reports/ci/`: evidências históricas do GitHub.
- `evidencias/achados.md`: análise dos casos; `diagnostico-nuclei-ronaldo.md`: melhoria decorrente do teste.
- [PR #1 de Cauê](https://github.com/MaduKa01/CP01-DevSecOps/pull/1): contribuição integrada com teste portátil.
- `docs/ROTEIRO-APRESENTACAO-28-SLIDES.md`: estrutura para Pedro.

Edmar escreve e revisa a pesquisa, Pedro monta o PPTX e seu PDF, Ronaldo e Cauê conferem coerência técnica. Cada integrante registra commits de sua contribuição real, com a própria autoria. A autoria assistida por IA deve permanecer declarada.

Antes da entrega: revisar referências, inserir prints legíveis com legendas/fontes, gravar plano B, ensaiar LAB em 12 minutos e apresentação em 30 minutos, garantir acesso ao repositório e conferir que PDF/PPTX/LAB concordam nos números. A gravação, os arquivos finais, o ensaio e os comprovantes dos outros grupos permanecem pendentes até serem efetivamente realizados.
