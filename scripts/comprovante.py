"""Imprime identificadores e resultados recentes das execuções feitas pelo aluno."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
try:
    result = {}
    now = datetime.now(timezone.utc)
    for variant in ("vulneravel", "corrigido"):
        trivy = json.loads((root / "reports/trivy" / variant / "results.json").read_text())
        kics = json.loads((root / "reports/kics" / variant / "results.json").read_text())
        for value in (trivy["CreatedAt"], kics["start"]):
            recorded = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if not -300 <= (now - recorded).total_seconds() <= 7200:
                raise ValueError("Relatórios com mais de 2 horas ou data inválida: execute novamente os passos do LAB.md")
        if kics.get("files_scanned", 0) < 1 or kics.get("files_failed_to_scan") or kics.get("queries_failed_to_execute"):
            raise ValueError("KICS não concluiu a análise")
        findings = [v for r in trivy.get("Results", []) for v in r.get("Vulnerabilities", [])]
        result[variant] = {
            "trivy_created_at": trivy["CreatedAt"],
            "trivy_vulnerabilities": len(findings),
            "jinja_cve_2025_27516_fixed_version": next((v.get("FixedVersion") for v in findings if v["VulnerabilityID"] == "CVE-2025-27516"), None),
            "kics_started_at": kics["start"],
            "kics_counts": kics["severity_counters"],
            "kics_high_rules": [q["query_name"] for q in kics["queries"] if q["severity"] == "HIGH"],
        }
    if result["vulneravel"]["kics_counts"].get("HIGH", 0) < 1:
        raise ValueError("O cenário vulnerável não comprovou HIGH")
    if any(result["corrigido"]["kics_counts"].get(s, 0) for s in ("HIGH", "CRITICAL")):
        raise ValueError("O cenário corrigido ainda tem bloqueantes: revisar os resultados")
    (root / "reports/comprovante.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("COMPROVANTE GERADO: reports/comprovante.json — salve este output e responda às duas perguntas.")
except (OSError, ValueError, KeyError) as exc:
    print(f"NÃO FOI POSSÍVEL GERAR COMPROVANTE: {exc}", file=sys.stderr)
    sys.exit(1)
