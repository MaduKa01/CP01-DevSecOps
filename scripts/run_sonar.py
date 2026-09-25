#!/usr/bin/env python3
"""Analisa o código próprio e exporta issues/hotspots sem exportar credenciais."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time

from setup_sonar import request

ROOT = Path(__file__).resolve().parents[1]


def main():
    env = dict(line.split("=", 1) for line in (ROOT / ".env").read_text().splitlines() if "=" in line and not line.startswith("#"))
    password = env["SONAR_ADMIN_PASSWORD"]
    output = ROOT / "reports" / "sonarqube"
    output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    command = ["docker", "compose", "run", "--rm", "-T", "sonar-scanner"]
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output / "scan.log").write_text(result.stdout)
    if result.returncode:
        print("SonarScanner falhou; consultar reports/sonarqube/scan.log")
        return result.returncode
    deadline = time.monotonic() + 120
    while True:
        activity = request("/api/ce/component?component=cp01-devsecops-grupo2", password)
        if not activity.get("queue") and activity.get("current", {}).get("status") == "SUCCESS":
            break
        if activity.get("current", {}).get("status") in ("FAILED", "CANCELED") and not activity.get("queue"):
            raise RuntimeError("O processamento SonarQube não concluiu com sucesso")
        if time.monotonic() > deadline:
            raise RuntimeError("Tempo excedido esperando processamento SonarQube")
        time.sleep(2)
    api_queries = {
        "issues": "/api/issues/search?componentKeys=cp01-devsecops-grupo2&ps=500",
        "hotspots": "/api/hotspots/search?projectKey=cp01-devsecops-grupo2&ps=500",
        "measures": "/api/measures/component?component=cp01-devsecops-grupo2&metricKeys=ncloc,bugs,vulnerabilities,code_smells,security_hotspots",
        "quality-gate": "/api/qualitygates/project_status?projectKey=cp01-devsecops-grupo2",
    }
    summary = {"timestamp": datetime.now(timezone.utc).isoformat(), "command": command, "seconds": round(time.perf_counter() - started, 3), "scanner_exit_code": result.returncode, "compute_engine": activity}
    for name, endpoint in api_queries.items():
        data = request(endpoint, password)
        (output / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        if name in ("issues", "hotspots"):
            summary[name] = len(data.get(name, []))
            if name == "issues":
                summary["open_issues"] = sum(i.get("status") not in ("CLOSED", "RESOLVED") for i in data["issues"])
                summary["resolved_issues"] = summary["issues"] - summary["open_issues"]
            if data.get("paging", {}).get("total", summary[name]) > summary[name]:
                raise RuntimeError("Relatório paginado/truncado: ampliar exportação")
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(f"SonarQube: {summary['open_issues']} issues abertas, {summary['resolved_issues']} encerradas, {summary['hotspots']} hotspots. Tempo: {summary['seconds']}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
