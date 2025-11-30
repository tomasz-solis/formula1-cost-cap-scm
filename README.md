# McLaren's Rise in Formula 1: A Data Analysis (2017-2024)

**Status**: Exploratory Analysis Complete | SCM Methodology Under Review

## Project Overview

This project analyzes McLaren's performance trajectory in Formula 1 from 2017-2024, a period spanning major regulatory changes including the 2021 cost cap and 2022 technical reset.

**Initial Goal:** Apply Synthetic Control Methods to evaluate regulatory impact on competitive balance.

**Current Status:** Exploratory analysis complete. SCM methodology paused due to methodological complications (see below).

## Key Findings from Exploratory Analysis

**McLaren's Trajectory:**
- 2017-2020 average: 110 points (midfield tier)
- 2022-2024 average: 376 points (elite tier)
- 2024: 666 points, P2 in championship (career-best since 2007)

**Other Midfield Teams (2022-2024):**
- Alpine: 119 points avg (no tier change)
- Sauber: 25 points avg (no tier change)
- Haas: 36 points avg (no tier change)

**Observation:** McLaren was the only midfield team to achieve tier mobility post-regulation changes.

## Methodological Challenges Identified

During exploratory analysis, several complications emerged for SCM application:

1. **Zero-Sum Constraint**
   - Championship points are relative (McLaren gains → others lose)
   - Violates SCM's independence assumption

2. **Bundled Treatment**
   - Cost cap (2021) + Technical reset (2022) cannot be isolated
   - Cannot attribute effects to specific intervention

3. **Non-Parallel Pre-Treatment Trends**
   - McLaren: Steep climb (30 → 202 points, 2017-2020)
   - Donors: Flat/volatile trajectories
   - Violates SCM's parallel trends assumption

4. **Unmeasured Confounders**
   - McLaren's organizational changes (personnel, tech stack) began mid-2010s
   - Pre-treatment surge likely reflects these changes, not cost cap
   - Cannot isolate regulatory effect from organizational evolution

## What's Been Completed

### Data Preparation
- Clean constructor championship data (2014-2024)
- Team name canonicalization handling rebrands
- Annual and race-level datasets created
- Donor pool construction and validation

See: `notebooks/01_data_preparation.ipynb`

### Exploratory Analysis
- Visualizations of McLaren vs donor pool trajectories
- Pre-treatment trend analysis
- Year-over-year change breakdowns
- Race-level 2024 season analysis
- Placebo unit comparisons (Sauber, Haas)

See: `notebooks/02_exploratory_analysis.ipynb`

## Potential Future Directions

This project could evolve in several ways:

**Option A: Descriptive Case Study**
- Comparative analysis: McLaren vs Alpine (similar resources, different outcomes)
- Qualitative layer: organizational changes, hiring decisions
- Honest conclusion: multiple factors, cannot isolate causality

**Option B: Alternative Research Question**
- Reframe around field compression (inequality metrics)
- Analyze tier mobility patterns across multiple teams
- Use different methodological approach (ITS, event study)

**Option C: Different F1 Question**
- Sprint race format impact on competitiveness
- Driver vs constructor performance attribution
- Home race advantage analysis

## Project Structure
```
├── data/
│   ├── raw/              # F1 data (not in repo)
│   └── processed/        # Clean CSVs
├── notebooks/
│   ├── 01_data_preparation.ipynb       [COMPLETE]
│   ├── 02_exploratory_analysis.ipynb   [COMPLETE]
│   └── 03_scm_mclaren.ipynb            [PAUSED]
├── src/
│   └── team_name_mapping.py            [COMPLETE]
└── outputs/
    └── figures/                         [6 visualizations created]
```

## Technical Implementation

**Data Sources:**
- FastF1 Ergast API (constructor standings 2014-2024)
- Race-by-race results for within-season analysis

**Tools:**
- Python (pandas, numpy, scipy)
- Plotly for interactive visualizations
- Custom team name mapping for historical continuity

**Key Learnings:**
- Importance of validating SCM assumptions before implementation
- Trade-offs between methodological rigor and research question fit
- Value of exploratory analysis in identifying analytical challenges

## Reflections

This project demonstrates an important aspect of rigorous data analysis: recognizing when a chosen methodology doesn't fit the research question, even after significant investment in data preparation.

**The exploratory work revealed that:**
- McLaren's rise is real and substantial
- Multiple confounding factors make causal attribution difficult
- Honest acknowledgment of limitations is more valuable than forced conclusions

**Key takeaway:** Knowing when NOT to apply a method is as important as knowing how to apply it.

---

Part of my causal inference learning journey.

See also: [RDD Analysis](https://github.com/tomasz-solis/rdd-free-shipping) | [DiD Analysis](https://github.com/tomasz-solis/marketing-campaign-causal-impact)

---

## Contact

**Tomasz Solis**
- Email: tomasz.solis@gmail.com
- LinkedIn: [linkedin.com/in/tomaszsolis](https://www.linkedin.com/in/tomaszsolis/)
- GitHub: [github.com/tomasz-solis](https://github.com/tomasz-solis)