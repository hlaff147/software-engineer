"""
Testes de ponta a ponta para a CLI do token-router.
"""

import unittest
import tempfile
import os
import subprocess
import sys

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.small_file = os.path.join(self.temp_dir.name, "small.txt")
        with open(self.small_file, "w") as f:
            for i in range(20):
                f.write(f"line {i}\n")

        self.large_file = os.path.join(self.temp_dir.name, "large.txt")
        with open(self.large_file, "w") as f:
            for i in range(500):
                f.write(f"line {i}\n")

        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.env = os.environ.copy()
        self.env["PYTHONPATH"] = os.path.join(self.root_dir, "src")

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cli(self, args):
        cmd = [sys.executable, "-m", "token_router.cli"] + args
        return subprocess.run(cmd, env=self.env, capture_output=True, text=True)

    def test_cli_check_small_file_passes(self):
        res = self.run_cli(["check", self.small_file])
        self.assertEqual(res.returncode, 0)

    def test_cli_check_large_file_blocks(self):
        res = self.run_cli(["check", self.large_file])
        self.assertEqual(res.returncode, 1)
        self.assertIn("BLOQUEIO PRE-TOOL", res.stderr)

    def test_cli_check_targeted_read_passes(self):
        res = self.run_cli(["check", self.large_file, "--start-line", "10", "--end-line", "30"])
        self.assertEqual(res.returncode, 0)

    def test_cli_read_command(self):
        res = self.run_cli(["read", "--question", "Qual o resumo?", "--paths", self.small_file])
        self.assertEqual(res.returncode, 0)
        self.assertIn("Processados 1 arquivos", res.stdout)

    def test_cli_write_command(self):
        target = os.path.join(self.temp_dir.name, "Out.java")
        res = self.run_cli([
            "write",
            "--spec", "Test spec",
            "--reference", self.small_file,
            "--target", target
        ])
        self.assertEqual(res.returncode, 0)
        self.assertTrue(os.path.exists(target))

if __name__ == "__main__":
    unittest.main()
