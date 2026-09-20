"""BHD Phase 1 protocol boundary."""
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

def load_protocol(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("protocol_version") != "BHD-P1.0":
        raise BHDProtocolIncomplete("Unsupported BHD protocol version.")
    if data.get("case_id") != "bhd.hidden_sector":
        raise BHDProtocolIncomplete("Unexpected BHD case id.")
    if data.get("scientific_experiment") is not False:
        raise BHDProtocolIncomplete("Phase 1 must not be marked as a scientific experiment.")
    return data

def execution_ready(protocol: dict) -> bool:
    if protocol.get("execution_gate", {}).get("allow_scientific_execution") is not True:
        return False
    stages = protocol.get("stages", {})
    for stage in REQUIRED_STAGES:
        item = stages.get(stage, {})
        if item.get("pre_registered") is not True:
            return False
        if not item.get("criterion") or item["criterion"] == "TBD":
            return False
    observable = protocol.get("model_scope", {}).get("observable_signature")
    if not observable or observable == "TBD":
        return False
    return True

def assert_execution_ready(protocol: dict) -> None:
    if not execution_ready(protocol):
        raise BHDProtocolIncomplete(
            "BHD Phase 1 is protocol-only: scientific execution is blocked until "
            "the observable and all five stage criteria are pre-registered."
        )
