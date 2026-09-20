# BHD Observable Derivation Contract

## Purpose

Define how the primary BHD observable will be selected without using simulation outcomes.

## Fixed model boundary

The current case boundary contains:
- boundary information: rho_boundary
- information coupling: g_info
- spacetime coupling: g_spacetime
- hypotheses: H0 (epsilon = 0), H1 (epsilon != 0), H2 (classical nuisance explanation)

These labels are protocol roles, not evidence for a physical interpretation.

## Selection rule

A primary observable is admissible only if all conditions hold:

1. It is derived from an explicit forward map from model inputs to an observable output.
2. It is computable under H0, H1, and H2.
3. Its units and normalization are fixed before simulation.
4. Its definition does not depend on fitted results from the same test.
5. Its null distribution can be generated independently under H0.
6. The H2 nuisance model can generate the same observable without inserting the H1 answer by construction.
7. The observable is distinct from an identifiability diagnostic.

## Candidate roles

- OBS-A: direct forward-model signature. Candidate for primary observable after the forward map is explicitly written.
- OBS-B: nuisance-orthogonal signature. Candidate only after the classical nuisance tangent/model space is explicitly defined.
- OBS-C: conditional information fraction R² = I(epsilon|eta) / I(epsilon,epsilon). Diagnostic for local identifiability, not primary physical evidence.

## Required derivation record

Before selecting one candidate, record:
- forward equation;
- input/state variables;
- output variable and units;
- H0/H1/H2 generation rules;
- nuisance parameters;
- normalization;
- admissible parameter domain;
- independent-data rule;
- falsification statistic and threshold.

## Scientific gate

No candidate is promoted to primary_observable until the derivation record is complete and independently auditable.
