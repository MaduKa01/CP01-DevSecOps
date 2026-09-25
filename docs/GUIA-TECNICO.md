# Guia rápido do projeto — Ronaldo

## O que está pronto

O projeto tem uma aplicação pequena, as quatro ferramentas do grupo configuradas,
resultados reais, análise dos achados e um pipeline executado no GitHub.
O LAB.md já descreve a atividade que a turma vai seguir.

| Parte | Função |
|---|---|
| `app/server.py` | Aplicação Python que responde a health check, renderiza um template e simula uma configuração interna exposta no estado vulnerável |
| `fixtures/vulneravel/` | Jinja2 antigo e manifesto com privilégios excessivos |
| `fixtures/corrigido/` | Dependência atualizada e permissões reduzidas |
| `docker-compose.yml` | Reúne ferramentas e aplicação com versões fixadas |
| `scripts/` | Executa scanners, verifica relatórios e gera comprovantes |
| `reports/` | Guarda os resultados brutos, incluindo os produzidos no GitHub |
| `evidencias/` | Explica os achados, as métricas e os builds vermelho/verde |

## A lógica do laboratório

**Arquivo vulnerável → scanner → relatório → correção → scanner novamente.**

Trivy responde: “As dependências declaradas têm vulnerabilidades conhecidas?”
KICS responde: “Esse arquivo de infraestrutura pede uma configuração insegura?”
O gate bloqueia quando encontra HIGH ou CRITICAL. Os achados menores continuam visíveis.

O estado vulnerável produziu dois HIGH no KICS e três MEDIUM no Trivy.
O corrigido removeu os dois HIGH e as três vulnerabilidades de dependência; ficaram
um MEDIUM e cinco LOW de infraestrutura. Portanto, ele passa pela política definida.

Nuclei analisa o alvo funcionando, com um template próprio: detectou o `/debug` no
vulnerável e não o encontrou no corrigido. SonarQube analisa o código: identificou MD5,
que foi trocado por SHA-256, e um aviso sobre HTTP que continua registrado.

## Onde trabalhar

O VS Code está com a pasta **CP01-DevSecOps** aberta na janela que estava em Welcome.
A janela do OneShift foi preservada. Abra o terminal nessa janela e confirme que o
diretório atual termina em `CP01-DevSecOps` antes de executar comandos.

O VS Code abriu o projeto em Restricted Mode. A análise foi executada pelo terminal
controlado pelo Codex; nenhuma configuração de confiança do editor foi alterada.

## O que fazer agora

1. Ler o README e acompanhar os comandos do LAB.md, observando os relatórios.
2. Pedir ao Cauê que clone o repositório em outra máquina e execute apenas o LAB.md.
3. Enviar a Edmar os arquivos `evidencias/achados.md` e `evidencias/metricas.md`.
4. Enviar a Pedro os links de CI em `evidencias/pipeline.md` e a tabela de resultados do README.
5. Gravar o plano B com o roteiro de `evidencias/plano-b.md` e ensaiar a apresentação.

Para reproduzir a automação local completa do lab principal, com Python 3 disponível:

```sh
python3 scripts/run_scan.py vulneravel --offline
```

Esse comando termina com falha esperada por segurança. Depois:

```sh
python3 scripts/run_scan.py corrigido --offline
docker compose run --rm verify
```

A turma usa os comandos Docker do LAB.md e não precisa instalar Python no host.

## O que ainda precisa ser concluído pelo grupo

- Documento acadêmico final de 15–25 páginas de conteúdo.
- Apresentação final de 20–30 slides, em PPTX e PDF.
- Teste humano em outra máquina e ensaio dentro dos 12/30 minutos.
- Vídeo de 5–8 minutos ou GIF completo.
- Commits reais dos demais integrantes e entrega formal dos artefatos.

## Acesso e isolamento

O [repositório](https://github.com/MaduKa01/CP01-DevSecOps) já recebeu a implementação.
Os alvos ficam em uma rede interna Docker, sem porta aberta para a rede da máquina.
O SonarQube pode ser aberto em `http://127.0.0.1:19000`; login `admin` e senha no `.env`
local, que não vai para o GitHub. Não compartilhar esse arquivo.

Todos os recursos Docker deste trabalho têm o prefixo `cp01-devsecops`.
Para parar apenas este projeto, dentro da sua pasta:

```sh
docker compose --profile demo --profile sonar down
```

O comando preserva as evidências e os volumes. As etapas do lab principal não alteram
ou implantam os manifests Kubernetes.
