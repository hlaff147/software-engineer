import unittest
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from token_router.core.config import RouterConfig
from token_router.core.router import TokenRouter

class TestTokenRouter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config = RouterConfig(line_threshold=100)
        self.router = TokenRouter(self.config)

        self.small_file = os.path.join(self.temp_dir.name, "small.py")
        with open(self.small_file, "w") as f:
            for i in range(50):
                f.write(f"print({i})\n")

        self.large_file = os.path.join(self.temp_dir.name, "large.py")
        with open(self.large_file, "w") as f:
            for i in range(200):
                f.write(f"print({i})\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_allow_small_file(self):
        decision = self.router.evaluate_read_request(self.small_file)
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.line_count, 50)

    def test_block_large_file(self):
        decision = self.router.evaluate_read_request(self.large_file)
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.line_count, 200)
        self.assertIn("Excedeu o limiar", decision.reason)
        self.assertIsNotNone(decision.recommendation)

    def test_allow_targeted_read_on_large_file(self):
        decision = self.router.evaluate_read_request(
            self.large_file, start_line=10, end_line=30
        )
        self.assertTrue(decision.allowed)
        self.assertIn("Targeted read permitido", decision.reason)

if __name__ == "__main__":
    unittest.main()
