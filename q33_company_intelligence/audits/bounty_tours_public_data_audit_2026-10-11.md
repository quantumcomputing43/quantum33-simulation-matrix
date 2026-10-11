# Bounty Tours — public-data audit v1
**Audit date:** 2026-10-11  
**Scope:** Public website/search-index content, public business directories, Moroccan Ministry of Tourism agency list, and public company-record metadata.  
**Status:** PRELIMINARY FINDINGS — LIVE TECHNICAL AND FINANCIAL VERIFICATION INCOMPLETE

## Executive result
The strongest actionable lead is a website/hosting availability failure: the official domain resolves in the available browser retrieval to a hosting-provider suspension page. The page names Heberdomaine and lists two possible suspension categories (invoice/payment or terms-of-service issue), but does not establish which applies. Search-indexed site pages also expose stale 2015–2016 booking/rate messaging. These create a plausible digital-service and trust problem, but do not prove the business is closed, the domain has expired, DNS is misconfigured, email is down, bookings are being lost, or the company has a current financial problem.

## Evidence register

| ID | Observation | Source | Confidence / limitation |
|---|---|---|---|
| E1 | Official domain redirects in available retrieval to /cgi-sys/suspendedpage.cgi; page says the site is suspended and identifies Heberdomaine. It lists payment/invoice and terms-of-service as possible reasons. | https://www.bounty-tours.com/ | Strong evidence of a suspension page in retrieved content; not a timestamped independent HTTP/DNS probe. Actual reason is unknown. |
| E2 | Search-indexed official-domain pages advertise a hotel booking service and include “New Rates 2015–2016” messaging. | https://www.bounty-tours.com/auth/login?redirect=%2Fhotels%2Flistrooms%2Fcity%2Fagadir%2Fcountry%2Fmorocco%2Fidhotel%2F2%2Fhotel%2F2-agadir-agadir-beach-club and https://www.bounty-tours.com/hotels/detail/id/8 | Strong evidence old content remains indexed; not proof the live database or every page is old. |
| E3 | Ministry of Tourism public ODV list includes “STE BOUNTY TOURS SARL” in Agadir at Avenue des FAR / Immeuble My Cherif. | https://mtaess.gov.ma/fr/annuaires/annuaire-des-agences-de-voyages/organisateurs-distributeurs-de-voyages/ | Official directory listing; does not establish current trading activity or financial health. |
| E4 | Chamber of Commerce Souss-Massa directory lists Bounty Tours, telephone +212 528 82 77 11 and emails bountytours@menara.ma and operations@bounty-tours.com; record date shown is 29 July 2024. | https://ccis-agadir.ma/en/listing-category/agence-de-voyages/ | Contact routes not independently verified as working today. |
| E5 | Charika lists the business as a SARL, capital MAD 3,200,000, contact details, representatives, and a judicial reorganisation procedure opened in 2012 and closed in 2018. It indicates financial statements are available for 2020, 2021 and 2023. | https://www.charika.ma/societe-bounty-tours-134382 | Secondary company-information source. Actual accounts were not retrieved or audited here; old judicial history is not evidence of current distress. |
| E6 | A public social-directory mirror contains Bounty Tours promotional posts from 2023 and 2024, including Umrah offers and mobile numbers. | https://www.findglocal.com/MA/Agadir/107301565083765/Bounty-Tours---بونتي-تورز | Historical, mirrored social content; does not prove current activity or working contacts. |
| E7 | Another directory associates the company with a named contact and a Gmail address, while other sources list different emails and numbers. | https://www.africabizinfo.com/ar-MA/bounty-tours_1z | Potential contact-data inconsistency; directory-only evidence, not proof that any listed details are wrong. |

## Preliminary issue register (ranked by evidence, not severity)

1. **P1 — Public website appears suspended.** Confirm live status using a fresh independent browser/network check. If still suspended, the authorized hosting/domain administrator must obtain the provider's actual reason and restore service. Do not assume non-payment or terms violation without confirmation.
2. **P1 — Booking/service information may be stale.** Search-indexed pages show 2015–2016 rates. Once the site is restored or a company-approved copy is available, check whether live rate/availability pages, login, booking, and contact journeys expose obsolete or misleading information.
3. **P2 — Email and phone contact routes may be stale or inconsistent.** Several directories list different mailboxes/numbers. Test only public business channels in a non-invasive manner, or ask the company to confirm canonical contacts. Do not send bulk messages or treat directory records as verified.
4. **P2 — Company status and website status are not the same question.** The Ministry directory lists the entity, but this does not establish current operations, current licensing details, or financial status. Confirm directly through authorized public/official channels before making claims.
5. **P3 — Financial risk is unassessed.** Charika advertises financial statements for 2020, 2021 and 2023, but actual figures were not accessed. No conclusion about profitability, solvency, debt, or current distress is supportable from the profile alone.
6. **P3 — Digital trust/maintenance risk.** Old indexed content and a suspension template can undermine confidence. This is a plausible customer-experience issue, not measured evidence of lost bookings or revenue.

## Required technical checks not completed
- Fresh HTTP/HTTPS status and redirect chain from more than one network.
- DNS A/AAAA/CNAME/NS/MX/TXT records, nameserver consistency, and registrar/domain-expiry status from authoritative sources.
- TLS certificate chain/expiry and HTTP-to-HTTPS behavior.
- Whether the business email domain accepts mail and whether MX is functional.
- Live mobile booking/contact journey and current rate/availability data.
- Actual financial statements, current licence details, and company confirmation of operating status.

These checks require current technical lookups and/or authorized company/registrar/provider information. Search snippets and cached pages are not substitutes.

## Simulation Matrix gate
**Company-specific simulation: NOT RUN.** No validated company-specific adapter, verified baseline, or company-approved requirements/data are available. A simulation cannot determine real DNS/hosting status or infer business revenue from public snippets. After live facts are collected, freeze the baseline, null/control, scenarios, endpoints, pass/fail rules, seeds, code hash and provenance before running adversarial/robustness tests.

## Safe next actions
1. Obtain a fresh live check of the official domain and independently verify DNS, TLS, MX, and registrar status using public read-only lookups.
2. Ask the hosting provider or the company's authorized administrator to confirm the actual suspension reason; do not attempt account access or configuration changes.
3. Confirm the canonical business email/phone and whether the company wants assistance.
4. Retrieve actual company accounts only from a lawful/public or authorized source before doing financial analysis.
5. Build a company-specific Matrix adapter only after the above inputs are verified and frozen.

**No company outreach, website modification, domain/DNS change, or account access was performed for this audit.**

## Sources
- Official website/suspension response: https://www.bounty-tours.com/
- Official-domain indexed booking/login content: https://www.bounty-tours.com/auth/login?redirect=%2Fhotels%2Flistrooms%2Fcity%2Fagadir%2Fcountry%2Fmorocco%2Fidhotel%2F2%2Fhotel%2F2-agadir-agadir-beach-club
- Moroccan Ministry of Tourism ODV directory: https://mtaess.gov.ma/fr/annuaires/annuaire-des-agences-de-voyages/organisateurs-distributeurs-de-voyages/
- Chamber of Commerce Souss-Massa directory: https://ccis-agadir.ma/en/listing-category/agence-de-voyages/
- Charika company profile: https://www.charika.ma/societe-bounty-tours-134382
- Social-directory mirror: https://www.findglocal.com/MA/Agadir/107301565083765/Bounty-Tours---بونتي-تورز
- AfricaBizInfo directory: https://www.africabizinfo.com/ar-MA/bounty-tours_1z
