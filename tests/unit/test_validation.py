import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "inventory"))

from generate_inventory import validate_record

class TestValidation(unittest.TestCase):
    def test_valid_record(self):
        valid_rec = {
            "name": "huggingface/transformers",
            "url": "https://github.com/huggingface/transformers",
            "stars": 168000,
            "category_id": 2,
            "architecture_workflow": "Model weights -> Tokenizer -> PyTorch inference pipeline"
        }
        errs = validate_record(valid_rec, 1)
        self.assertEqual(len(errs), 0, "Valid record should produce 0 errors")

    def test_invalid_name(self):
        bad_rec = {
            "name": "invalid_name_without_slash",
            "url": "https://github.com/bad",
            "stars": 100,
            "category_id": 1,
            "architecture_workflow": "A -> B"
        }
        errs = validate_record(bad_rec, 2)
        self.assertTrue(any("invalid name" in e for e in errs))

    def test_negative_stars(self):
        bad_rec = {
            "name": "owner/repo",
            "url": "https://github.com/owner/repo",
            "stars": -5,
            "category_id": 1,
            "architecture_workflow": "A -> B"
        }
        errs = validate_record(bad_rec, 3)
        self.assertTrue(any("negative" in e for e in errs))

if __name__ == "__main__":
    unittest.main()
