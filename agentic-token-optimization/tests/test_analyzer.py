import unittest
import tempfile
import os
import sys

# Injeta src no sys.path para execução direta do arquivo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from token_router.core.analyzer import FileAnalyzer

class TestFileAnalyzer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.small_file = os.path.join(self.temp_dir.name, "small.txt")
        with open(self.small_file, "w") as f:
            f.write("line 1\nline 2\nline 3\n")

        self.large_file = os.path.join(self.temp_dir.name, "large.txt")
        with open(self.large_file, "w") as f:
            for i in range(400):
                f.write(f"content line {i}\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_count_lines_small(self):
        self.assertEqual(FileAnalyzer.count_lines(self.small_file), 3)

    def test_count_lines_large(self):
        self.assertEqual(FileAnalyzer.count_lines(self.large_file), 400)

    def test_count_lines_nonexistent(self):
        self.assertEqual(FileAnalyzer.count_lines("/path/does/not/exist.txt"), 0)

    def test_targeted_read_identification(self):
        # 20 linhas solicitadas em limiar de 350 -> targeted read válido
        self.assertTrue(FileAnalyzer.is_targeted_read(10, 30, threshold=350))
        # 400 linhas solicitadas em limiar de 350 -> não é targeted read
        self.assertFalse(FileAnalyzer.is_targeted_read(1, 401, threshold=350))
        # Parâmetros nulos
        self.assertFalse(FileAnalyzer.is_targeted_read(None, None, threshold=350))

    def test_package_to_xml(self):
        xml_payload, total_lines = FileAnalyzer.package_to_xml([self.small_file])
        self.assertIn('<file path="', xml_payload)
        self.assertIn('lines="3">', xml_payload)
        self.assertIn("line 1", xml_payload)
        self.assertEqual(total_lines, 3)

if __name__ == "__main__":
    unittest.main()
