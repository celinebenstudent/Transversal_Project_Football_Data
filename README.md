# Football Performance Monitoring (GPS/IMU)

Master 2SIA — Python/R/Git project

This repository contains a **football performance monitoring** workflow built from **GPS/IMU** data (player–session aggregates + optional raw tracking folders).

It provides:
- A **Python + DuckDB** pipeline (ingestion → quality control → SQL views → monitoring dashboards) in a Jupyter notebook.
- An **R Markdown** report focused on statistical testing and modeling (game vs practice, position effects, trends, simple linear regression).

## Project structure

```
Project_3/
├─ football_project/
│  ├─ main.ipynb
│  ├─ football.duckdb
│  ├─ data/
│  │  └─ data/summary.csv
│  ├─ export_visual_outputs.py
│  ├─ visual_outputs/              # extracted notebook outputs (gallery)
│  └─ visual_outputs.zip           # exported plots + HTML tables
└─ Football_project_R/
   ├─ main.Rmd
   ├─ main.html                    # knitted report
   ├─ main.Rproj
   ├─ export_rmd_visual_outputs.py
   ├─ r_visual_outputs/            # extracted HTML-embedded images (gallery)
   └─ r_visual_outputs.zip
```

## Data

- Main aggregated dataset: `football_project/data/data/summary.csv`.
- The dataset is a **player × session** table containing KPIs such as:
  - total distance
  - speed zones (0–5, 5–10, …, >30 km/h)
  - accelerations/decelerations counts
  - max speed

## Key KPIs

- **Distance (km)**
- **HID (High-Intensity Distance)**
  - Python notebook: HID = distance at **≥ 21 km/h** (`21–24 + 24–30 + >30`)
  - R report: HID = distance at **> 15 km/h** (`15–21 + 21–24 + 24–30 + >30`)
- **HID ratio**: `HID / total distance`
- **Accelerations / Decelerations**: counts at ≥ 3 m/s²

## Python (DuckDB monitoring notebook)

Location: `football_project/main.ipynb`

What it does:
1. Creates/opens a DuckDB database (`football.duckdb`).
2. Ingests `summary.csv` into a raw table and builds typed SQL views.
3. Applies **quality-control rules** into a `summary_clean` view (consistent filters for monitoring).
4. Produces match and training monitoring outputs:
   - team timelines (distance, HID ratio, acc/dec, max speed)
   - speed-zone profiles (stacked bars)
   - distributions and position comparisons
   - auto-selected “specific session” zoom
   - simple dashboard and two-player comparison

### Run it

- Open `football_project/main.ipynb` in VS Code or Jupyter.
- Run cells top-to-bottom.

Python dependencies (typical):
- `duckdb`, `pandas`, `numpy`, `matplotlib`, `seaborn`

Example install:
```bash
pip install duckdb pandas numpy matplotlib seaborn
```

### Export the notebook visual outputs

The notebook already includes exported visuals:
- `football_project/visual_outputs/` (gallery)
- `football_project/visual_outputs.zip` (shareable bundle)

To re-export from the current notebook file:
```bash
python football_project/export_visual_outputs.py football_project/main.ipynb \
  --out football_project/visual_outputs --include-html --zip football_project/visual_outputs.zip
```

Open the gallery:
- `football_project/visual_outputs/index.html`

## R (statistical report)

Location: `Football_project_R/main.Rmd` → knitted to `Football_project_R/main.html`

Scientific questions covered:
1. **Game vs practice**: are KPI distributions significantly different?
2. **Evolution over time**: trend visualization and peak/overload inspection.
3. **Modeling**: simple linear regression predicting distance from intensity variables.

Methods used:
- Normality checks (QQ-plots, Shapiro–Wilk)
- Non-parametric tests (Wilcoxon rank-sum; Kruskal–Wallis; Dunn post-hoc)
- Linear regression + diagnostics
- Simple outlier detection (|z| > 2 within position × session type)

### Knit the report

- Open `Football_project_R/main.Rproj` in RStudio.
- Knit `main.Rmd` to HTML.

R packages used (as in the report):
- `readr`, `dplyr`, `tidyr`, `ggplot2`, `scales`, `coin`, `rstatix`, `knitr`, `kableExtra`, `broom`

### Export visual outputs from the knitted HTML

If plots are embedded inside `main.html` (base64 images), extract them with:
```bash
python Football_project_R/export_rmd_visual_outputs.py --html Football_project_R/main.html --out Football_project_R/r_visual_outputs
```

Open the gallery:
- `Football_project_R/r_visual_outputs/index.html`

## Notes / limitations

- Quality-control thresholds are simple, explainable rules (domain-driven). They can be adjusted depending on club context and data provider.
- Some analyses would benefit from contextual variables not available here (e.g., minutes played, match context).
- For repeated measures per player, mixed-effects models would be more appropriate than a simple linear model.

## Author

Celine BENDEKOUM
