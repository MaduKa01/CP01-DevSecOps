#!/usr/bin/env python3
"""Executa ambos os scanners; 0=gate aprovado, 1=achados bloqueantes, 2=erro."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def run(command, log):
    started = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log.write_text(result.stdout, encoding="utf-8")
    return {"command": command, "exit_code": result.returncode, "seconds": round(time.perf_counter() - started, 3)}


def load_report(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("variant", choices=["vulneravel", "corrigido"])
    parser.add_argument("--offline", action="store_true", help="Usa banco do Trivy já baixado, sem atualização.")
    args = parser.parse_args()
    variant = args.variant
    metadata = {"variant": variant, "started_at": datetime.now(timezone.utc).isoformat(), "steps": {}, "errors": []}
    for name in ("trivy", "kics", "gate"):
        directory = ROOT / "reports" / name / variant
        directory.mkdir(parents=True, exist_ok=True)
        # Evita aceitar relatório antigo após erro de um scanner.
        for file in directory.iterdir():
            if file.is_file():
                file.unlink()
    compose = ["docker", "compose", "run", "--rm", "-T"]
    trivy_path = ROOT / "reports" / "trivy" / variant
    kics_path = ROOT / "reports" / "kics" / variant
    gate_path = ROOT / "reports" / "gate" / variant
    trivy_cmd = compose + ["trivy", "fs", "--scanners", "vuln", "--format", "json", "--output", f"/reports/trivy/{variant}/results.json", "--exit-code", "0", "--list-all-pkgs"]
    if args.offline:
        trivy_cmd += ["--skip-db-update", "--offline-scan"]
    trivy_cmd += [f"/workspace/{variant}/requirements.txt"]
    metadata["steps"]["trivy_scan"] = run(trivy_cmd, trivy_path / "scan.log")
    if metadata["steps"]["trivy_scan"]["exit_code"] == 0:
        try:
            report = load_report(trivy_path / "results.json")
            if not report.get("Results") or not any(r.get("Packages") for r in report["Results"]):
                raise ValueError("Trivy não analisou os pacotes esperados")
            vulns = [v for r in report["Results"] for v in r.get("Vulnerabilities", [])]
            metadata["trivy_counts"] = dict(Counter(v["Severity"] for v in vulns))
            for fmt, filename in [("sarif", "results.sarif"), ("cyclonedx", "sbom.cdx.json")]:
                conversion = run(compose + ["trivy", "convert", "--format", fmt, "--output", f"/reports/trivy/{variant}/{filename}", f"/reports/trivy/{variant}/results.json"], trivy_path / f"{fmt}.log")
                metadata["steps"][f"trivy_{fmt}"] = conversion
                if conversion["exit_code"] != 0:
                    metadata["errors"].append(f"Falha na exportação Trivy {fmt}")
            metadata["steps"]["trivy_gate"] = run(compose + ["trivy", "convert", "--severity", "HIGH,CRITICAL", "--exit-code", "1", f"/reports/trivy/{variant}/results.json"], trivy_path / "gate.log")
            expected = 1 if any(v["Severity"] in ("HIGH", "CRITICAL") for v in vulns) else 0
            if metadata["steps"]["trivy_gate"]["exit_code"] != expected:
                metadata["errors"].append("Exit code Trivy incompatível com o relatório")
        except (OSError, ValueError, KeyError) as exc:
            metadata["errors"].append(f"Relatório Trivy inválido: {exc}")
    else:
        metadata["errors"].append("Falha na execução Trivy; consultar scan.log")

    metadata["steps"]["kics_scan"] = run(compose + ["kics", "scan", "-p", f"/workspace/{variant}/deployment.yaml", "--type", "Kubernetes", "--report-formats", "json,sarif", "--output-path", f"/reports/kics/{variant}", "--fail-on", "high,critical", "--no-progress", "--no-color"], kics_path / "scan.log")
    try:
        report = load_report(kics_path / "results.json")
        metadata["kics_counts"] = report["severity_counters"]
        if report.get("files_scanned", 0) < 1 or report.get("files_parsed", 0) < 1:
            raise ValueError("Nenhum manifesto analisado")
        if report.get("files_failed_to_scan", 0) or report.get("queries_failed_to_execute", 0):
            raise ValueError("KICS registrou falhas de análise")
        high = sum(metadata["kics_counts"].get(k, 0) for k in ("HIGH", "CRITICAL"))
        # Na versão fixada, código 50 significa bloqueio por resultados.
        expected = 50 if high else 0
        if metadata["steps"]["kics_scan"]["exit_code"] != expected:
            raise ValueError("Exit code KICS incompatível com relatório")
    except (OSError, ValueError, KeyError) as exc:
        metadata["errors"].append(f"Relatório KICS inválido: {exc}")

    blockers = sum(metadata.get(tool + "_counts", {}).get(sev, 0) for tool in ("trivy", "kics") for sev in ("HIGH", "CRITICAL"))
    metadata["blocking_findings"] = blockers
    metadata["exit_code"] = 2 if metadata["errors"] else (1 if blockers else 0)
    metadata["status"] = "ERROR" if metadata["errors"] else ("FAIL" if blockers else "PASS")
    metadata["policy"] = {"block": ["HIGH", "CRITICAL"], "suppressions": [], "trivy_severity_source": "vendor default"}
    metadata["inputs_sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT / "fixtures" / variant).glob("*"))}
    metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
    (gate_path / "summary.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{variant}: {metadata['status']} | bloqueantes HIGH/CRITICAL: {blockers}")
    print("Trivy:", metadata.get("trivy_counts", {}), "KICS:", metadata.get("kics_counts", {}))
    for error in metadata["errors"]:
        print("ERRO:", error)
    print("Evidências:", str(gate_path.relative_to(ROOT)))
    return metadata["exit_code"]


if __name__ == "__main__":
    sys.exit(main())

