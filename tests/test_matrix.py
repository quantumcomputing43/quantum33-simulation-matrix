import json,tempfile,unittest
from pathlib import Path
from simulation_matrix.config import ConfigError,load_matrix
from simulation_matrix.engine import run

class MatrixTests(unittest.TestCase):
    def test_duplicate_keys_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"matrix.json"; p.write_text('{"a":1,"a":2}',encoding="utf-8")
            with self.assertRaises(ConfigError): load_matrix(p)

    def test_pipeline_result_and_resume(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"simulation_matrix"; root.mkdir()
            src=Path(__file__).parents[1]/"simulation_matrix"/"matrix.json"
            (root/"matrix.json").write_text(src.read_text(encoding="utf-8"),encoding="utf-8")
            first=run(root); second=run(root)
            self.assertEqual(first["status"],"RESULT")
            self.assertTrue(second["resumed"])
            self.assertEqual([x["stage"] for x in second["stages"]],
                ["FALSIFICATION","ADVERSARIAL_STRESS","IDENTIFIABILITY","ROBUSTNESS","SURVIVOR_CHECK"])

    def test_incompatible_checkpoint_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"simulation_matrix"; root.mkdir()
            src=Path(__file__).parents[1]/"simulation_matrix"/"matrix.json"
            (root/"matrix.json").write_text(src.read_text(encoding="utf-8"),encoding="utf-8")
            run(root)
            p=root/"state"/"checkpoint_V2.0.json"
            saved=json.loads(p.read_text(encoding="utf-8")); saved["execution_identity"]="incompatible"
            p.write_text(json.dumps(saved),encoding="utf-8")
            with self.assertRaises(RuntimeError): run(root)
            self.assertEqual(json.loads(p.read_text(encoding="utf-8"))["execution_identity"],"incompatible")

if __name__=="__main__": unittest.main()
