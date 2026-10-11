"""Deterministic lead qualification gate; never a market-demand simulator."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REQUIRED_COLUMNS = {
    "company",
    "public_listing_source",
    "digital_gap_evidence",
    "gap_source_url",
    "outreach_status",
}
QUALIFIED_STATUS = "READY_FOR_HUMAN_REVIEW"


def classify(row: dict[str, str]) -> tuple[str, list[str]]:
    """Classify only evidence completeness; do not infer buyer intent."""
    reasons: list[str] = []
    company = (row.get("company") or "").strip()
    listing = (row.get("public_listing_source") or "").strip()
    gap = (row.get("digital_gap_evidence") or "").strip()
    gap_url = (row.get("gap_source_url") or "").strip()
    contact = (row.get("public_contact") or "").strip()
    verified = (row.get("contact_verified_on") or "").strip()

    if not company:
        reasons.append("missing company name")
    if not listing:
        reasons.append("missing public listing source")
    if not gap:
        reasons.append("no specific observed digital issue")
    if not gap_url:
        reasons.append("no source URL for observed issue")
    if not contact:
        reasons.append("no current public business contact recorded")
    if not verified:
        reasons.append("contact freshness not verified")

    if reasons:
        return "HOLD_RESEARCH", reasons
    return QUALIFIED_STATUS, ["evidence fields complete; human review still required"]


def screen_csv(path: Path) -> dict:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
        rows = list(reader)

    results = []
    for row in rows:
        status, reasons = classify(row)
        results.append({
            "company": (row.get("company") or "").strip(),
            "status": status,
            "reasons": reasons,
            "buyer_intent_established": False,
            "automatic_contact_permitted": False,
        })

    return {
        "project_id": "Q33_COMMERCE_LAUNCH",
        "case_id": "ZERO_BUDGET_DIGITAL_BUSINESS_SCREEN",
        "protocol_version": "Q33-COMMERCE-V1",
        "status": "SCREENING_COMPLETE_NOT_MARKET_VALIDATION",
        "lead_count": len(results),
        "ready_for_human_review": sum(x["status"] == QUALIFIED_STATUS for x in results),
        "held_for_research": sum(x["status"] == "HOLD_RESEARCH" for x in results),
        "paid_customers": 0,
        "market_validated": False,
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leads", type=Path, required=True)
    parser.add_argument("--json", action="store_true", help="Print full JSON output")
    args = parser.parse_args()
    result = screen_csv(args.leads)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Status: {result['status']}")
        print(f"Prospect seeds: {result['lead_count']}")
        print(f"Ready for human review: {result['ready_for_human_review']}")
        print(f"Held for research: {result['held_for_research']}")
        print("Market validated: no")
        for item in result["results"]:
            print(f"- {item['company']}: {item['status']} — {'; '.join(item['reasons'])}")


if __name__ == "__main__":
    main()
