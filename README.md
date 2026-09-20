# Quantum33 Simulation Matrix

Independent simulation and falsification infrastructure for Quantum33 research.

## Scientific rule

**Experiment validity precedes result significance.**

## Architecture

The core engine is generic. Scientific hypotheses are introduced through case adapters and protocol contracts rather than by modifying the engine.

## BHD Phase 1

Phase 1 defines the boundary of the BHD scientific case without running a scientific experiment.

The BHD protocol records:
- case identity and protocol version;
- H0, H1, and H2 hypothesis roles;
- separation between information coupling (g_info) and spacetime coupling (g_spacetime);
- the required five validity stages;
- an explicit execution gate.

Scientific execution is intentionally blocked while the observable derivation, observable signature, and stage-specific criteria remain unregistered.

The observable derivation contract is recorded in simulation_matrix/cases/bhd_observable_derivation.md and explicitly forbids result-driven observable selection.

This is deliberate: the protocol must be complete before the experiment can run.

## BHD Pre-Experiment Validation

The repository now contains a deterministic N=4 TFIM/QFI implementation under `simulation_matrix/cases/bhd_preexperiment.py`. It validates the previously declared mathematical benchmark points at h=0.1 and h=0.01. This is an implementation/model-consistency check only; it does **not** constitute hidden-sector evidence and does not open the BHD scientific execution gate.
