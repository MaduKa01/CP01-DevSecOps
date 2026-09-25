# Análise dos achados — resultados reais de 25/09/2026

## 1. Jinja2 vulnerável — SCA

- **Ferramenta:** Trivy 0.74.0, scanner `vuln`.
- **Identificador:** CVE-2025-27516; severidade MEDIUM na fonte GHSA escolhida automaticamente.
- **Evidência:** `reports/trivy/vulneravel/results.json`, pacote Jinja2 3.1.4, correção 3.1.6; arquivo `fixtures/vulneravel/requirements.txt`, linha 1.
- **CWE:** CWE-1336, conforme o relatório Trivy.
- **Classificação:** verdadeiro positivo para dependência em versão afetada. O endpoint `/preview` recebe templates do usuário e usa SandboxedEnvironment, atendendo ao cenário de uso relevante. Não foi executada uma exploração de fuga da sandbox; detecção da versão e confirmação de exploração são evidências diferentes.
- **Justificativa:** o advisory do mantenedor descreve contorno da sandbox por interação entre o filtro `attr` e o método `format`, quando o usuário controla o template.
- **Correção:** atualizar Jinja2 para 3.1.6, mantendo MarkupSafe 3.0.3, e reconstruir a aplicação.
- **Validação:** `reports/trivy/corrigido/results.json` não contém as três CVEs encontradas no estado anterior.
- **Limite:** este scan não analisa pacotes do sistema operacional, não faz prova de exploração nem cobertura completa de licenças.
- **Fontes:** [advisory do Jinja](https://github.com/pallets/jinja/security/advisories/GHSA-cpwx-vrp4-4pq7), [changelog Jinja](https://jinja.palletsprojects.com/en/stable/changes/#version-3-1-6).

## 2. Container privilegiado — IaC

- **Ferramenta/regra:** KICS 2.1.20, `Container Is Privileged`, ID `dd29336b-fe57-445b-a26e-e6aa867ae609`.
- **Severidade:** HIGH; CWE-269, conforme a regra e o relatório.
- **Evidência:** `fixtures/vulneravel/deployment.yaml`, linha 31, `privileged: true`; `reports/kics/vulneravel/results.json`.
- **Classificação:** verdadeiro positivo na configuração declarada. Não foi criado um pod com essa permissão.
- **Justificativa:** o manifesto pede execução privilegiada e remove restrições importantes de isolamento caso seja implantado.
- **Correção:** `privileged: false`, preservando usuário não root, seccomp e remoção de capabilities.
- **Validação:** a regra desaparece em `reports/kics/corrigido/results.json`; o gate deixa de contabilizar esse HIGH.
- **Limite:** KICS não inspecionou um cluster real nem provou comprometimento de host.
- **Fontes:** [regra KICS](https://docs.kics.io/latest/queries/kubernetes-queries/dd29336b-fe57-445b-a26e-e6aa867ae609/), [CWE-269](https://cwe.mitre.org/data/definitions/269.html).

## 3. Escalada de privilégios permitida — IaC

- **Ferramenta/regra:** KICS 2.1.20, `Privilege Escalation Allowed`, ID `5572cc5e-1e4c-4113-92a6-7a8a3bd25e6d`.
- **Severidade:** HIGH; CWE-269.
- **Evidência:** `fixtures/vulneravel/deployment.yaml`, linha 32, `allowPrivilegeEscalation: true`; `reports/kics/vulneravel/results.json`.
- **Classificação:** verdadeiro positivo na configuração declarada.
- **Justificativa:** a propriedade permite que processos obtenham mais privilégios do que o processo pai. É um controle distinto de `privileged`, embora relacionado e sujeito à interação com outros privilégios.
- **Correção:** `allowPrivilegeEscalation: false` junto de `privileged: false`.
- **Validação:** a regra não aparece no relatório corrigido; o gate deixa de contabilizar o segundo HIGH.
- **Limite:** o risco foi identificado no arquivo; não foi executada escalada de privilégios.
- **Fontes:** [regra KICS](https://docs.kics.io/latest/queries/kubernetes-queries/5572cc5e-1e4c-4113-92a6-7a8a3bd25e6d/), [CWE-269](https://cwe.mitre.org/data/definitions/269.html).

## Evidência complementar: Nuclei

O template próprio `nuclei/debug-exposure.yaml` associa CWE-497 ao endpoint didático que
retorna configuração interna fictícia. Ele exige HTTP 200 e dois marcadores específicos,
reduzindo a chance de confundir uma página genérica com a exposição desejada.
O scanner encontrou uma correspondência no alvo vulnerável; no corrigido, `/debug`
retorna 404 e não corresponde ao mesmo template. As duas execuções terminaram sem erro de requisição.

Classificação: verdadeiro positivo dentro do exemplo simulado. Não houve vazamento de segredo real.
Severidade MEDIUM é atribuída pelo template do grupo, não calculada autonomamente pelo Nuclei.
Ausência de correspondência no cenário corrigido vale apenas para esse teste.

Relatórios: `reports/nuclei/vulneravel/results.jsonl`, `reports/nuclei/corrigido/results.jsonl`
e `reports/nuclei/summary.json`. Fonte: [CWE-497](https://cwe.mitre.org/data/definitions/497.html).

## Evidência complementar: SonarQube

A primeira análise encontrou `python:S4790` (CRITICAL, classificada como VULNERABILITY
pela versão usada) no MD5 e `python:S5332` (MINOR) no servidor HTTP.
O checksum foi trocado por SHA-256 no commit `c736a60`; a reanálise encerrou S4790 como FIXED.
A API de issues inclui histórico: duas entradas totais não significam duas issues ainda abertas.

**Triagem contextual:** o MD5 era apenas um checksum retornado junto do próprio texto, sem
comparação de autenticidade ou autorização. A presença do algoritmo fraco foi detectada
corretamente, mas não foi demonstrado impacto de segurança nesse uso. Tratar como alerta
contextual/possível falso positivo de impacto, sem inventar exploração. A troca por SHA-256
é uma melhoria simples que remove o alerta.

HTTP continua como issue aberta: foi aceito somente neste laboratório de rede Docker interna,
sem portas de aplicação publicadas. A condição HTTP é real; isolamento local não a transforma
em falso positivo. Em uma implantação externa seria necessário TLS e revisão completa.

Relatórios anteriores: `reports/sonarqube-antes/`; posteriores: `reports/sonarqube/`.
O campo `type` observado foi preservado: não rebatizamos automaticamente os resultados como hotspots.

## Falsos positivos e limitações da amostra

Nos três achados principais revisados acima, foram classificados **0 falsos positivos em 3 achados**.
Isso não estima a taxa global de falso positivo das ferramentas. O alerta MD5 tem discussão
contextual separada. Os demais avisos menores não receberam triagem individual completa.

O corrigido mantém 1 MEDIUM e 5 LOW de IaC: namespace, política/digest de imagem, AppArmor,
LimitRange e ResourceQuota. Nenhuma supressão foi usada. O escopo da correção demonstrada é
eliminar os HIGH e corrigir a raiz gravável, não transformar a fixture em um deployment pronto para produção.
