"""Regressões do gate: erro ou relatório antigo jamais podem produzir verde."""
import json
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


class GateSafetyTests(unittest.TestCase):
    def test_success_exit_without_fresh_reports_is_error(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "scripts").mkdir()
            run_scan_path = root / "scripts/run_scan.py"
            shutil.copy(Path(__file__).with_name("run_scan.py"), run_scan_path)
            for tool in ("trivy", "kics"):
                directory = root / "reports" / tool / "corrigido"
                directory.mkdir(parents=True)
                (directory / "results.json").write_text('{"stale": true}')
            spec = importlib.util.spec_from_file_location("run_scan_under_test", run_scan_path)
            run_scan = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_scan)
            successful_command = {"exit_code": 0, "seconds": 0.0}
            with mock.patch.object(sys, "argv", [str(run_scan_path), "corrigido"]), mock.patch.object(
                run_scan, "run", return_value=successful_command
            ):
                result = run_scan.main()
            self.assertEqual(result, 2)
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
