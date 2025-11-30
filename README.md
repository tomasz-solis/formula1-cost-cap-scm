# F1 Cost Cap Impact Analysis: A Synthetic Control Study

**Status**: Work in Progress - Data Preparation Complete

## Project Goal

Evaluate the heterogeneous effects of F1's 2021 cost cap regulation using Synthetic Control Methods. The core puzzle: why did McLaren surge to championship contention (666 points, P2 in 2024) while teams like Haas and Sauber remained in the midfield despite the same regulations?

## Research Question

"Did the bundled intervention of the 2021 cost cap and 2022 technical regulations enable McLaren to join the top pack, and if so, through what mechanism?"

**Hypothesis**: The cost cap only helped teams that could (1) spend up to the £145M limit AND (2) capitalize on talent released from top teams. McLaren met both conditions. Haas and Sauber met neither.

## Methodology

**Method**: Synthetic Control Method (SCM)

**Treated Unit**: McLaren (2022-2024)

**Donor Pool**:
- Main analysis: Alpine, Sauber, Haas (excludes RB due to junior team structure)
- Robustness check: Alpine, Sauber, Haas, RB (tests sensitivity to RB inclusion)

**Time Periods**:
- Pre-treatment: 2017-2020 (4 years before treatment, excludes 2021 transition year)
- Treatment: 2022-2024 (cost cap + new technical regulations in effect)

**Why exclude 2021?**
- 2021 cars were frozen carry-overs from 2020 (pandemic regulations)
- Cost cap was active but didn't affect racing (development for 2022 started under cap)
- Token-based development system made 2021 a messy transition year

**Bundled Treatment Problem**: We cannot isolate the pure cost cap effect from the 2022 technical reset (ground effect return, 18-inch wheels, simplified aero). These interventions are bundled - we analyze their combined effect and acknowledge we cannot disentangle them.

## Validation Strategy

**Placebo Tests**:
1. Sauber (primary) - Cost cap not binding, stable team, no major shocks
2. Haas (secondary) - Cost cap not binding, but 2021 tank year confounds interpretation

**Expected Results**:
- McLaren: Large treatment effect (synthetic McLaren << actual McLaren 2022-2024)
- Sauber: No sustained treatment effect (synthetic Sauber ≈ actual Sauber)
- Haas: 2022 rebound from tank year, but no sustained surge like McLaren

**Robustness Checks**:
- Include RB in donor pool (tests if exclusion biases results)
- Race-level time series (validates within-season dynamics)
- Pre-treatment period sensitivity (2017-2019 vs 2017-2020)

## Key Findings (Preliminary)

**McLaren Trajectory**:
- 2017-2020 average: 110 points
- 2022-2024 average: 376 points
- Increase: +242% 

**Mechanism (Hypothesized)**:
- McLaren could spend up to £145M (cap was binding for them)
- Hired Mercedes aerodynamicists released due to top team budget cuts
- 2022 technical reset reduced infrastructure disadvantage
- Sustained improvement 2023-2024 suggests organizational capability, not luck

**Donor Pool Pre-Treatment (2017-2020 Average)**:
- Alpine: 121 points
- Haas: 34 points
- Sauber: 26 points
- RB: 84 points

McLaren's pre-treatment trajectory (30 → 62 → 145 → 202) shows strong upward trend, requiring careful synthetic control construction.

## Project Structure
```
├── data/                              # F1 data (not in repo, .gitignored)
│   ├── raw/              
│   └── processed/        
├── notebooks/
│   ├── 01_data_preparation.ipynb      # [COMPLETE]
│   ├── 02_exploratory_analysis.ipynb  # [IN PROGRESS]
│   ├── 03_scm_mclaren.ipynb
│   ├── 04_placebo_tests.ipynb
│   └── 05_sensitivity_analysis.ipynb
├── src/
│   ├── team_name_mapping.py           # [COMPLETE]
│   ├── scm_utils.py
│   ├── visualization.py
│   └── validation.py
└── outputs/
    ├── figures/
    └── results/
```

## Data Sources

- Constructor Championship Standings (2014-2024) via FastF1 Ergast API
- Race-by-race results for within-season analysis
- Team mappings handle historical rebrands (Renault→Alpine, Toro Rosso→AlphaTauri→RB)

## Technical Notes

**Team Name Canonicalization**: 
The `team_name_mapping.py` module handles F1's frequent rebranding:
- Tracks institutional continuity (Alpine = Renault rebrand, same team)
- Identifies ownership shocks (Williams 2020 Dorilton takeover, Aston Martin 2020 Stroll investment)
- Excludes defunct teams (Lotus, Manor, Caterham)

**Why RB is excluded from main donor pool**:
- RB (formerly AlphaTauri, Toro Rosso) is Red Bull's junior team
- Structural relationship with Red Bull Racing creates dependency
- 2022 collapse (-107 points) was idiosyncratic, not representative
- Included in robustness check to validate results are stable

## Causal Inference Learning

This project applies Synthetic Control Methods to a real-world policy question with messy features:
- Bundled treatment (cannot isolate cost cap from technical reset)
- Zero-sum outcomes (championship points are relative)
- General equilibrium effects (talent reallocation across teams)
- Heterogeneous treatment effects (cap binding for some teams, not others)

The analysis prioritizes honest acknowledgment of limitations over overclaiming causal certainty.

## Status

- [x] Project setup and repository structure
- [x] Team name canonicalization with institutional continuity tracking
- [x] Data preparation pipeline (annual + race-level datasets)
- [x] Donor pool construction (main + robustness)
- [ ] Exploratory data analysis and visualization
- [ ] SCM implementation (McLaren)
- [ ] Placebo tests (Sauber, Haas)
- [ ] Sensitivity analysis
- [ ] Portfolio documentation

## Portfolio Narrative

"The F1 cost cap reduced inequality but didn't eliminate it. McLaren surged because they could spend up to the £145M cap AND capitalize on talent released from top teams. Teams like Haas and Sauber, who couldn't spend £145M anyway, saw no sustained improvement. Institutional capacity to utilize regulatory constraints matters more than the regulation itself."

---

Part of my causal inference learning journey.

See also: [RDD Analysis](https://github.com/tomasz-solis/rdd-free-shipping) | [DiD Analysis](https://github.com/tomasz-solis/marketing-campaign-causal-impact)

---

## Contact

**Tomasz Solis**
- Email: tomasz.solis@gmail.com
- LinkedIn: [linkedin.com/in/tomaszsolis](https://www.linkedin.com/in/tomaszsolis/)
- GitHub: [github.com/tomasz-solis](https://github.com/tomasz-solis)