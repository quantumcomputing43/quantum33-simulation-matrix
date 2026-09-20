"""BHD Phase 1 protocol boundary and execution gate."""
from __future__ import annotations
import json
from pathlib import Path

class BHDProtocolIncomplete(RuntimeError):
    """Raised when the BHD protocol is not yet executable."""

REQUIRED_STAGES = (
    "FALSIFICATION",
    "ADVERSARIAL_STRESS",
    "IDENTIFIABILITY",
    "ROBUSTNESS",
    "SURVIVOR_CHECK",
)

REQUIRED_AUDIT_FIELDS = (
    "primary_observable",
    "measurement_definition",
    "null_model_definition",
    "classical_nuisance_model",
    "parameter_domain",
    "simulation_domain",
    "units_and_normalization",
    "data_generation_rule",
    "independent_repetition_policy",
    "multiple_comparison_policy",
    "stopping_rule",
    "exclusion_rule",
    "missing_or_invalid_output_rule",
)

BLOCKED_VALUES = {"TBD", "", None}

def load_protocol(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("protocol_version") != "BHD-P1.1":
        raise BHDProtocolIncomplete("Unsupported BHD protocol version.")
    if data.get("case_id") != "bhd.hidden_sector":
        raise BHDProtocolIncomplete("Unexpected BHD case id.")
    if data.get("scientific_experiment") is not False:
        raise BHDProtocolIncomplete("Phase 1 must not be marked as a scientific experiment.")
    return data

def _audit_complete(protocol: dict) -> bool:
    audit = protocol.get("pre_experiment_audit", {})
    return all(audit.get(field) not in BLOCKED_VALUES for field in REQUIRED_AUDIT_FIELDS)

def execution_ready(protocol: dict) -> bool:
    if protocol.get("execution_gate", {}).get("allow_scientific_execution") is not True:
        return False
    if not _audit_complete(protocol):
        return False

    scope = protocol.get("model_scope", {})
    observable = scope.get("observable_signature")
    if observable in BLOCKED_VALUES:
        return False

    stages = protocol.get("stages", {})
    for stage in REQUIRED_STAGES:
        item = stages.get(stage, {})
        if item.get("pre_registered") is not True:
            return False
        if item.get("criterion") in BLOCKED_VALUES:
            return False
        if any(item.get("required_inputs", []).__contains__(x) for x in []):
            return False

    return True

def assert_execution_ready(protocol: dict) -> None:
    if not execution_ready(protocol):
        raise BHDProtocolIncomplete(
            "BHD scientific execution is blocked: the protocol is not fully "
            "pre-registered and audited."
        )
