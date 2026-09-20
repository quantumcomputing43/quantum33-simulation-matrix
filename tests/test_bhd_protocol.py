import unittest
from pathlib import Path
from simulation_matrix.cases.bhd import (
    BHDProtocolIncomplete, assert_execution_ready, execution_ready, load_protocol
)

class BHDProtocolTests(unittest.TestCase):
    def test_phase1_protocol_is_not_executable(self):
        source = Path(__file__).parents[1] / "simulation_matrix" / "cases" / "bhd_protocol.json"
        protocol = load_protocol(source)
        self.assertFalse(execution_ready(protocol))
        with self.assertRaises(BHDProtocolIncomplete):
            assert_execution_ready(protocol)

    def test_execution_gate_cannot_be_enabled_without_all_criteria(self):
        source = Path(__file__).parents[1] / "simulation_matrix" / "cases" / "bhd_protocol.json"
        protocol = load_protocol(source)
        protocol["execution_gate"]["allow_scientific_execution"] = True
        self.assertFalse(execution_ready(protocol))

    def test_protocol_identity_is_explicit(self):
        source = Path(__file__).parents[1] / "simulation_matrix" / "cases" / "bhd_protocol.json"
        protocol = load_protocol(source)
        self.assertEqual(protocol["case_id"], "bhd.hidden_sector")
        self.assertEqual(protocol["protocol_version"], "BHD-P1.1")

if __name__ == "__main__":
    unittest.main()
