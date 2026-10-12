# Q33 Dropshipping — Zero-Budget Audit V1

**Status:** prelaunch audit only; no live store, supplier, payment route, or sales have been verified.  
**Budget constraint:** 0 MAD upfront.  
**Markets:** Morocco and international.  
**Model:** physical dropshipping without operator-owned inventory.

## Audit-first gates

Before any paid storefront, checkout, or customer transaction, verify with current primary sources or written supplier/platform confirmation:

1. Supplier identity, product price, stock, direct fulfillment, tracking, shipping time, failed-delivery handling, returns and refunds.
2. Seller eligibility for a Morocco-based operator.
3. Payment acceptance, payout destination, fees, settlement timing, reserves/holds and chargeback costs.
4. Whether supplier and shipping costs can be paid after payout. If the supplier requires payment before payout, the zero-cash hypothesis fails unless a documented no-upfront arrangement exists.
5. All-in unit economics and stress-case margin.
6. Relevant Moroccan consumer, tax, import/export and foreign-exchange requirements.

## Current simulation

Run:

```bash
python -m unittest discover -s dropshipping -p 'test_*.py' -v
python -m dropshipping.simulate
```

The three scenarios are explicitly illustrative. They are not sourced prices, forecasts, or market evidence. The tool reports contribution margin and whether an upfront supplier payment makes a zero-budget launch impossible. It intentionally does not invent demand, conversion rates, orders, or revenue.

## Product archetypes for later evidence collection

- Home organization accessories
- Pet accessories
- Simple phone stands / non-electrical accessories

No archetype is selected as a winner. Select only after supplier-level landed costs, actual competition, customer interest evidence, and returns risk are documented.

## Status definitions

- `HOLD_RESEARCH`: any material supplier, platform, payout, fee, shipping, return or compliance fact remains unknown.
- `FAIL_ZERO_BUDGET_MODEL`: unavoidable upfront cash is required or stress-case contribution is non-positive.
- `PASS_TO_MANUAL_PILOT`: all gates are evidence-backed and zero-upfront feasibility is confirmed.
- `COMMERCIAL_SUCCESS`: only after a real unrelated customer order is fulfilled and payout received.

Simulation completion is not commercial validation. No paid service, ad, order, or outreach is initiated by this project.
