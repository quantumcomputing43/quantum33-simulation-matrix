import json,tempfile,unittest
from pathlib import Path
from simulation_matrix.config import ConfigError,load_matrix
from simulation_matrix.engine import run

class MatrixTests(unittest.TestCase):
    def test_duplicate_keys_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"matrix.json"; p.write_text('{"a":1,"a":2}',encoding="utf-8")
            with self.assertRaises(ConfigError): load_matrix(p)

    def _copy_matrix(self,root):
        src=Path(__file__).parents[1]/"simulation_matrix"/"matrix.json"
        (root/"matrix.json").write_text(src.read_text(encoding="utf-8"),encoding="utf-8")

    def test_pipeline_result_and_resume_is_project_local(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self._copy_matrix(root)
            first=run(root,project_id="PROJECT_A",matrix_path=root/"matrix.json")
            second=run(root,project_id="PROJECT_A",matrix_path=root/"matrix.json")
            self.assertEqual(first["status"],"RESULT")
            self.assertTrue(second["resumed"])
            self.assertEqual(second["project_id"],"PROJECT_A")

    def test_two_projects_do_not_share_checkpoint_or_log(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self._copy_matrix(root)
            a=run(root,project_id="BHD",matrix_path=root/"matrix.json")
            b=run(root,project_id="miRNA21",matrix_path=root/"matrix.json")
            self.assertEqual(a["status"],"RESULT")
            self.assertEqual(b["status"],"RESULT")
            self.assertNotEqual(a["execution_identity"],b["execution_identity"])
            self.assertTrue((root/"state"/"BHD"/"checkpoint_V2.1.json").is_file())
            self.assertTrue((root/"state"/"miRNA21"/"checkpoint_V2.1.json").is_file())
            self.assertTrue((root/"logs"/"BHD"/"matrix_V2.1.jsonl").is_file())
            self.assertTrue((root/"logs"/"miRNA21"/"matrix_V2.1.jsonl").is_file())

    def test_project_id_is_required_and_path_safe(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self._copy_matrix(root)
            with self.assertRaises(TypeError): run(root,matrix_path=root/"matrix.json")
            for bad in ("../BHD","BHD/../miRNA21",""):
                with self.assertRaises(ConfigError): run(root,project_id=bad,matrix_path=root/"matrix.json")

    def test_incompatible_checkpoint_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self._copy_matrix(root)
            run(root,project_id="PROJECT_A",matrix_path=root/"matrix.json")
            p=root/"state"/"PROJECT_A"/"checkpoint_V2.1.json"
            saved=json.loads(p.read_text(encoding="utf-8")); saved["execution_identity"]="incompatible"
            p.write_text(json.dumps(saved),encoding="utf-8")
            with self.assertRaises(RuntimeError): run(root,project_id="PROJECT_A",matrix_path=root/"matrix.json")
            self.assertEqual(json.loads(p.read_text(encoding="utf-8"))["execution_identity"],"incompatible")

if __name__=="__main__": unittest.main()
