from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_corpus", ROOT / "scripts" / "validate_corpus.py")
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateCorpusTests(unittest.TestCase):
    def copy_data(self, target: Path) -> None:
        for source in (ROOT / "data").glob("*.json"):
            target.joinpath(source.name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def test_curated_dataset_is_valid(self) -> None:
        self.assertEqual(VALIDATOR.validate_dataset(ROOT / "data"), [])

    def test_aristophanes_cannot_be_relabelled_as_socrates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            self.copy_data(target)
            path = target / "myth_cards.json"
            cards = json.loads(path.read_text(encoding="utf-8"))
            changed = copy.deepcopy(cards)
            for card in changed:
                if card["id"] == "symposium-aristophanes":
                    card["speaker"] = "Socrates"
            path.write_text(json.dumps(changed, ensure_ascii=False), encoding="utf-8")
            errors = VALIDATOR.validate_dataset(target)
            self.assertTrue(any("divided humans" in error for error in errors))

    def test_atlantis_requires_archaeology_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            self.copy_data(target)
            path = target / "myth_cards.json"
            cards = json.loads(path.read_text(encoding="utf-8"))
            changed = copy.deepcopy(cards)
            for card in changed:
                if card["id"] == "timaeus-atlantis":
                    card["non_claims"].remove("not archaeological proof")
            path.write_text(json.dumps(changed, ensure_ascii=False), encoding="utf-8")
            errors = VALIDATOR.validate_dataset(target)
            self.assertTrue(any("Atlantis" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
