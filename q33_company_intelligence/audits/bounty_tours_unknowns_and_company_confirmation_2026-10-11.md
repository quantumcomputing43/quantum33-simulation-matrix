# Bounty Tours — Issue decomposition and confirmation register

**Date:** 2026-10-11  
**Status:** HOLD_RESEARCH / COMPANY-SPECIFIC SIMULATION NOT RUN  
**Purpose:** Separate public evidence, testable technical questions, and facts that only Bounty Tours can confirm. This is a planning/audit artifact, not a live DNS/TLS result and not proof of commercial benefit.

## 1. Current evidence and confidence

| Topic | Current evidence | Status | What would resolve it |
|---|---|---|---|
| Official website | Retrieved page showed a hosting suspension template, but the crawl was about three months old | STALE / NOT CURRENTLY VERIFIED | Open apex and www URLs directly and record UTC timestamp, redirect chain, status, and screenshot/text |
| DNS A/AAAA/NS | No direct resolver answer captured in this session | NOT VERIFIED | Query at least two independent DNS resolvers; save answer, TTL, timestamp |
| HTTPS/TLS | No direct handshake or certificate details captured | NOT VERIFIED | Test apex and www separately; capture TLS result, certificate validity dates, hostname match, chain |
| MX / SPF / DMARC | No direct DNS answers captured | NOT VERIFIED | Resolve MX, TXT SPF, _dmarc TXT; distinguish absent record from resolver/query failure |
| Domain registration / expiry | No current RDAP response captured | NOT VERIFIED | Retrieve current registrar, expiry, and status codes from RDAP |
| Public contact details | Directories list contacts, but currency and working status are unconfirmed | DIRECTORY-ONLY | Confirm through an independently sourced current route or with the company |
| Company need / authorization | No direct company confirmation | UNKNOWN | Ask whether the issue exists now and whether they want assistance |
| Commercial value | No actual task analytics, lead data, or booking data | UNKNOWN | Do not infer; define measurable baseline only if the company chooses to share data |

## 2. Frozen hypotheses (do not change after seeing results)

- **H0 — Null:** no current actionable issue is verified. Decision: no build, no outreach, preserve HOLD_RESEARCH.
- **H1 — Website/domain/hosting problem:** fresh evidence shows a current suspension or outage, and the company confirms it wants help. Decision: route account/domain recovery to the authorized owner/provider; do not access or change accounts.
- **H2 — Contact journey problem:** website is reachable, and a specific mobile inquiry task fails reproducibly. Decision: only with company approval, test a small prototype against the current baseline.
- **H3 — No actionable fit:** website/contact route works for the agreed task, or company declines. Decision: no intervention; record NOT_A_FIT.

## 3. Diagnostic scenarios and pass/fail rules

| Scenario | Evidence needed | Pass condition | Fail / stop condition |
|---|---|---|---|
| S1: stale crawl mistaken for live outage | Fresh direct browser check for apex and www | Current state recorded with timestamp and redirects | No fresh result: keep BLOCKED |
| S2: DNS fault | A, AAAA, NS answers from two resolvers | Consistent answers are recorded; discrepancy is explained | Resolver failure or inconsistent unexplained results: NOT VERIFIED |
| S3: TLS fault | Direct TLS/certificate check for apex and www | Valid chain, hostname match, and dates, or exact reproducible error | No handshake evidence: NOT VERIFIED |
| S4: mail routing/authentication fault | MX, SPF, DMARC DNS records | Each record is reported independently with lookup evidence | Missing evidence is not called a mail outage |
| S5: hosting suspension | Current HTTP status/redirect/page plus owner/provider confirmation | Current suspension confirmed by fresh evidence; owner knows provider is the remedy path | Page may be stale or provider reason unknown: no diagnosis of cause |
| S6: broken mobile inquiry flow | Company-approved task, device/viewport, current URL | A tester can reach the confirmed inquiry route within 3 clear actions, with no false booking/payment implication | Broken/stale CTA, unapproved claims, unclear destination, or missing authorization |
| S7: false commercial success | Real, consented baseline/outcome data if shared | Only report observed measurements with provenance | Never infer bookings, revenue, traffic, or conversion lift from simulation |

**Global rule:** unknown critical inputs fail closed. A passing generic infrastructure test is not a company-specific pass. Simulation cannot repair missing observations or identify a live cause from stale directory records.

## 4. Questions for Bounty Tours — hold until contact route is verified and user approves exact message

1. Is the official website currently under your control and intended to be active?
2. Are you currently experiencing a website, domain, hosting, email, or mobile contact problem? If yes, what exact symptom and since when?
3. Who is the authorized person/provider for the domain and hosting? We do not need passwords, recovery codes, or private account access.
4. Which public inquiry route should a visitor use today (phone, email, WhatsApp, or form), and which contact details/languages are approved for publication?
5. What is the one visitor task you most want to improve (e.g. request a tour, ask for information, or call the agency)?
6. Do you authorize a no-cost, non-production prototype for review only? This does not imply permission to publish, host, change DNS, or connect booking/payment systems.
7. Are there approved service descriptions, images/logos, and current prices/availability that may be used? If not, the prototype will omit them.
8. If you want outcome measurement, what non-sensitive baseline can you voluntarily share? No customer personal data or credentials are needed.

## 5. Required gate before company-specific Simulation Matrix execution

- [ ] Fresh website result with timestamp and redirect/status details
- [ ] Direct DNS/TLS/MX/SPF/DMARC/RDAP outputs or explicit per-check failure
- [ ] One independently verified public contact route
- [ ] Company confirms current issue and desired outcome
- [ ] Approved contact route, languages, content, and prototype scope
- [ ] Company-specific adapter/version/hash and frozen baseline, metric, null, pass/fail threshold, scenarios, seeds, and logs

Until every critical item is resolved: **HOLD_RESEARCH**. No company message is sent automatically; exact recipient and message require explicit user approval.
