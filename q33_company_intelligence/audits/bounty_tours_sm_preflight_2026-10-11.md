# Bounty Tours — Simulation Matrix preflight

**Date:** 2026-10-11  
**Decision:** `HOLD_RESEARCH`  
**Simulation execution:** `NOT_RUN` — blocked by input/adapter validity, not by a failed result.

## Result first

The strongest lead is a possible official-website availability problem, but the current evidence is not fresh enough to call it a live outage. The official-domain page returned a hosting-provider suspension template, while the available crawl is about three months old. The Chamber of Commerce directory was crawled recently, but the Bounty Tours entry itself is dated 2024-07-29. Charika also lists the business and contact details, but neither directory confirms that the contact details are currently working or that the company wants this problem fixed.

**We cannot responsibly select or deploy a fix yet.** A Simulation Matrix run cannot validate a live website condition that has not been freshly verified, and the documented generic Matrix fixture is not a company-specific remediation adapter.

## What the real fix depends on

- **If the official domain is still suspended:** the authorized domain/hosting administrator must resolve the suspension with the provider. VELTRIX cannot restore it from a standalone landing page, and must not access or change company accounts.
- **If the official site works but a mobile inquiry path is broken:** after Bounty Tours confirms the need, a small mobile-first service/contact page may fit the frozen zero-budget offer.
- **If the site and inquiry path work, or the company declines:** no build; record the negative/neutral result rather than inventing a problem.

## Frozen experiment question

> Conditional on a current, company-confirmed digital issue and approved inputs, which in-scope change improves completion of a clearly defined mobile inquiry task without introducing false claims, paid dependencies, or privileged access?

### Hypotheses and controls

- **H0 — null:** no current actionable problem is established; no build and no outreach.
- **H1 — current suspension confirmed:** route the owner to their authorized hosting/domain administrator. A temporary page is only considered if explicitly requested.
- **H2 — site reachable, mobile contact task fails:** compare the verified baseline against a company-approved mobile-first service/contact-page prototype.
- **H3 — journey works or company declines:** no intervention.

### Frozen technical endpoints

Primary: a visitor can reach a company-confirmed public inquiry route within three clear mobile actions, without mistaking the page for a confirmed booking or payment flow.

Secondary: approved service copy and contact details; mobile/narrow-screen and keyboard checks; no paid hosting, domain, API, booking or payment dependency.

**Not endpoints:** simulated bookings, revenue, traffic, or conversion uplift. Those require real measured data.

### Adversarial checks

- stale or broken contact route;
- CTA points to the wrong destination;
- mobile layout hides the inquiry action;
- unapproved prices, availability, claims, logos, or images;
- visitor confuses inquiry with a confirmed booking/payment;
- missing authorization to publish, host, or use company content.

Any unknown critical input fails closed. Seeds reserved for a future reproducible adapter: `42–46`; no run has been represented as completed.

## Audit gate and next operation

1. Open the official domain in a normal browser and record the live result and timestamp.
2. Independently verify one public business contact route; directory listing alone is insufficient.
3. Confirm with the company that the issue is current and that they want help.
4. Freeze the business-specific adapter, baseline/null, metric, pass/fail rules, inputs, and provenance.
5. Run Simulation Matrix adversarial and robustness tests, then review a prototype only if it passes.

No outreach has been sent. Any first company message still requires explicit approval of the exact recipient and message.

## Sources

- Official website: https://www.bounty-tours.com/ — retrieved suspension-page result; crawl age is about three months.
- Chamber of Commerce listing: https://ccis-agadir.ma/en/listing-category/agence-de-voyages/ — directory crawl recent, Bounty Tours record dated 2024-07-29.
- Charika record: https://www.charika.ma/societe-bounty-tours-134382 — corroborating directory, not direct contact verification.
- Generic project workflow: `README.md` and `Q33_COMMERCE_PROJECT_MAP.md`; commercial research remains isolated from the generic scientific engine.
