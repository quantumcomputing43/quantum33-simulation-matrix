# Quantum33 Simulation Matrix

Independent simulation and falsification infrastructure for Quantum33 research.

## Scientific rule

Experiment validity precedes result significance.

## Run locally

Install dependencies, then execute the matrix and its configured numerical
checks from the repository root:

```bash
pip install -r requirements.txt
python -m simulation_matrix.runner
python -m simulation_matrix.falsification
python -m simulation_matrix.adversarial_stress
python -m unittest discover -s tests
```

The runner validates and records the generic matrix configuration. Numerical
stages use the shared primitives in `simulation_matrix.numerics`, which keeps
normalization, Fisher information, and quantum-potential calculations
consistent across stages.
