# Direcionamento da apresentação — 28 slides / 30 minutos

Responsável pela montagem: Pedro. Todos apresentam. Coordenação e conferência técnica: Ronaldo; validação: Cauê; consistência com a pesquisa: Edmar.
Data: 28/09/2026 às 19h. Material preparado em 26/09/2026 a partir do PDF do professor e das execuções reais.

## Como usar este roteiro

Este arquivo orienta a criação do PPTX e do PDF de segurança; não é a apresentação final. São **28 slides**, dentro do intervalo de 20–30. Cada item abaixo contém conteúdo, visual, fala, fonte e tempo. Usar os números como expectativa observada em setembro/2026; o banco de vulnerabilidades pode mudar.

A turma deve copiar comandos do `LAB.md`, com o link correspondente à versão publicada. Não colocar comandos longos ilegíveis nos slides. Os slides 13–22 orientam o laboratório ao vivo; alternar para o terminal e voltar ao roteiro sem repetir a demonstração como palestra.

| Bloco | Slides | Tempo total |
|---|---|---:|
| Abertura e posicionamento | 1–4 | 3 min |
| Quatro ferramentas | 5–12 | 10 min, 2min30 por ferramenta |
| Laboratório com a turma | 13–22 | 12 min |
| Comparativo e encerramento | 23–27 | 3 min |
| Perguntas | 28 | 2 min |

As falas propostas somam aproximadamente: Edmar 6min50, Pedro 6min, Cauê 7min30 e Ronaldo 7min40, além das perguntas compartilhadas. Ensaiar transições e ajustar a divisão sem aumentar o total. A apresentação de ferramentas deve ser curta para preservar a prática, que tem maior peso na nota.

## Roteiro slide a slide

### 01. Segurança no pipeline: código, dependências, infraestrutura e aplicação

**Tempo:** 20s. **Fala:** Edmar.

- **Colocar no slide:** Nome da disciplina, Grupo 2, Ronaldo, Cauê, Edmar e Pedro; data; SonarQube, Trivy, KICS e Nuclei.
- **Visual/demonstração:** Capa simples com quatro categorias, sem print de terminal.
- **Explicar:** Apresentar o objetivo: detectar, corrigir e comprovar a mudança com relatórios.
- **Fonte/evidência:** `README.md`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 02. O que a turma fará nos próximos 30 minutos

**Tempo:** 40s. **Fala:** Edmar.

- **Colocar no slide:** 3 min abertura; 10 min ferramentas; 12 min laboratório; 3 min comparativo; 2 min perguntas.
- **Visual/demonstração:** Linha do tempo com cinco blocos.
- **Explicar:** Avisar que a turma executará Trivy e KICS; confirmar que os downloads foram feitos.
- **Fonte/evidência:** `PDF do professor, p. 10; LAB.md`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 03. Quatro categorias respondem a perguntas diferentes

**Tempo:** 60s. **Fala:** Edmar.

- **Colocar no slide:** SAST: código próprio; SCA: dependências; IaC: configuração; DAST: aplicação rodando. Destacar SAST versus SCA.
- **Visual/demonstração:** Tabela de quatro linhas com entrada e necessidade de execução da aplicação.
- **Explicar:** Uma biblioteca vulnerável pode estar presente mesmo que o código próprio pareça correto.
- **Fonte/evidência:** `README.md; fundamentação verificada no documento final`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 04. Onde cada análise entra no nosso projeto

**Tempo:** 60s. **Fala:** Edmar.

- **Colocar no slide:** Código → SonarQube; requirements → Trivy; manifesto → KICS; HTTP local → Nuclei. Gate automatizado: Trivy e KICS.
- **Visual/demonstração:** Diagrama do README adaptado com fonte; diferenciar CI de execução complementar.
- **Explicar:** Explicar shift-left e por que testar artefatos não substitui observar runtime. Alvos próprios em Docker isolado.
- **Fonte/evidência:** `README.md; docker-compose.yml; .github/workflows/security.yml`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 05. SonarQube: análise do código próprio

**Tempo:** 75s. **Fala:** Pedro.

- **Colocar no slide:** Categoria SAST; edição Community usada; servidor 26.9.0.129388 e scanner separado; entrada app/server.py; resultado por regra/localização.
- **Visual/demonstração:** Fluxo código → scanner → servidor → issues.
- **Explicar:** Explicar servidor versus scanner e que a técnica/capacidade depende da regra e da edição. Na pesquisa, conferir licença e mantenedor exatos; não usar funcionalidades comerciais como se fossem da edição testada.
- **Fonte/evidência:** `README.md; sonar-project.properties; documentação oficial SonarSource`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 06. SonarQube: o que mudou depois da análise

**Tempo:** 75s. **Fala:** Pedro.

- **Colocar no slide:** MD5 → SHA-256; S4790 encerrada; S5332 de HTTP permanece; reanálise pessoal 15,907 s, 1 aberta, 1 encerrada e 0 hotspots.
- **Visual/demonstração:** Trecho do diff c736a60 e recorte legível das issues antes/depois.
- **Explicar:** MD5 era checksum sem papel de autenticação: impacto não demonstrado. HTTP é real e aceito apenas no laboratório isolado. Histórico de duas entradas não significa duas issues abertas.
- **Fonte/evidência:** `evidencias/achados.md; reports/sonarqube-antes/; reports/sonarqube/summary.json`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 07. Trivy: versões de dependências e vulnerabilidades conhecidas

**Tempo:** 75s. **Fala:** Edmar.

- **Colocar no slide:** Categoria SCA; Trivy 0.74.0; Jinja2 e MarkupSafe declarados; consulta à base de vulnerabilidades; saída JSON/SARIF.
- **Visual/demonstração:** Recorte do requirements e seta para uma linha do relatório.
- **Explicar:** Versão do scanner e data do banco são coisas diferentes. O scan comprova a versão afetada; não demonstra exploração.
- **Fonte/evidência:** `reports/trivy/vulneravel/results.json; fixtures/vulneravel/requirements.txt; documentação Trivy`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 08. Trivy: correção, inventário e limites

**Tempo:** 75s. **Fala:** Edmar.

- **Colocar no slide:** Jinja2 3.1.4 → 3.1.6; três MEDIUM → zero nas dependências declaradas; SBOM CycloneDX gerado pelo executor.
- **Visual/demonstração:** Antes/depois curto e pequeno exemplo de componente do SBOM.
- **Explicar:** SBOM é inventário. Esta execução não cobre imagem base do SO nem licenças completas; o aviso de site-packages deve ser explicado.
- **Fonte/evidência:** `reports/trivy/corrigido/results.json; reports/trivy/corrigido/sbom.cdx.json; scripts/run_scan.py`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 09. KICS: revisar a infraestrutura antes de implantar

**Tempo:** 75s. **Fala:** Cauê.

- **Colocar no slide:** Categoria IaC; KICS 2.1.20; lê deployment.yaml; regras retornam severidade, local e CWE; outputs JSON/SARIF.
- **Visual/demonstração:** Trecho de securityContext com duas propriedades destacadas.
- **Explicar:** É análise estática: não criamos cluster e não concedemos esses privilégios ao Compose.
- **Fonte/evidência:** `fixtures/vulneravel/deployment.yaml; reports/kics/vulneravel/results.json; documentação KICS`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 10. KICS: os dois HIGH que bloqueiam o projeto

**Tempo:** 75s. **Fala:** Cauê.

- **Colocar no slide:** privileged: true; allowPrivilegeEscalation: true; CWE-269; correção false/false; raiz somente leitura remove um LOW adicional.
- **Visual/demonstração:** Comparação de três linhas antes/depois.
- **Explicar:** As propriedades são distintas e relacionadas. Gate corrigido aceita 1 MEDIUM e 5 LOW; não ocultamos esses avisos.
- **Fonte/evidência:** `evidencias/achados.md; fixtures/corrigido/deployment.yaml`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 11. Nuclei: observar o comportamento da aplicação

**Tempo:** 75s. **Fala:** Pedro.

- **Colocar no slide:** Categoria DAST; Nuclei 3.11.1; um template próprio; GET /debug; exige HTTP 200 e dois marcadores de configuração fictícia.
- **Visual/demonstração:** Fluxo scanner → app local → resposta → correspondência; trecho pequeno dos matchers.
- **Explicar:** O alvo precisa estar ativo. A severidade MEDIUM vem do template do grupo; os dados são simulados.
- **Fonte/evidência:** `nuclei/debug-exposure.yaml; app/server.py; documentação Nuclei`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 12. Nuclei: resultado e dificuldade encontrada

**Tempo:** 75s. **Fala:** Pedro.

- **Colocar no slide:** Uma correspondência no vulnerável e zero no corrigido; original demorou cerca de 180 s por cenário; download público desativado eliminou espera nos testes diagnósticos.
- **Visual/demonstração:** Tabela com antes/depois funcional; uma anotação sobre a inicialização.
- **Explicar:** Não confundir scan de um template com auditoria completa. Diferenciar a execução pessoal de Ronaldo dos testes de diagnóstico assistidos.
- **Fonte/evidência:** `reports/nuclei/summary.json; evidencias/diagnostico-nuclei-ronaldo.md`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 13. Laboratório: abrir o roteiro e conferir a pasta

**Tempo:** 30s. **Fala:** Cauê.

- **Colocar no slide:** Link/QR para LAB.md na versão publicada; objetivo: detectar e corrigir com Trivy + KICS; downloads antecipados.
- **Visual/demonstração:** QR grande, link escrito e comando cd CP01-DevSecOps.
- **Explicar:** Iniciar cronômetro do bloco de 12 minutos; quem tiver instalação pendente acompanha e usa o plano B depois.
- **Fonte/evidência:** `LAB.md; URL exata da branch ou main após integração`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 14. Laboratório: conferir as versões

**Tempo:** 30s. **Fala:** Cauê.

- **Colocar no slide:** docker compose run --rm trivy --version; docker compose run --rm kics version.
- **Visual/demonstração:** Dois comandos grandes; espaço para a saída ao vivo.
- **Explicar:** Esperado: 0.74.0 e 2.1.20. Mostrar a data do banco e explicar que a versão das imagens está fixada.
- **Fonte/evidência:** `LAB.md, etapa 1`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 15. Laboratório: executar o Trivy vulnerável

**Tempo:** 90s. **Fala:** Cauê.

- **Colocar no slide:** Executar os dois comandos da etapa 2 do LAB: scan JSON e convert. Resultado: três MEDIUM em Jinja2 3.1.4.
- **Visual/demonstração:** Terminal ao vivo; slide mantém somente nome da etapa, caminho de entrada e resultado esperado.
- **Explicar:** Turma copia comandos do LAB, não da imagem. Explicar os avisos sem tratá-los como bloqueio da varredura.
- **Fonte/evidência:** `LAB.md, etapa 2; reports/trivy/vulneravel/results.json`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 16. Laboratório: interpretar uma CVE

**Tempo:** 90s. **Fala:** Cauê.

- **Colocar no slide:** CVE-2025-27516; CWE-1336; versão afetada 3.1.4; correção indicada 3.1.6; verdadeiro positivo de dependência.
- **Visual/demonstração:** Recorte legível da linha do Trivy e link do advisory do mantenedor.
- **Explicar:** Explicar evidência versus exploração: a aplicação usa templates, mas não demonstramos fuga de sandbox. Este é o achado 1 dos três exigidos.
- **Fonte/evidência:** `evidencias/achados.md, caso 1; advisory Jinja2`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 17. Laboratório: executar o KICS vulnerável

**Tempo:** 60s. **Fala:** Cauê.

- **Colocar no slide:** Executar etapa 3 do LAB; 2 HIGH, 1 MEDIUM e 6 LOW; saída 50 esperada.
- **Visual/demonstração:** Terminal ao vivo e destaque de duas regras HIGH.
- **Explicar:** Ler o código de saída imediatamente; diferenciar bloqueio por política de erro operacional.
- **Fonte/evidência:** `LAB.md, etapa 3; reports/kics/vulneravel/results.json`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 18. Laboratório: explicar os dois achados de configuração

**Tempo:** 60s. **Fala:** Ronaldo.

- **Colocar no slide:** Container privilegiado e escalada permitida; ambos CWE-269; verdadeiros positivos no arquivo; false/false remove os HIGH.
- **Visual/demonstração:** Duas colunas: propriedade insegura e correção; mostrar também readOnlyRootFilesystem.
- **Explicar:** Estes são os achados 2 e 3. Não afirmar que invadimos host ou executamos um pod privilegiado.
- **Fonte/evidência:** `evidencias/achados.md, casos 2 e 3`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 19. Laboratório: executar o cenário corrigido

**Tempo:** 90s. **Fala:** Ronaldo.

- **Colocar no slide:** Rodar os três comandos da etapa 4: Trivy JSON, gate Trivy e KICS corrigido.
- **Visual/demonstração:** Terminal ao vivo; tabela esperada Trivy 0, KICS 0 HIGH/CRITICAL.
- **Explicar:** Comparar fixtures antes dos comandos. Correção não muda o limiar nem esconde regras.
- **Fonte/evidência:** `LAB.md, etapa 4; fixtures/corrigido/`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 20. Laboratório: conferir o que ainda permanece

**Tempo:** 90s. **Fala:** Ronaldo.

- **Colocar no slide:** Trivy: zero no conjunto declarado; KICS: 1 MEDIUM e 5 LOW; saída 0 dos gates; nenhum HIGH/CRITICAL.
- **Visual/demonstração:** Tabela antes/depois, com avisos menores visíveis.
- **Explicar:** O verde é o cumprimento de uma política. Namespace, imagem e controles adicionais continuam como limitações da fixture.
- **Fonte/evidência:** `reports/kics/corrigido/results.json; evidencias/achados.md`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 21. Laboratório: abrir os builds vermelho e verde

**Tempo:** 60s. **Fala:** Ronaldo.

- **Colocar no slide:** Vermelho: dois HIGH, errors vazio, executor 1. Verde: zero bloqueantes, executor 0. Mesmo commit, fixtures diferentes.
- **Visual/demonstração:** Dois prints/links dos runs já concluídos, com ID e status legíveis.
- **Explicar:** Não esperar novo CI durante o LAB. O workflow preserva artifacts em falha; não usamos continue-on-error para produzir verde.
- **Fonte/evidência:** `evidencias/pipeline.md; runs 36167909434 e 36167707788`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 22. Laboratório: comprovante e duas perguntas

**Tempo:** 120s. **Fala:** Ronaldo.

- **Colocar no slide:** docker compose run --rm verify python scripts/comprovante.py; salvar print; responder timestamp Trivy + versão de correção e timestamp KICS + HIGH + propriedades corrigidas.
- **Visual/demonstração:** Duas perguntas e exemplo de campos do comprovante, sem dar os timestamps pessoais como resposta universal.
- **Explicar:** Cada pessoa responde com sua execução. O verificador rejeita relatórios com mais de duas horas. Encerrar o cronômetro do laboratório.
- **Fonte/evidência:** `LAB.md, etapa 5; scripts/comprovante.py`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 23. As ferramentas cobrem partes diferentes do problema

**Tempo:** 40s. **Fala:** Edmar.

- **Colocar no slide:** Comparar entrada, categoria, necessidade de runtime, saída usada e principal limitação das quatro ferramentas.
- **Visual/demonstração:** Matriz de quatro linhas; máximo cinco colunas além da ferramenta.
- **Explicar:** Recomendar a combinação: SAST no código, SCA nas dependências, IaC no manifesto e DAST em ambiente autorizado após subir a aplicação.
- **Fonte/evidência:** `README.md; GUIA-PARA-DOCUMENTACAO.md, seções 1 e 11`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 24. Duas máquinas, mesmos resultados principais

**Tempo:** 40s. **Fala:** Edmar.

- **Colocar no slide:** Windows/Cauê e Mac/Ronaldo: mesmos três MEDIUM e mesmos dois HIGH antes; remoção dos bloqueantes depois; testes 2/2.
- **Visual/demonstração:** Tabela pequena de contagens, com data e sistema operacional.
- **Explicar:** Windows teve teste portátil corrigido; Mac teve ajuste de inicialização do Nuclei. Não comparar desempenho dos sistemas: caches e métodos diferentes.
- **Fonte/evidência:** `evidencias/validacao-kaue.md; evidencias/validacao-ronaldo.md`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 25. Limitações que os relatórios não resolvem

**Tempo:** 40s. **Fala:** Ronaldo.

- **Colocar no slide:** 0/3 falsos positivos apenas nos casos revisados; sem prova de exploração SCA; sem cluster; DAST com um template; HTTP ainda aberto; ensaio humano separado das medições automáticas.
- **Visual/demonstração:** Lista de cinco ou seis linhas legíveis, sem parágrafo.
- **Explicar:** Assumir os limites da amostra. Não afirmar 100% seguro, cobertura total, zero vulnerabilidades globais ou benchmark entre sistemas.
- **Fonte/evidência:** `evidencias/achados.md; evidencias/metricas.md; relatos de validação`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 26. Entrega, colaboração e próximos controles

**Tempo:** 30s. **Fala:** Pedro.

- **Colocar no slide:** Branches com contribuições reais; PR #1 de Cauê; branch/PR de Ronaldo conforme estado real; PDF, slides, LAB e evidências juntos; uso de IA declarado.
- **Visual/demonstração:** Captura de histórico/PR com títulos claros e pequeno checklist.
- **Explicar:** Mostrar o que foi concluído e somente então marcar gravação e ensaio quando existirem. Todos devem compreender o conjunto.
- **Fonte/evidência:** `USO-DE-IA.md; histórico Git; evidencias/plano-b.md`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 27. Fontes e material para continuar

**Tempo:** 30s. **Fala:** Pedro.

- **Colocar no slide:** Links do repositório, LAB, pesquisa final e documentação oficial das quatro ferramentas; conclusão: reduzir risco com evidência e limites explícitos.
- **Visual/demonstração:** QR do repositório, seis referências curtas legíveis; referências completas no documento.
- **Explicar:** Citar fontes também nos rodapés dos slides correspondentes; este slide não substitui atribuições de imagens e afirmações.
- **Fonte/evidência:** `GUIA-PARA-DOCUMENTACAO.md, fontes; PDF final quando disponível`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

### 28. Perguntas

**Tempo:** 120s. **Fala:** Todos.

- **Colocar no slide:** Onde termina a evidência de cada ferramenta? Por que o verde ainda tem avisos? Como confirmar que o relatório é da execução atual?
- **Visual/demonstração:** QR do LAB/repositório e título simples; deixar outputs e plano B acessíveis.
- **Explicar:** Responder com os relatórios. Se perguntarem algo não testado, distinguir capacidade documentada de resultado observado.
- **Fonte/evidência:** `LAB.md; evidencias/achados.md; relatórios versionados`. Os caminhos são relativos ao repositório; links externos devem ser clicáveis no arquivo final.

## Orientação visual e referências

- Usar formato 16:9, títulos curtos, fontes grandes e contraste alto. Uma mensagem principal por slide.
- Preferir recortes legíveis de terminal a prints de tela inteira. Manter comando, regra/CVE, severidade e resultado visíveis; ocultar credenciais e dados desnecessários.
- Usar verde/vermelho junto de palavras PASS/FAIL: não depender somente da cor.
- Identificar capturas por ferramenta, cenário, data e arquivo/run. Usar evidências reais; não desenhar terminal fictício para parecer execução.
- Citar fonte externa no slide em que foi utilizada. Diagramas feitos pelo grupo podem ser identificados como elaboração própria; IA deve ser declarada conforme USO-DE-IA.md.
- Para SonarQube, não chamar issues de hotspots: os relatórios observados registram zero hotspots.
- Versões usadas estão fixadas no Compose; não usar “última versão” sem consulta atual e fonte.

## Arquivos e telas que Pedro deve separar antes de montar

1. Diff `fixtures/vulneravel/` versus `fixtures/corrigido/`.
2. Trivy vulnerável com CVE-2025-27516 e correção 3.1.6.
3. KICS vulnerável com os dois HIGH e corrigido com os avisos restantes.
4. Comprovantes individuais em `evidencias/comprovante-kaue.json` e `comprovante-ronaldo.json`.
5. SonarQube antes/depois em `reports/sonarqube-antes/` e `reports/sonarqube/`.
6. Nuclei com uma/zero correspondências em `reports/nuclei/`.
7. [CI vermelho](https://github.com/MaduKa01/CP01-DevSecOps/actions/runs/36167909434) e [CI verde](https://github.com/MaduKa01/CP01-DevSecOps/actions/runs/36167707788).
8. [PR de Cauê](https://github.com/MaduKa01/CP01-DevSecOps/pull/1) e [branch de Ronaldo](https://github.com/MaduKa01/CP01-DevSecOps/tree/feat/validacao-ronaldo). Conferir o estado do PR de Ronaldo antes da captura; não afirmar merge se ainda estiver aberto.
9. Vídeo/GIF de plano B, depois de gravado; verificar local, áudio/legibilidade e duração.

O guia detalhado para consultar conceitos e comandos é `docs/GUIA-PARA-DOCUMENTACAO.md`. A análise técnica dos três casos fica em `evidencias/achados.md`.

## Plano B e ensaio

Gravar a execução completa com explicação dos achados, correções e gates em 5–8 minutos, ou GIF completo conforme o PDF. O arquivo ainda precisa ser produzido; as saídas de terminal não substituem gravação. Não reproduzir o vídeo inteiro além dos 12 minutos do laboratório: usá-lo como substituição se houver impedimento.

Antes da aula: baixar imagens/base, testar no computador que será usado, abrir links de evidências, conferir acesso da turma, testar o arquivo PPTX e seu PDF. Rodar ensaio humano contínuo do LAB em 12 minutos e do conjunto em 30. As medições automáticas do Cauê e os 18min56s com pausas de Ronaldo não comprovam esse ensaio.

## Checklist de fechamento para Pedro

- [ ] Exatamente 28 slides, com capa, agenda, quatro ferramentas, demo, comparação e limitações.
- [ ] Os quatro integrantes têm falas ensaiadas e sabem explicar os três achados.
- [ ] Cada número corresponde ao relatório certo, com antes/depois e fonte.
- [ ] QR/link aponta para uma versão acessível do LAB; comandos estão copiáveis nele.
- [ ] Prints não mostram `.env`, senha ou token; nenhuma evidência usa alvo externo.
- [ ] PPTX e PDF conferidos, com fontes legíveis e links funcionando.
- [ ] Plano B gravado/testado e cronômetro dentro dos limites.
- [ ] Arquivos finais no repositório, com contribuição real registrada por quem os produziu.
