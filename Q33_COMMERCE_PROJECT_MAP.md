# Q33 Commerce project map

This note documents the two commercial-research folders in this repository. Both are isolated from the generic scientific Simulation Matrix engine.

## 1. `q33_commerce/` — 20-seed screening workflow

- Frozen offer and endpoint: `contract.json`
- Prospect list: `prospect_seeds.csv`
- Screening CLI: `python -m q33_commerce.screening --leads q33_commerce/prospect_seeds.csv`
- Tests: `python -m unittest discover -s q33_commerce/tests -v`
- CI: `.github/workflows/q33-commerce.yml`
- AgentMail operations and approval gate: `AGENTMAIL_OPERATIONS.md`

This is the broad initial seed list and deterministic evidence-completeness gate. AgentMail send-and-reply was smoke-tested with the project owner; no company outreach has been sent.

## 2. `q33_company_intelligence/` — detailed research dossiers

- Frozen research rules: `contract.json`
- Four starter records: `prospects.csv`
- Research method: `research_protocol.md`
- Dossier template: `dossier_template.json`
- Screening CLI: `python -m q33_company_intelligence.screening q33_company_intelligence/prospects.csv`
- Tests: `python -m unittest q33_company_intelligence.tests.test_screening -v`
- CI: `.github/workflows/q33-company-intelligence.yml`
- Evidence-qualified Bounty Tours audit: `audits/bounty_tours_public_audit_2026-10-11.json`
- Simulation Matrix validity preflight: `audits/bounty_tours_sm_preflight_2026-10-11.md` and `.json`

This folder stores richer evidence, unknowns, and human-review gates.

## Why these folders are not merged yet

They use different CSV schemas and different CLI contracts. A blind merge could discard fields or change qualification behavior. Keep both intact until a deliberate schema migration is implemented with tests.

## Current evidence status

- AgentMail inbox `veltrix@agentmail.to` sent a test message to the owner, and the owner's reply was observed in the inbox thread.
- No outreach has been sent to any company; no payment is recorded, and the seven-day paid-pilot window has not started.
- The Bounty Tours website has a retrieved suspension-page result, but the available crawl is not fresh enough to certify the live status on its own.
- Bounty Tours contact information is present in public directories, but has not been independently verified as current. It remains `HOLD_RESEARCH`.
- Real company outreach requires a current, source-backed issue/contact check and explicit owner approval of the exact recipient and message.
- Do not modify the generic Simulation Matrix engine to embed commercial assumptions.
