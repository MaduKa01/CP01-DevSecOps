# Demora na inicialização do Nuclei — 26/09/2026

Durante a etapa 9 executada por Ronaldo, o script ficou sem apresentar saída.
O diagnóstico foi realizado com assistência do Codex, enquanto a execução original
continuava. Os alvos estavam saudáveis e a execução terminou com sucesso.

## Evidência da execução original

- Início registrado: `2026-09-26T03:41:37.599461+00:00`.
- Vulnerável: 180,892 segundos, saída 0, uma correspondência, validação OK.
- Corrigido: 180,781 segundos, saída 0, zero correspondências, validação OK.
- Cada varredura HTTP levou menos de um segundo; a espera ocorreu antes dela.
- O script capturava a saída e só a apresentava após cada cenário terminar.

## Ajuste e verificação

Foi definido `DISABLE_NUCLEI_TEMPLATES_PUBLIC_DOWNLOAD=true` no serviço Nuclei.
A configuração é documentada pelo fornecedor para desativar o download de templates
públicos: https://docs.projectdiscovery.io/opensource/nuclei/running . O laboratório
usa um template próprio e uma rede isolada; não precisa desse download.

O teste diagnóstico automatizado com essa variável terminou em menos de um segundo
por cenário, com uma correspondência no vulnerável e zero no corrigido, sem erros
nas requisições. Esses testes não sobrescreveram os relatórios da execução original.
Isso sustenta que a espera estava associada à inicialização de templates públicos.

O script também passou a informar o início de cada cenário e sua duração ao terminar.
A configuração Compose e a sintaxe Python foram verificadas. A execução pessoal
do script após o ajuste ainda deve ser registrada por Ronaldo.

Este incidente pertence à demonstração complementar de DAST, fora do cronômetro
do laboratório principal Trivy/KICS. Ele não demonstra falha das aplicações. A reexecução pessoal do SonarQube foi
posteriormente concluída e está registrada em `validacao-ronaldo.md`.
