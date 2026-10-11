# Q33 Company Intelligence & Deal Finder — V1

**Project:** `Q33_COMMERCE_LAUNCH`  
**Status:** research workflow scaffold; no customer need or market demand validated.  
**Budget:** 0 MAD. Mobile-first, free tools only.

## Goal
Find a real, evidence-backed business problem before building anything. Research one company at a time, verify public business information, document a specific digital friction, identify a public professional contact route, and propose a narrowly scoped paid pilot.

## Initial market
Agadir / Souss-Massa travel agencies and small tourism operators. Four starting leads are in `prospects.csv`; these are seeds, not qualified buyers.

## Workflow
1. Verify the company is currently operating and record dated public sources.
2. Map its business, services, target customers and channels.
3. Inspect the public customer journey: mobile website, service details, contact, inquiry/quote flow, languages, booking instructions and social links.
4. Record only observable issues. Separate **observed fact**, **inference**, and **unknown**. Directory presence alone is not evidence of need.
5. Describe the likely business impact as a hypothesis, not a fact.
6. Check whether the issue can be solved inside the zero-budget offer. Do not promise traffic, leads or sales.
7. Find a public business contact route and, only if publicly listed, a relevant professional decision-maker.
8. Score evidence completeness with `screening.py`; the script never proves willingness to pay.
9. Human-review the tailored message; contact one business at a time. No bulk spam or automatic sending.
10. Record all replies, refusals, silence, scope, price, agreement and payment evidence.

## Files
- `contract.json`: frozen rules, scope, endpoint and decision gates.
- `prospects.csv`: four initial leads; their contact details are directory-sourced and need rechecking.
- `dossier_template.json`: standard per-company research dossier.
- `research_protocol.md`: evidence and privacy rules.
- `outreach_templates.md`: honest first-contact templates.
- `screening.py`: deterministic completeness gate; no scraping or sending.
- `tests/test_screening.py`: unit tests.

## Run on phone or computer
Python 3.10+:
```bash
python -m q33_company_intelligence.screening q33_company_intelligence/prospects.csv
python -m unittest discover -s q33_company_intelligence/tests -v
```
If running from the repository root, use the paths shown. The screening tool uses only the local CSV and Python standard library.

## Frozen commercial endpoint
A real unrelated business pays for the defined pilot within seven calendar days after the first valid outreach. The window has **not** started yet. Do not count replies, simulations, directory entries or verbal interest as a paid deal.

## Current state
Seed list only. No company has a verified digital problem in this dataset; no messages have been sent; no customer or revenue is validated.
