# Platform evidence audit — 2026-10-12

## Current decision

**Morocco-first pilot candidate: HOLD, not approved to launch.** DropyCash is the strongest lead for further verification because its public website advertises free registration, no monthly subscription, local Moroccan COD fulfillment, and a 60 MAD fee per successfully delivered order. This is vendor-published information, not independently verified performance.

## Evidence table

| Item | Public evidence | Status / consequence |
|---|---|---|
| DropyCash registration | https://www.dropycash.com/ar/pricing | Website says registration is free and no bank card is required. Verify during signup; no account was created by this audit. |
| Inventory and fulfillment | https://www.dropycash.com/ar | Website advertises local product catalog, supplier sourcing, storage, packaging, confirmation and delivery. Actual product-level terms remain unverified. |
| COD service fee | https://www.dropycash.com/ar | Public page advertises 60 MAD per successfully delivered order, including service/logistics items. Confirm exclusions, refused/returned order charges, taxes and payout deductions in writing. |
| Market coverage | https://dropycash.com/en | The platform describes itself as Morocco-only and COD-only. It does not validate the international-market requirement. |
| Payout timing | https://www.dropycash.com/ar/about | Website advertises weekly payout. Confirm payout method, minimum threshold, delay, bank transfer fees and required business documents directly with the provider. |
| YouCan Pay card processing | https://youcanpay.com/pricing | Public price: Moroccan cards 3.9% + 2 MAD per successful card transaction; page also says it normally retains 30% for 30 days. This may be irrelevant to a COD-only DropyCash pilot, but is a material cost if used. |
| Shopify gateway compatibility | https://help.shopify.com/en/manual/payments/third-party-providers/payment-gateway-availability | Shopify directs sellers to check payment providers available for their country. Do not build a paid Shopify store before verifying a compatible Morocco-based payout route. |
| PayPal country features | https://developer.paypal.com/payouts/supported-features/ | Official feature matrix lists Morocco as send, receive and withdraw, subject to applicable product terms and local requirements. This does not by itself prove a specific Shopify gateway integration or business-account eligibility. |

## Zero-budget stress test

The local COD model can potentially avoid buying inventory in advance if the provider truly supplies/fulfills products and deducts all costs from proceeds. That critical cash-flow condition is **not yet proven** by the public landing page alone.

Before approval, obtain written answers to:

1. Is any product purchase, deposit, shipping, return, packaging, account, or withdrawal fee payable before the first successful delivery?
2. Does the 60 MAD include product cost, packaging, shipping, call-center confirmation and all taxes, or are some charges additional?
3. What happens financially when a customer refuses delivery, returns an item, or a parcel is lost?
4. What is the exact payout schedule and minimum withdrawal? Which payout methods accept a Moroccan individual / auto-entrepreneur?
5. Can the seller start as an individual, or is auto-entrepreneur / company registration required?
6. Can the seller use organic traffic and a free landing page without paying for a domain, subscription, or ads?

## Product decision

No product has passed. The three archetypes remain unranked pending a live catalog and supplier-level evidence:

- Home organization accessories
- Pet accessories
- Simple phone stands / non-electrical accessories

A product passes only if the actual sale price minus the supplier/product charge, 60 MAD service fee (if confirmed applicable), payment/payout fees, return/refusal reserve, and other documented costs leaves a positive contribution in the stress case **and** no unavoidable upfront cash is required.

## International-market gate

DropyCash's public description is Morocco-only/COD-only, so it cannot alone satisfy the international-sales goal. International sales stay **HOLD** until seller eligibility from Morocco, gateway support, payout to the Moroccan bank account, supplier shipping, taxes/customs, returns and foreign-exchange compliance are documented.

## Final status

- Code and deterministic sensitivity tests: implemented in isolated branch.
- GitHub Actions tests: passed on 2026-10-12.
- Supplier verified in writing: no.
- Product prices and total landed costs verified: no.
- Payment/payout route verified for this business: no.
- Real orders, revenue, or profit: 0.
- Decision: **HOLD_RESEARCH — do not pay for a store, ads, inventory, or supplier setup yet.**
