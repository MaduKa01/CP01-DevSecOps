"""Regressões do gate: erro ou relatório antigo jamais podem produzir verde."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class GateSafetyTests(unittest.TestCase):
    def test_success_exit_without_fresh_reports_is_error(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "scripts").mkdir()
            shutil.copy(Path(__file__).with_name("run_scan.py"), root / "scripts/run_scan.py")
            for tool in ("trivy", "kics"):
                directory = root / "reports" / tool / "corrigido"
                directory.mkdir(parents=True)
                (directory / "results.json").write_text('{"stale": true}')
            bin_dir = root / "bin"
            bin_dir.mkdir()
            fake = bin_dir / "docker"
            fake.write_text("#!/bin/sh\nexit 0\n")
            fake.chmod(0o755)
            env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ["PATH"])
            result = subprocess.run([sys.executable, str(root / "scripts/run_scan.py"), "corrigido"], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            summary = json.loads((root / "reports/gate/corrigido/summary.json").read_text())
            self.assertEqual(summary["status"], "ERROR")
            self.assertEqual(len(summary["errors"]), 2)
            self.assertFalse((root / "reports/trivy/corrigido/results.json").exists())

    def test_invalid_variant_is_rejected_before_execution(self):
        result = subprocess.run([sys.executable, str(Path(__file__).with_name("run_scan.py")), "outside-scope"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
