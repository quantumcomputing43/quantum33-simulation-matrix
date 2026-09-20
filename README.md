# Quantum33 Simulation Matrix

Generic deterministic scientific-validation infrastructure for Quantum33 Research.

## Core rule

**Experiment validity precedes result significance.**

The core engine is case-independent. Scientific cases are supplied through explicit adapters; case-specific equations and assumptions must not be embedded in the engine.

## Pipeline

1. FALSIFICATION
2. ADVERSARIAL_STRESS
3. IDENTIFIABILITY
4. ROBUSTNESS
5. SURVIVOR_CHECK

The current synthetic adapter is an infrastructure fixture only. It is not a scientific experiment and establishes no physical claim.

## Status taxonomy

- INFRASTRUCTURE_FAILURE
- IMPLEMENTATION_FAILURE
- METHOD_FAILURE
- SCIENTIFIC_FAILURE
- RESULT

A successful infrastructure run is not scientific evidence.


## Project isolation

The Simulation Matrix is a shared validation engine, but execution state is never shared implicitly between projects.

Every run requires:
- an explicit `project_id`;
- an explicit project manifest binding that project to a `case_id` and `protocol_version`;
- project-namespaced checkpoint, result, and log paths;
- an execution identity that includes the project identity.

A project with no manifest, a disabled manifest, or a manifest/case/protocol mismatch must fail as an infrastructure error rather than silently falling back to another project's state.

The generic repository fixture is `GENERIC_SYNTHETIC`. It is infrastructure-only and is not scientific evidence.

## Parallel execution rule

Different project IDs may execute independently because their state is namespaced. The GitHub Actions workflow also uses a concurrency group so repeated runs of the same project/ref are serialized rather than racing on the same state.

Parallelism does not remove scientific gates: every project still follows the same validity pipeline, and project-specific science remains outside the generic core engine.
