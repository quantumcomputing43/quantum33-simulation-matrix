import json
import tempfile
import unittest
from pathlib import Path
from simulation_matrix.cases.bhd import (
    BHDProtocolIncomplete, assert_execution_ready, execution_ready, load_protocol
)

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "simulation_matrix" / "cases" / "bhd_protocol.json"

class BHDProtocolTests(unittest.TestCase):
    def test_phase1_protocol_is_not_executable(self):
        protocol = load_protocol(SOURCE)
        self.assertFalse(execution_ready(protocol))
        with self.assertRaises(BHDProtocolIncomplete):
            assert_execution_ready(protocol)

    def test_execution_gate_cannot_be_enabled_without_all_criteria(self):
        protocol = load_protocol(SOURCE)
        protocol["execution_gate"]["allow_scientific_execution"] = True
        self.assertFalse(execution_ready(protocol))

    def test_protocol_identity_is_explicit(self):
        protocol = load_protocol(SOURCE)
        self.assertEqual(protocol["case_id"], "bhd.hidden_sector")
        self.assertEqual(protocol["protocol_version"], "BHD-P1.3")

    def test_duplicate_json_keys_are_rejected(self):
        raw = SOURCE.read_text(encoding="utf-8").replace(
            '"case_id": "bhd.hidden_sector",',
            '"case_id": "bhd.hidden_sector",
  "case_id": "tampered",',
            1,
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as handle:
            handle.write(raw)
            handle.flush()
            with self.assertRaises(BHDProtocolIncomplete):
                load_protocol(Path(handle.name))

    def test_stage_registration_is_required(self):
        protocol = load_protocol(SOURCE)
        protocol["execution_gate"]["allow_scientific_execution"] = True
        protocol["pre_experiment_audit"] = {
            key: "registered" for key in (
                "primary_observable", "measurement_definition", "null_model_definition",
                "classical_nuisance_model", "parameter_domain", "simulation_domain",
                "units_and_normalization", "data_generation_rule",
                "independent_repetition_policy", "multiple_comparison_policy",
                "stopping_rule", "exclusion_rule", "missing_or_invalid_output_rule"
            )
        }
        protocol["pre_experiment_audit"]["provenance"] = {
            "equations": "registered",
            "assumptions": "registered",
            "external_baselines": "registered",
        }
        protocol["model_scope"]["observable_signature"] = "registered"
        for stage in protocol["stages"].values():
            stage["pre_registered"] = True
            stage["criterion"] = "registered"
            stage["registered_inputs"] = {
                name: "registered" for name in stage["required_inputs"]
            }
        self.assertTrue(execution_ready(protocol))

        del protocol["stages"]["FALSIFICATION"]["registered_inputs"]["falsification_threshold"]
        self.assertFalse(execution_ready(protocol))

    def test_observable_candidate_set_does_not_open_gate(self):
        protocol = load_protocol(SOURCE)
        self.assertEqual(protocol["observable_selection"]["status"], "CANDIDATE_SET_NOT_SELECTED")
        self.assertEqual(protocol["observable_selection"]["derivation_contract"], "simulation_matrix/cases/bhd_observable_derivation.md")
        self.assertEqual(protocol["model_scope"]["observable_signature"], "TBD")
        self.assertFalse(execution_ready(protocol))

if __name__ == "__main__":
    unittest.main()
