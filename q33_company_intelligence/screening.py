"""Evidence-completeness gate; does not infer demand, scrape websites, or send outreach."""
from __future__ import annotations
import csv
import sys
from pathlib import Path

REQUIRED = ("company", "sector", "city", "source_url")
ISSUE_FIELDS = ("observed_issue", "issue_source_url", "issue_checked_date")
CONTACT_FIELDS = ("public_phone", "public_email")
def classify(row: dict[str, str]) -> tuple[str, list[str]]:
    missing = [k for k in REQUIRED if not (row.get(k) or "").strip()]
    if missing:
        return "HOLD_RESEARCH", [f"missing:{k}" for k in missing]
    contact = any((row.get(k) or "").strip() for k in CONTACT_FIELDS)
    if not contact:
        return "HOLD_RESEARCH", ["no_public_business_contact"]
    missing_issue = [k for k in ISSUE_FIELDS if not (row.get(k) or "").strip()]
    if missing_issue:
        return "HOLD_RESEARCH", [f"missing:{k}" for k in missing_issue]
    if not (row.get("contact_checked_date") or "").strip():
        return "HOLD_RESEARCH", ["contact_not_currently_verified"]
    return "READY_FOR_HUMAN_REVIEW", ["evidence_fields_present; human verification still required"]

def run(path: str) -> int:
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    counts = {"READY_FOR_HUMAN_REVIEW": 0, "HOLD_RESEARCH": 0}
    for row in rows:
        status, reasons = classify(row)
        counts[status] += 1
        print(f'{row.get("company", "(unnamed)")}: {status} — {"; ".join(reasons)}')
    print(f"SUMMARY: total={len(rows)} ready={counts['READY_FOR_HUMAN_REVIEW']} hold={counts['HOLD_RESEARCH']}")
    print("NOTE: readiness is a completeness gate, not proof of need, intent, or market validation.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python screening.py <prospects.csv>")
    raise SystemExit(run(sys.argv[1]))
