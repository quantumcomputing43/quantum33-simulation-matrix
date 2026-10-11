"""Deterministic infrastructure fixture; never a scientific experiment."""
from __future__ import annotations

import hashlib
import json

from simulation_matrix.contracts import StageResult

STAGES = {
    "FALSIFICATION",
    "ADVERSARIAL_STRESS",
    "IDENTIFIABILITY",
    "ROBUSTNESS",
    "SURVIVOR_CHECK",
}
REQUIRED_VALIDITY_RULES = {
    "no_post_hoc_thresholds",
    "no_post_hoc_hypothesis_changes",
    "no_result_based_stage_removal",
    "record_all_failures",
    "separate_infrastructure_failure_from_scientific_failure",
    "case_specific_science_must_not_modify_core_engine",
}


class SyntheticAdapter:
    case_id = "synthetic.contract"
    protocol_version = "1.1"

    @staticmethod
    def _digest(case_id: str, stage: str, seed: int, protocol_version: str) -> str:
        payload = json.dumps(
            {
                "case": case_id,
                "stage": stage,
                "seed": seed,
                "protocol_version": protocol_version,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def run_stage(self, stage: str, *, seed: int, context: dict) -> StageResult:
        if stage not in STAGES:
            raise ValueError(f"unsupported synthetic contract stage: {stage}")
        if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
            raise ValueError("seed must be a non-negative integer")
        if not isinstance(context, dict) or not isinstance(context.get("matrix"), dict):
            raise ValueError("context.matrix must be a dict")

        matrix = context["matrix"]
        if matrix.get("case_id") != self.case_id:
            raise ValueError("matrix case_id does not match synthetic adapter")
        if matrix.get("seed") != seed:
            raise ValueError("stage seed does not match frozen matrix seed")
        if matrix.get("scientific_experiment") is not False:
            raise ValueError("synthetic fixture must not be marked as a scientific experiment")

        pipeline = matrix.get("pipeline")
        if not isinstance(pipeline, list):
            raise ValueError("matrix.pipeline must be a list")
        names = [item.get("stage") for item in pipeline if isinstance(item, dict)]
        if len(names) != len(pipeline) or len(names) != len(set(names)):
            raise ValueError("matrix pipeline must contain unique, well-formed stages")
        if any(name not in STAGES for name in names) or "SURVIVOR_CHECK" not in names:
            raise ValueError("matrix pipeline contains unknown stages or omits SURVIVOR_CHECK")

        rules = matrix.get("validity_rules")
        if not isinstance(rules, dict) or any(rules.get(key) is not True for key in REQUIRED_VALIDITY_RULES):
            raise ValueError("all frozen validity rules must be explicitly true")

        digest_a = self._digest(self.case_id, stage, seed, self.protocol_version)
        digest_b = self._digest(self.case_id, stage, seed, self.protocol_version)
        if digest_a != digest_b:
            raise RuntimeError("deterministic fixture digest mismatch")

        return StageResult(
            stage=stage,
            status="PASS",
            passed=True,
            details={
                "fixture": True,
                "checks": [
                    "registered_case_and_seed",
                    "well_formed_unique_pipeline",
                    "frozen_validity_rules",
                    "repeatable_digest",
                ],
                "deterministic_digest": digest_a,
                "scientific_experiment": False,
            },
        )


def load_case() -> SyntheticAdapter:
    return SyntheticAdapter()
