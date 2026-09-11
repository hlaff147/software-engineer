import unittest
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from token_router.workers.bulk_reader import BulkReaderWorker
from token_router.workers.code_writer import CodeWriterWorker

class TestWorkers(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ref_file = os.path.join(self.temp_dir.name, "ReferenceService.java")
        with open(self.ref_file, "w") as f:
            f.write("public class ReferenceService { public void test() {} }\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_bulk_reader_synthesis(self):
        worker = BulkReaderWorker(model_name="test-flash-model")
        result = worker.execute(
            question="Quais métodos existem?",
            file_paths=[self.ref_file],
            mock=True
        )
        self.assertIn("Processados 1 arquivos", result["summary"])
        self.assertIn("Quais métodos existem?", result["summary"])
        self.assertEqual(result["model_used"], "test-flash-model")

    def test_code_writer_disk_persistence(self):
        worker = CodeWriterWorker(model_name="test-flash-model")
        target_file = os.path.join(self.temp_dir.name, "TargetService.java")
        result = worker.execute(
            spec="Gerar serviço de validação",
            reference_path=self.ref_file,
            target_path=target_file,
            mock=True
        )
        self.assertTrue(result["written_to_disk"])
        self.assertTrue(os.path.exists(target_file))
        with open(target_file, "r") as f:
            saved_content = f.read()
        self.assertIn("GeneratedServiceStub", saved_content)
        self.assertFalse(saved_content.startswith("```"))

if __name__ == "__main__":
    unittest.main()
