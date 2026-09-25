"""Confere contraste didático e integridade mínima das evidências geradas."""
import json
from pathlib import Path
import sys


def verify(root):
    for variant in ("vulneravel", "corrigido"):
        summary = json.loads((root / "reports" / "gate" / variant / "summary.json").read_text())
        expected = "FAIL" if variant == "vulneravel" else "PASS"
        if summary["status"] != expected or summary["errors"]:
            raise ValueError(f"{variant}: esperado {expected}, obtido {summary['status']}")
        for tool in ("trivy", "kics"):
            report_path = root / "reports" / tool / variant / "results.json"
            data = json.loads(report_path.read_text())
            if tool == "trivy":
                findings = [v for r in data.get("Results", []) for v in r.get("Vulnerabilities", [])]
                if variant == "vulneravel" and not any(v["PkgName"].lower() == "jinja2" for v in findings):
                    raise ValueError("O exemplo vulnerável não produziu achados em Jinja2")
                if variant == "corrigido" and findings:
                    raise ValueError("Surgiram novos achados SCA no estado corrigido; revisar a base atual")
            elif not data.get("files_scanned") or data.get("files_failed_to_scan") or data.get("queries_failed_to_execute"):
                raise ValueError("KICS não concluiu análise válida")
        print(f"OK: {variant} -> {expected}, {summary['blocking_findings']} bloqueantes")


if __name__ == "__main__":
    try:
        verify(Path(__file__).resolve().parents[1])
    except (OSError, ValueError, KeyError) as exc:
        print(f"FALHA: {exc}", file=sys.stderr)
        sys.exit(1)
