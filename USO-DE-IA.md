# Uso de IA generativa

Ferramenta: Codex, utilizado com supervisão de Ronaldo.

## Material assistido por IA

- Leitura e organização dos requisitos do PDF fornecido pelo professor.
- Plano do grupo e proposta de divisão das atividades.
- Aplicação didática, fixtures, configuração Docker, scripts, pipeline e rascunhos de documentação.
- Pesquisa em documentação oficial e interpretação inicial de resultados.

## Validação

As execuções efetivamente concluídas são registradas em `evidencias/` e `reports/`.
Rascunhos e previsões não equivalem a resultados executados.
Os integrantes devem revisar código, referências, achados e falas antes da entrega.
O teste independente de Cauê, a revisão editorial de Edmar, a conferência dos slides
por Pedro e o ensaio do grupo permanecem pendentes até que cada responsável os realize.

Não são atribuídas aos integrantes contribuições que eles não tenham realizado.

## Validações concluídas em 25/09/2026

- Execução local de Trivy/KICS nos dois estados, com gate vermelho e verde.
- Execução de Nuclei nos dois alvos locais, com uma e zero correspondências.
- Execução SonarQube, revisão do resultado e reanálise após SHA-256.
- GitHub Actions em runner Linux: cenário corrigido aprovado e vulnerável bloqueado; artifacts baixados e conferidos.
- Testes de falha operacional/relatório antigo e smoke tests benignos dos endpoints.
- Verificação de que as credenciais geradas no .env não aparecem nos arquivos publicados.

Estas execuções foram automatizadas com assistência de Codex. A revisão e o ensaio humanos continuam necessários e não são declarados como já realizados.
