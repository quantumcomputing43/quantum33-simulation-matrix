import unittest
from q33_company_intelligence.screening import classify

class ScreeningTests(unittest.TestCase):
    def test_directory_seed_is_hold(self):
        row = {"company":"Example","sector":"travel","city":"Agadir","source_url":"https://example.org",
               "public_email":"hello@example.org"}
        status, reasons = classify(row)
        self.assertEqual(status, "HOLD_RESEARCH")
        self.assertTrue(any("observed_issue" in reason for reason in reasons))

    def test_missing_contact_is_hold(self):
        row = {"company":"Example","sector":"travel","city":"Agadir","source_url":"https://example.org",
               "observed_issue":"No inquiry link on service page","issue_source_url":"https://example.org/services",
               "issue_checked_date":"2026-10-11"}
        status, reasons = classify(row)
        self.assertEqual(status, "HOLD_RESEARCH")
        self.assertIn("no_public_business_contact", reasons)

    def test_complete_record_only_ready_for_human_review(self):
        row = {"company":"Example","sector":"travel","city":"Agadir","source_url":"https://example.org",
               "public_email":"hello@example.org","contact_checked_date":"2026-10-11",
               "observed_issue":"No inquiry link on service page","issue_source_url":"https://example.org/services",
               "issue_checked_date":"2026-10-11"}
        status, _ = classify(row)
        self.assertEqual(status, "READY_FOR_HUMAN_REVIEW")

if __name__ == "__main__":
    unittest.main()
