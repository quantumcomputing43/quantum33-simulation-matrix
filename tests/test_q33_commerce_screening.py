import csv
import tempfile
import unittest
from pathlib import Path

from q33_commerce.screening import classify, screen_csv


class ScreeningTests(unittest.TestCase):
    def test_directory_listing_alone_is_not_qualified(self):
        row = {
            "company": "Example Travel",
            "public_listing_source": "https://example.com/directory",
            "digital_gap_evidence": "",
            "gap_source_url": "",
            "public_contact": "",
            "contact_verified_on": "",
        }
        status, reasons = classify(row)
        self.assertEqual(status, "HOLD_RESEARCH")
        self.assertTrue(any("digital issue" in reason for reason in reasons))
        self.assertTrue(any("contact" in reason for reason in reasons))

    def test_complete_evidence_only_reaches_human_review(self):
        row = {
            "company": "Example Travel",
            "public_listing_source": "https://example.com/directory",
            "digital_gap_evidence": "Services page has no visible contact action",
            "gap_source_url": "https://example.com/services",
            "public_contact": "business@example.com",
            "contact_verified_on": "2026-10-11",
        }
        status, _ = classify(row)
        self.assertEqual(status, "READY_FOR_HUMAN_REVIEW")

    def test_no_automatic_contact_or_demand_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "leads.csv"
            fields = [
                "company", "segment", "public_listing_source", "location",
                "public_contact", "contact_verified_on", "digital_gap_evidence",
                "gap_source_url", "buyer_signal", "outreach_status", "notes",
            ]
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow({
                    "company": "Example Travel",
                    "public_listing_source": "https://example.com/directory",
                    "location": "Agadir",
                    "outreach_status": "NOT_REVIEWED",
                })
            result = screen_csv(path)
        self.assertEqual(result["status"], "SCREENING_COMPLETE_NOT_MARKET_VALIDATION")
        self.assertFalse(result["market_validated"])
        self.assertEqual(result["paid_customers"], 0)
        self.assertFalse(result["results"][0]["automatic_contact_permitted"])
        self.assertEqual(result["held_for_research"], 1)

    def test_missing_schema_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text("company,notes\nExample,none\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                screen_csv(path)


if __name__ == "__main__":
    unittest.main()
