# Football Performance Monitoring

**Master Sport, Health and Artificial Intelligence — M1 2SIA**  
University Of Montpellier · Course: *Python-R-Git* · Supervisor: Denis MOTTET  
Student: Celine BENDEKOUM · 2025–2026

---

## Overview

This project builds a **GPS/IMU performance monitoring pipeline** for a football club, designed to answer the physical load management questions a coaching staff asks every week:

- What is the load of a match compared to a training session?
- How does load evolve over the season?
- Which positions are most exposed to high-intensity efforts?
- Which sessions are atypical — too intense, too low, or suspicious data?
- How do two players compare relative to their own habits?

The pipeline ingests raw GPS data, stores it in a SQL database, applies quality control, computes standardised KPIs (Key Performance Indicators), and produces staff-oriented visualisations and statistical analyses.

---

## Repository structure

```
Football_Analysis/
│
├── data/
│       ├── summary.csv             # Aggregated player × session KPIs (main data source)
│       └── <overall_practice.pdf
|       └──<overall_game.pdf   
│
├── results/
│   └── Images
│   └── Images_R                  # Exported charts and visualisations
│      
│
├── sources/
│   └── Sources.pdf               # Enumerating all sources and LLM assitance used
│   
├── main.ipynb                      # Python entry point — run this first
├── main.Rmd                        # R entry point — knit after main.ipynb
├── main.Rproj                      # RStudio project file
│
├── bendekoum.celine.html           # Project report (HTML, self-contained)
├── README.md                       # This file
└── LICENCE                         # GPLv3
```

---

## Data

| File | Description |
|------|-------------|
| `summary.csv` | One row per player × session. Contains total distance, 7 speed zones (0–5, 5–10, 10–15, 15–21, 21–24, 24–30, >30 km/h), max speed, average speed, and acceleration/deceleration counts ≥ 3 m/s². |
| Raw tracking files | Per-sensor position and speed time series. Available for within-session analysis (not exploited in the current version). |

### Key derived KPI

**HID (High Intensity Distance)** = distance covered above 21 km/h  
`HID_km = d_21_24 + d_24_30 + d_over30`

### Quality control rules

| Rule | Condition | Scope |
|------|-----------|-------|
| Valid sensor & timestamp | `sensor IS NOT NULL`, `session_ts IS NOT NULL` | All |
| Known session type | `session_type IN ('game', 'practice')` | All |
| No negative KPI values | `distance ≥ 0`, `max_speed ≥ 0`, etc. | All |
| Match minimum distance | `distance_km ≥ 0.5` | Games only |
| Match maximum distance | `distance_km ≤ 20.0` | Games only |
| Plausible max speed | `max_speed_kmh ≤ 40.0` | Games only |
| Speed-zone coherence | `Σ zones ≤ distance × 1.15` | All |

---

## Python pipeline (`main.ipynb`)

**Stack:** DuckDB · pandas · numpy · matplotlib · seaborn

The notebook builds a DuckDB database (`football.duckdb`) with four layers:

| Layer | Object | Description |
|-------|--------|-------------|
| 1 | `summary_raw` | Raw VARCHAR import — never fails on bad values |
| 2 | `summary` | Typed view via `try_cast` — bad values become NULL |
| 3 | `players` | Player dimension table with anonymisation toggle |
| 4 | `summary_clean` | Quality-filtered view used by all analyses |

### Analyses

1. **Matches — team overview**: KPI time series, speed-zone profiles, position boxplots
2. **Matches — specific session**: per-player rankings (distance, HID) for a selected match
3. **Training — team overview**: seasonal load trends, weekly variability
4. **Training — specific session**: player scatter plots (distance vs HID ratio)
5. **Team dashboard**: game vs practice comparison across all KPIs
6. **Individual comparison**: two-player profiles with normalised KPIs

### Setup

```bash
pip install duckdb pandas numpy matplotlib seaborn jupyterlab
```

Open `main.ipynb` in Jupyter and run all cells. The DuckDB database is created automatically on first run.

> **Note:** All file paths in the notebook are relative. Do not use absolute paths.

---

## R analysis (`main.Rmd`)

**Stack:** readr · dplyr · tidyr · ggplot2 · scales · coin · rstatix · knitr · kableExtra

### Install required packages

```r
install.packages(c(
  "readr", "dplyr", "tidyr", "ggplot2", "scales",
  "coin", "rstatix", "knitr", "kableExtra", "broom"
))
```

### Analyses

| Analysis | Method | Purpose |
|----------|--------|---------|
| A. Normality check | Shapiro–Wilk test + QQ-plots | Justify non-parametric tests |
| B. Game vs practice | Wilcoxon rank-sum + effect size *r* + BH correction | Compare all KPIs across session types |
| C. Positional differences | Kruskal–Wallis + Dunn post-hoc (Bonferroni) | Identify which positions differ significantly |
| D. Predictive model | Linear regression `distance ~ HID + max_speed + session_type` | Quantify KPI relationships + residuals diagnostics |
| E. Outlier detection | Z-score (threshold: \|z\| > 2 per position × session type) | Flag anomalous sessions for staff review |

### How to run

1. Open `main.Rmd` in RStudio
2. Install packages (see above)
3. Click **Knit** (`Ctrl+Shift+K`) → produces an HTML report

> The R script reads `data/data/summary.csv` directly with relative paths. It applies the same quality control thresholds as the Python pipeline to ensure consistent results.

---

## Report

The file `bendekoum.celine.html` is a self-contained project report covering the scientific question, data, pipeline architecture, analyses, results, and discussion. It can be opened in any browser with no external dependencies.

---

## Reproducibility

- All file paths are **relative** — the project runs on any operating system (Windows, macOS, Linux)
- `football.duckdb` is generated locally and excluded from Git
- Python dependencies can be installed with `pip`, R dependencies with `install.packages()`
- The quality control rules are defined once (in the DuckDB view for Python, and mirrored in `main.Rmd` for R) to guarantee that both pipelines produce consistent results

---

## Licence

This project is licensed under the GNU General Public License v3.0 — see the `LICENCE` file for details.
