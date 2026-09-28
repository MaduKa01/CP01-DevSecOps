# Base conjunta para Edmar e Pedro

Atualizada em 26/09/2026. As validações do laboratório por Cauê no Windows e Ronaldo no Mac estão concluídas e documentadas. O ensaio explicado, a gravação e os arquivos acadêmicos finais ainda estão pendentes.

## Começar pelos dois guias

- [Guia para documentação e reprodução do zero](GUIA-PARA-DOCUMENTACAO.md): preparação, comandos, explicações, resultados, estrutura da pesquisa e fontes a consultar.
- [Roteiro de 28 slides](ROTEIRO-APRESENTACAO-28-SLIDES.md): conteúdo por slide, evidência visual, falas e tempo total de 30 minutos.

## Evidências de cada participante

- [Cauê](../evidencias/validacao-kaue.md): reprodução Windows, comprovante e correção de portabilidade com unittest.mock. [PR #1 integrado](https://github.com/MaduKa01/CP01-DevSecOps/pull/1); pipelines 36177350207 e 36177445043 registrados como aprovados na conferência anterior.
- [Ronaldo](../evidencias/validacao-ronaldo.md): execução pessoal Mac, output fornecido, comprovante, gate e análises complementares. Branch `feat/validacao-ronaldo`, preparada a partir do merge `76fbf53`.
- [Incidente Nuclei](../evidencias/diagnostico-nuclei-ronaldo.md): diagnóstico e ajuste da inicialização; distinguir execução pessoal dos testes assistidos.

## Números que devem coincidir no PDF e nos slides

| Ferramenta | Vulnerável/antes | Corrigido/depois 
|---|---|---|
| Trivy | 3 MEDIUM | 0 nas dependências declaradas |
| KICS | 2 HIGH, 1 MEDIUM, 6 LOW | 0 HIGH/CRITICAL, 1 MEDIUM, 5 LOW |
| Nuclei | 1 correspondência | 0 no mesmo template |
| SonarQube histórico | MD5 e HTTP abertos | MD5 encerrado, HTTP aberto; 0 hotspots |

O CI automatiza Trivy/KICS. Vermelho e verde históricos usam o mesmo commit e fixtures distintas. Zero achados neste recorte não equivale a segurança total. Os três achados principais revisados foram classificados como verdadeiros positivos: 0 falsos positivos em 3, sem inferência sobre a taxa global.

Cauê mediu 118,404 s de comandos automatizados. Ronaldo registrou 1.136 s com pausas; isso não prova tempo de ensaio nem superioridade de plataforma. Detalhes e limitações constam nos relatos e no guia.

## Próximas contribuições

Edmar produz a pesquisa final (15–25 páginas, mínimo 10 fontes/4 primárias), Pedro monta PPTX/PDF (28 slides propostos). Ronaldo e Cauê conferem evidências e ensaiam a execução com o grupo. Todos apresentam e registram contribuições reais. Plano B de 5–8 minutos ou GIF completo ainda deve ser gravado. Não marcar essas entregas como concluídas antes de existirem.
