# F1 Cost Cap Impact Analysis: A Synthetic Control Study

**Status**: 🚧 Work in Progress

## Project Goal

Evaluate the heterogeneous effects of F1's 2021 cost cap regulation using Synthetic Control Methods, focusing on why McLaren improved while teams like Haas didn't.

## Research Question

"Did the 2021 cost cap + 2022 technical reset enable McLaren to join the top pack, and if so, through what mechanism?"

## Methodology

- **Method**: Synthetic Control Method (SCM)
- **Treated Unit**: McLaren (2022+)
- **Donor Pool**: Midfield teams 2017-2021 (Alpine, Alfa Romeo, AlphaTauri, Aston Martin, Haas)
- **Pre-treatment Period**: 2017-2021
- **Post-treatment Period**: 2022-2024

## Validation Strategy

**Placebo Tests**:
1. Haas (primary) - cap not binding
2. Alfa Romeo (secondary) - cap not binding
3. AlphaTauri (optional) - cap marginally binding

## Expected Findings

- **McLaren**: Large positive effect (~100-200 constructor points)
  - Mechanism: Hired Mercedes aerodynamicists, cap was binding
- **Haas/Alfa Romeo**: No effect
  - Mechanism: Cap wasn't binding (couldn't spend £145M anyway)

## Project Structure
```
├── data/                  # F1 championship data (not in repo)
├── notebooks/             # Analysis notebooks
│   ├── 01_data_preparation.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_scm_mclaren.ipynb
│   ├── 04_placebo_tests.ipynb
│   └── 05_sensitivity_analysis.ipynb
├── src/                   # Reusable functions
│   ├── scm_utils.py
│   ├── visualization.py
│   └── validation.py
└── outputs/              # Figures and results
```

## Status

- [x] Project setup
- [ ] Data preparation
- [ ] Exploratory analysis
- [ ] SCM implementation (McLaren)
- [ ] Placebo tests (Haas, Alfa Romeo)
- [ ] Sensitivity analysis
- [ ] Final documentation

---
Part of my causal inference learning journey. <br>
See also: <br>
[RDD](https://github.com/tomasz-solis/rdd-free-shipping) | [DiD](https://github.com/tomasz-solis/marketing-campaign-causal-impact)*
