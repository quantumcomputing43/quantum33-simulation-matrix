# Bounty Tours — DNS / TLS / MX audit run record
**Requested run date:** 2026-10-11  
**Target:** bounty-tours.com and www.bounty-tours.com  
**Run status:** PARTIAL — live record queries could not be completed through the available retrieval interface.  
**Important:** This is not a DNS/TLS failure result. It is a limitation of the audit execution channel.

## Results table

| Check | Result | Interpretation |
|---|---|---|
| A / AAAA | NOT VERIFIED | No authoritative/live address answer captured. |
| NS / delegation | NOT VERIFIED | Cannot determine whether nameserver delegation is correct or mismatched. |
| MX | NOT VERIFIED | Cannot determine whether domain mail routing is configured. |
| TXT / SPF / DMARC | NOT VERIFIED | Cannot assess SPF, DMARC, or other TXT records. |
| TLS certificate for apex | NOT VERIFIED | No live TLS handshake or certificate chain/expiry captured. |
| TLS certificate for www | NOT VERIFIED | No live TLS handshake or certificate chain/expiry captured. |
| RDAP / registrar / expiry | NOT VERIFIED | No authoritative registry response captured. |
| HTTP/HTTPS status | PRIOR EVIDENCE ONLY | Prior search result showed a hosting suspension page, but its crawl was months old; fresh live status remains unconfirmed. |

## What the existing evidence does establish
- Search-indexed results for the official domain show legacy booking/rate content, including 2015–2016 rate messaging.
- A prior retrieved official-domain result displayed a hosting-provider suspension page. This does not identify whether the cause is billing, a terms issue, DNS, or another hosting-side condition.
- Directory sources list operations@bounty-tours.com and a legacy Menara mailbox, but directory listings do not prove the MX records or mailboxes currently work.

## Safe one-pass verification links
- Combined RDAP, DNS, mail, HTTP and TLS report: https://www.orbitprobe.com/domain
- DNS records A/AAAA/NS/MX/TXT/CAA/SOA: https://www.orbitprobe.com/dns-lookup
- TLS certificate issuer, hostname coverage, validity and chain: https://www.orbitprobe.com/ssl-checker
- Combined DNS / WHOIS / SSL checker: https://owner.domains/

Run these targets separately in the same audit session:
1. bounty-tours.com
2. www.bounty-tours.com
3. MX/TXT mail checks for bounty-tours.com

Record each observation timestamp, returned values, TTLs, source/resolver, TLS issuer/validity/SANs, HTTP redirect chain and final status. A missing record must be distinguished from a query failure or tool timeout.

## Diagnostic logic once results are available
- NXDOMAIN / no delegation: check registrar status and authoritative nameservers before making any changes.
- A/AAAA resolves but site serves suspension template: likely hosting/account/application state; DNS may be functioning correctly.
- No MX: domain-based inbound email likely lacks DNS mail routing, unless mail is intentionally handled elsewhere.
- MX exists: this alone does not prove mailbox delivery; SMTP acceptance and mailbox access are separate tests.
- TLS expired / hostname mismatch / untrusted chain: fix at the authorized TLS termination point; do not change DNS unless evidence identifies DNS as the cause.
- A and AAAA point to different/stale endpoints: confirm intended architecture before editing either record.
- Registrar expiry/status concern: confirm against registry/registrar data and the authorized domain administrator.

## Change control
No DNS, registrar, hosting, certificate, or mail settings were changed. Do not modify records or attempt account access without the company's authorization and a confirmed intended configuration.

## Audit conclusion
**DNS: INCONCLUSIVE. TLS: INCONCLUSIVE. MX: INCONCLUSIVE.** The existing suspension-page evidence points toward a hosting-side issue, but a current root cause cannot be responsibly assigned until live record and certificate data are captured.