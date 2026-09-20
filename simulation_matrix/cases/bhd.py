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

REQUIRED_PROVENANCE_FIELDS = (
    "equations",
    "assumptions",
    "external_baselines",
)

BLOCKED_VALUES = {"TBD", "", None}

def _is_blocked(value) -> bool:
    return value in BLOCKED_VALUES or (isinstance(value, str) and not value.strip())

def _strict_object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise BHDProtocolIncomplete(f"Duplicate JSON key: {key}")
        result[key] = value
    return result

def load_protocol(path: Path) -> dict:
    try:
        data = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_strict_object_pairs,
        )
    except (json.JSONDecodeError, BHDProtocolIncomplete) as exc:
        raise BHDProtocolIncomplete(f"Invalid BHD protocol JSON: {exc}") from exc

    if data.get("protocol_version") != "BHD-P1.2":
        raise BHDProtocolIncomplete("Unsupported BHD protocol version.")
    if data.get("case_id") != "bhd.hidden_sector":
        raise BHDProtocolIncomplete("Unexpected BHD case id.")
    if data.get("scientific_experiment") is not False:
        raise BHDProtocolIncomplete("Phase 1 must not be marked as a scientific experiment.")
    if set(data.get("stages", {})) != set(REQUIRED_STAGES):
        raise BHDProtocolIncomplete("BHD protocol must define exactly the five required stages.")
    return data

def _audit_complete(protocol: dict) -> bool:
    audit = protocol.get("pre_experiment_audit", {})
    if any(_is_blocked(audit.get(field)) for field in REQUIRED_AUDIT_FIELDS):
        return False
    provenance = audit.get("provenance", {})
    if any(_is_blocked(provenance.get(field)) for field in REQUIRED_PROVENANCE_FIELDS):
        return False
    return True

def _stage_registration_complete(item: dict) -> bool:
    if item.get("pre_registered") is not True or _is_blocked(item.get("criterion")):
        return False
    required = item.get("required_inputs", [])
    registered = item.get("registered_inputs", {})
    if not isinstance(required, list) or not isinstance(registered, dict):
        return False
    return all(name in registered and not _is_blocked(registered[name]) for name in required)

def execution_ready(protocol: dict) -> bool:
    if protocol.get("execution_gate", {}).get("allow_scientific_execution") is not True:
        return False
    if not _audit_complete(protocol):
        return False

    scope = protocol.get("model_scope", {})
    if _is_blocked(scope.get("observable_signature")):
        return False

    stages = protocol.get("stages", {})
    return all(_stage_registration_complete(stages.get(stage, {})) for stage in REQUIRED_STAGES)

def assert_execution_ready(protocol: dict) -> None:
    if not execution_ready(protocol):
        raise BHDProtocolIncomplete(
            "BHD scientific execution is blocked: the protocol is not fully "
            "pre-registered and audited."
        )
