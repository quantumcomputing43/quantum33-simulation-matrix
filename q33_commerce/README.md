# Q33 Commerce Launch — V1

**Current status:** prospect research is prepared; commercial validation has not occurred.  
**Budget:** 0 MAD.  
**Mode:** Android/mobile-first; free tools only.

## What is built

- `contract.json`: frozen offer hypothesis, endpoint, constraints, and decision rules.
- `prospect_seeds.csv`: 20 businesses listed in the Moroccan Ministry of Tourism travel-agency directory. These are **unqualified prospect seeds**, not companies known to need or want our service.
- `screening.py`: deterministic data-quality/qualification gate; it does not predict demand or send messages.
- `tests/test_screening.py`: isolated unit tests for the qualification gate.
- `outreach_templates.md`: respectful, individually tailored outreach templates.

## Frozen initial offer hypothesis

A simple mobile-friendly service/catalog page with a clear WhatsApp contact action, up to two agreed languages, handover, and one correction round. No paid hosting, domain, booking/payment integration, maintenance, or promise of traffic/sales is included. Quote and scope must be agreed in writing before delivery.

## Required audit per prospect

1. Verify that the business and contact are current.
2. Inspect its current public digital presence.
3. Record one specific, observable digital issue and the URL where it was observed.
4. Decide whether the issue is within the frozen offer scope.
5. Only then mark it `READY_FOR_HUMAN_REVIEW`; a human must approve the contact.
6. Log the outreach and outcome, including no reply or refusal.

A directory listing alone never qualifies a prospect. Empty evidence must remain HOLD.

## Seven-day test

Start the clock only after the offer, scope, proposed price, target segment, and list of eligible prospects are frozen and the first outreach is sent. Use one-to-one, relevant contact; no bulk spam or automated messaging.

- **Primary endpoint:** at least one genuine payment from an unrelated customer for the defined pilot within seven calendar days.
- Secondary: qualified replies, calls, explicit rejection reasons, written pilot agreements, delivery hours, direct costs.
- Silence is recorded as silence; it is not interpreted as proof that the business has no need.
- If no payment occurs, report that the endpoint was not met for this test; do not claim the whole market has no demand.

## Simulation Matrix boundary

The current generic engine hard-codes `SyntheticAdapter` and the existing workflow accepts only `synthetic.contract` / `matrix.json`. Do not route this commercial case through that engine or change the generic engine to contain business assumptions. The isolated screening CLI is a **lead-qualification gate**, not an economic simulation, and cannot establish willingness to pay.

## Run locally (Python standard library)

From the repository root:

```bash
python -m unittest discover -s q33_commerce/tests -v
python -m q33_commerce.screening --leads q33_commerce/prospect_seeds.csv
```

GitHub Actions runs these same checks for changes to `q33_commerce/`.

## Evidence links

- Ministry of Tourism directory: https://mtaess.gov.ma/fr/annuaires/annuaire-des-agences-de-voyages/
- Souss-Massa Chamber of Commerce listings: https://ccis-agadir.ma/en/listing-category/agence-de-voyages/

Verify contact details and current digital presence before outreach; directories can be stale.
