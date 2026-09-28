#!/usr/bin/env python3
"""Executa somente o template local em dois serviços do projeto."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    metadata = {"started_at": datetime.now(timezone.utc).isoformat(), "scope": "Containers locais app-vulneravel e app-corrigido; um template próprio", "runs": []}
    failed = False
    for variant in ("vulneravel", "corrigido"):
        path = ROOT / "reports" / "nuclei" / variant
        path.mkdir(parents=True, exist_ok=True)
        output = path / "results.jsonl"
        output.unlink(missing_ok=True)
        command = ["docker", "compose", "run", "--rm", "-T", "nuclei", "-u", f"http://app-{variant}:8080", "-t", "/templates/debug-exposure.yaml", "-duc", "-ni", "-jsonl-export", f"/reports/nuclei/{variant}/results.jsonl", "-no-color", "-stats"]
        print(f"Iniciando Nuclei: cenário {variant} (template local)...", flush=True)
        started = time.perf_counter()
        result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elapsed = round(time.perf_counter() - started, 3)
        (path / "scan.log").write_text(result.stdout, encoding="utf-8")
        findings = [json.loads(line) for line in output.read_text().splitlines() if line.strip()] if output.exists() else []
        expected = 1 if variant == "vulneravel" else 0
        # Um relatório vazio sem execução comprovada não conta como sucesso.
        valid = result.returncode == 0 and output.exists() and "Templates loaded for current scan: 1" in result.stdout and "Errors: 0" in result.stdout and "Requests: 1/1 (100%)" in result.stdout and "[ERR]" not in result.stdout and len(findings) == expected
        metadata["runs"].append({"variant": variant, "command": command, "seconds": elapsed, "exit_code": result.returncode, "matches": len(findings), "expected_matches": expected, "validated": valid})
        failed |= not valid
        print(f"Nuclei {variant}: {len(findings)} achados; validação={'OK' if valid else 'FALHA'}; {elapsed}s", flush=True)
    (ROOT / "reports" / "nuclei" / "summary.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
