"""Regression tests for the synthetic infrastructure contract."""
import copy
import unittest
from pathlib import Path

from simulation_matrix.cases.synthetic import SyntheticAdapter, STAGES
from simulation_matrix.config import load_matrix
from simulation_matrix.contracts import StageResult
from simulation_matrix.engine import _validate_adapter_identity

ROOT = Path(__file__).resolve().parents[1]


class SyntheticContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_matrix(ROOT / "matrix.json")
        cls.adapter = SyntheticAdapter()
        cls.context = {"matrix": cls.matrix, "execution_identity": "test"}

    def test_every_registered_stage_passes_without_scientific_claim(self):
        self.assertEqual(set(self.matrix["pipeline"][i]["stage"] for i in range(len(self.matrix["pipeline"])), STAGES)
        for stage in sorted(STAGES):
            result = self.adapter.run_stage(stage, seed=42, context=self.context)
            self.assertIsInstance(result, StageResult)
            self.assertEqual(result.stage, stage)
            self.assertTrue(result.passed)
            self.assertFalse(result.details["scientific_experiment"])
            self.assertEqual(len(result.details["deterministic_digest"]), 64)

    def test_same_stage_and_seed_produce_same_digest(self):
        first = self.adapter.run_stage("ROBUSTNESS", seed=42, context=self.context)
        second = self.adapter.run_stage("ROBUSTNESS", seed=42, context=self.context)
        self.assertEqual(first.details["deterministic_digest"], second.details["deterministic_digest"])

    def test_unknown_stage_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported"):
            self.adapter.run_stage("MADE_UP_STAGE", seed=42, context=self.context)

    def test_wrong_seed_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "frozen matrix seed"):
            self.adapter.run_stage("FALSIFICATION", seed=43, context=self.context)

    def test_scientific_flag_cannot_be_enabled(self):
        bad = copy.deepcopy(self.matrix)
        bad["scientific_experiment"] = True
        with self.assertRaisesRegex(ValueError, "must not be marked"):
            self.adapter.run_stage("FALSIFICATION", seed=42, context={"matrix": bad})

    def test_duplicate_stage_fails_closed(self):
        bad = copy.deepcopy(self.matrix)
        bad["pipeline"].append(copy.deepcopy(bad["pipeline"][0]))
        with self.assertRaisesRegex(ValueError, "unique"):
            self.adapter.run_stage("FALSIFICATION", seed=42, context={"matrix": bad})

    def test_matrix_and_adapter_identity_must_match(self):
        bad = copy.deepcopy(self.matrix)
        bad["case_id"] = "other.case"
        with self.assertRaisesRegex(RuntimeError, "case_id mismatch"):
            _validate_adapter_identity(bad, self.adapter)

    def test_bad_adapter_result_shape_is_not_silently_accepted(self):
        class BadAdapter:
            case_id = "synthetic.contract"
            protocol_version = "test"
            def run_stage(self, stage, *, seed, context):
                return {"stage": stage, "passed": True}
        bad = BadAdapter()
        _validate_adapter_identity(self.matrix, bad)
        returned = bad.run_stage("FALSIFICATION", seed=42, context=self.context)
        self.assertFalse(isinstance(getattr(returned, "passed", None), bool))


if __name__ == "__main__":
    unittest.main()
