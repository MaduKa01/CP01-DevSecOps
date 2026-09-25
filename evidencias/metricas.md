# Tempos e resultados observados

Medições reais de 25/09/2026. Uma execução por cenário; não são benchmark estatístico nem tempo de ensaio da turma.

## Mac local

MacBook Pro M3 Pro, 18 GB físicos; Docker 29.2.1 em ARM64, 11 CPUs e aproximadamente 7,65 GiB disponíveis à VM. As imagens e a base já estavam baixadas para as medições de SCA/IaC.

| Cenário | Scan Trivy | Scan KICS | Fluxo completo com exports e gate |
|---|---:|---:|---:|
| vulneravel | 0.587s | 1.770s | 3.244s |
| corrigido | 0.452s | 1.291s | 2.723s |

Os tempos incluem criação/remoção dos containers. O fluxo completo inclui JSON, SARIF, SBOM CycloneDX e verificação de severidade. Não incluem pull das imagens nem o download inicial de cerca de 117 MiB da base.

Base Trivy utilizada: versão 2; atualizada em 25/09/2026 às 13:09:04 UTC e baixada às 17:17:23 UTC. Fonte de severidade observada para Jinja2: GHSA. Não foram usadas supressões.

## Nuclei

Um único template local; um alvo por execução; sem Interactsh, atualização automática ou conexão a sites públicos.
- vulneravel: 0.722s incluindo criação do container; 1 correspondências; execução validada: True.
- corrigido: 0.633s incluindo criação do container; 0 correspondências; execução validada: True.

## SonarQube

Servidor Community 26.9.0.129388 em ARM64; scanner 12.2.0.4256_8.1.0 em AMD64 por emulação. H2 é utilizado somente para avaliação.
- Antes da correção: 19.663s, 2 issues abertas, 0 encerradas e 0 hotspots.
- Depois da correção: 15.652s, 1 issues abertas, 1 encerradas e 0 hotspots.

Esses tempos incluem inicialização do scanner e espera do processamento, mas não a subida inicial do servidor nem pull. A segunda execução utiliza caches já preenchidos; não concluir que a mudança para SHA-256 acelerou a análise.

## GitHub Actions / AMD64

Os relatórios originais baixados dos artifacts ficam em `reports/ci/`. Isso valida outro ambiente de execução, mas não substitui o ensaio humano de Cauê em outra máquina.
- Run 36167707788, corrigido: PASS; 0 bloqueantes; 15.661s nos comandos registrados. O primeiro scan no runner inclui preparação de base, portanto não comparar diretamente com o cache aquecido do Mac.
- Run 36167909434, vulneravel: FAIL; 2 bloqueantes; 14.088s nos comandos registrados. O primeiro scan no runner inclui preparação de base, portanto não comparar diretamente com o cache aquecido do Mac.

## Limitações práticas

- Fixture pequena: estes tempos não representam monorepositórios ou aplicações grandes.
- SCA por requirements não comprova exploração nem examina a imagem base do SO.
- KICS analisa arquivos; não foi implantado um cluster.
- Nuclei cobre somente um template criado para a condição demonstrada.
- SonarQube precisa de servidor e recursos adicionais; por isso ficou fora do lab de 12 minutos.
- O teste em máquina alheia e o ensaio cronometrado da turma continuam pendentes.
