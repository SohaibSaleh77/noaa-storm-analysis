# NOAA Storm Analysis

A reproducible, end-to-end Python pipeline for ingesting, analyzing, and visualizing severe weather events across the United States (2010–2023), built on NOAA's Storm Events database and GHCND daily climate observations.

The project transforms raw meteorological records into structured insights on **economic damage**, **human mortality**, **regional storm climatology**, and **urban climate baselines** — combining descriptive statistics, inferential hypothesis testing, and narrative interpretation.

---

## Table of Contents

- [Overview](#overview)
- [Key Findings](#key-findings)
- [Pipeline Architecture](#pipeline-architecture)
- [Repository Structure](#repository-structure)
- [Data Sources](#data-sources)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Outputs](#outputs)
- [Methodology Notes](#methodology-notes)
- [License](#license)

---

## Overview

Severe weather in the United States causes tens of billions of dollars in damage and hundreds of fatalities each year. This project consolidates 14 years (2010–2023) of NOAA Storm Events records alongside daily surface climate observations from a reference urban station (NYC Central Park, `USW00094728`) to answer four core questions:

1. **Where and when** do severe storms cause the greatest economic damage?
2. **Which hazards** are the deadliest, and why does mortality not track property loss?
3. **How do tornado dynamics differ** between the traditional Plains (Tornado Alley) and the southeastern Dixie Alley?
4. **Are urban climate baselines shifting** over the study window?

The pipeline is fully reproducible via a single `./run.sh` command and is structured for clarity, modularity, and extension.

---

## Key Findings

### Macroeconomic Toll & State Vulnerability
- **$413.79 Billion** in cumulative property + crop damage (adjusted to constant 2023 USD) between 2010 and 2023.
- Top-5 impacted states by total damage:
  - **Texas** — $100.80B (65,313 events)
  - **Louisiana** — $45.31B (12,609 events, $3.59M per-event severity)
  - **Florida** — $43.84B
  - **New Jersey** — $34.82B
  - **California** — $30.24B
- **2017 outlier** exceeding $100B in a single year, driven by Hurricanes **Harvey, Irma, and Maria**.
- Per-event severity (Louisiana > Florida > New Jersey) reveals the catastrophic capital destruction of Gulf Coast hurricane landfalls on vulnerable delta infrastructure.

### Mortality vs. Property Damage Disconnect
- **Excessive Heat** is the single deadliest U.S. weather hazard (**2,235 direct fatalities**), with Heat reports adding another **1,770+**.
- Tornadoes (~1,200), Flash Floods (~1,000), and Rip Currents (~800) follow.
- A structural divergence exists: hurricanes destroy the most capital but cause fewer deaths (evacuation pipelines, satellite tracking), while heatwaves and flash floods claim more lives due to shorter lead times and behavioral factors.

### Tornado Alley vs. Dixie Alley
- Near-exact touchdown parity: **Plains 5,220** vs. **Southeast 5,037** (2010–2023).
- **Seasonal divergence:** Southeast peaks in **April**; Plains peak in **May–June**.
- **Diurnal peak:** Nationwide maximum tornado frequency at **17:00 local time**, aligned with peak CAPE.
- Southeastern tornadoes stay on the ground significantly longer (median 4.0 min vs. 3.0 min; Mann-Whitney U test, **p ≈ 3.89 × 10⁻³³**), elevating casualty risk when combined with nighttime storms, forest canopy, and higher population density.

### Urban Climate Baseline Shifts
- NYC Central Park mean daily T_max rose by **+0.79°F** when comparing 2010–2015 baseline vs. 2020–2023 baseline.
- Extreme heat days (T_max > 90°F) cluster in summers of 2010, 2011, and 2016 — illustrating increasing thermal volatility in urban centers.

---

## Pipeline Architecture

The full workflow is orchestrated by `run.sh` and executes in eight sequential stages:

| Step | Script | Output |
|------|--------|--------|
| 1 | `scripts/fetch_storms.py` | `data/processed/storms.pkl` |
| 2 | `scripts/fetch_climate.py` | `data/processed/climate.pkl` |
| 3 | `scripts/plot_trends.py` | `outputs/figures/temporal_trends.png` |
| 4 | `scripts/plot_maps.py` | `outputs/figures/spatial_distribution_scatter.png` |
| 5 | `scripts/plot_heatmap.py` | `outputs/maps/tornado_heatmap.html` |
| 6 | `scripts/analyze_tornadoes.py` | `outputs/figures/*.png` |
| 7 | `scripts/analyze_impact.py` | `outputs/figures/*.png` |
| 8 | `scripts/generate_report.py` | `analysis.md` (narrative report) |

Each stage reads persisted intermediate artifacts (`.pkl` files), enabling selective re-execution of downstream steps without re-fetching upstream data.

---

## Repository Structure

```
noaa-storm-analysis/
├── src/                          # Core analysis library
│   ├── __init__.py
│   ├── config.py                 # Configuration & constants
│   ├── utils.py                  # Shared helper utilities
│   ├── storm_data.py             # Storm events ingestion & cleaning
│   ├── climate_data.py           # GHCND climate observations handling
│   ├── impact_analysis.py        # Economic damage & mortality analysis
│   ├── spatial_analysis.py       # Geographic distribution analysis
│   ├── temporal_trends.py        # Time-series trend analysis
│   ├── tornado_analysis.py       # Tornado Alley vs. Dixie Alley study
│   └── report.py                 # Narrative report generation
│
├── scripts/                      # Executable pipeline steps
│   ├── fetch_storms.py
│   ├── fetch_climate.py
│   ├── plot_trends.py
│   ├── plot_maps.py
│   ├── plot_heatmap.py
│   ├── analyze_tornadoes.py
│   ├── analyze_impact.py
│   └── generate_report.py
│
├── run.sh                        # End-to-end pipeline orchestrator
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project configuration
├── .python-version               # Python version pin
├── analysis.md                   # Generated analytical report
└── README.md                     # This file
```

---

## Data Sources

| Source | Coverage | Variables Used |
|--------|----------|----------------|
| **NOAA Storm Events Database** | 2010–2023, all U.S. states | Event type, location (state/county), begin/end time, injuries, fatalities, property damage, crop damage |
| **NOAA GHCND — Station USW00094728** (NYC Central Park) | 2010–2023, daily | T_max, T_min, precipitation |

All damage values are normalized to constant 2023 USD using the CPI-U adjustment factor.

---

## Installation

### Prerequisites
- Python 3.10+ (see `.python-version`)
- A NOAA NCEI API token (free) — [request one here](https://www.ncdc.noaa.gov/cdo-web/token)

### Setup

```bash
# Clone the repository
git clone https://github.com/SohaibSaleh77/noaa-storm-analysis.git
cd noaa-storm-analysis

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your NOAA API token (export it before running)
export NOAA_TOKEN="your_token_here"
```

---

## Usage

### Run the Full Pipeline

```bash
chmod +x run.sh
./run.sh
```

The script will:
1. Fetch storm events (2010–2023)
2. Fetch daily climate data for NYC Central Park
3. Generate temporal trend visualizations
4. Generate spatial distribution maps
5. Generate an interactive tornado heatmap (HTML)
6. Run tornado regional analysis (Plains vs. Southeast)
7. Run impact analysis (damage + fatalities)
8. Generate the consolidated `analysis.md` report

### Run Individual Stages

Each script is independently executable. For example, to regenerate only the tornado analysis:

```bash
python scripts/analyze_tornadoes.py \
    --input data/processed/storms.pkl \
    --output_dir outputs/figures
```

### Outputs

After a successful run, results are written under `outputs/`:

```
outputs/
├── figures/
│   ├── temporal_trends.png
│   ├── spatial_distribution_scatter.png
│   ├── tornado_*.png
│   └── impact_*.png
└── maps/
    └── tornado_heatmap.html      # Interactive Folium/Leaflet map
```

The narrative report is written to `analysis.md` at the project root.

---

## Modules

### `storm_data.py`
Wraps the NOAA Storm Events API, normalizes field naming, parses damage strings into numeric USD, applies CPI adjustments, and returns a tidy DataFrame indexed by event ID.

### `climate_data.py`
Fetches GHCND daily observations for a given station ID, handles missing-value codes, and converts units to consistent Fahrenheit/inches conventions.

### `impact_analysis.py`
Aggregates damage and fatalities by state, hazard type, and year. Computes a per-event **Severity Index** ($M / event) and ranks jurisdictions.

### `spatial_analysis.py`
Produces state-level choropleths and county-level scatter plots of storm event density.

### `temporal_trends.py`
Computes yearly and seasonal aggregates, smoothing lines, and trend tests across the 14-year window.

### `tornado_analysis.py`
Segments tornado events into **Plains (Tornado Alley)** and **Southeast (Dixie Alley)** cohorts. Performs:
- Touchdown frequency comparison
- Seasonal climatology (monthly histograms)
- Diurnal distribution (hour-of-day)
- Ground-duration comparison via **Mann-Whitney U test**

### `report.py`
Assembles all upstream analytical artifacts into a structured Markdown narrative with tables, statistical results, and interpretive commentary.

---

## Methodology Notes

- **Currency normalization:** All property and crop damage values are adjusted to constant 2023 USD using the U.S. Bureau of Labor Statistics CPI-U series.
- **Regional definitions:**
  - **Plains (Tornado Alley):** TX, OK, KS, NE, SD, ND
  - **Southeast (Dixie Alley):** AL, MS, GA, TN, KY, AR, LA
- **Statistical testing:** Non-parametric **Mann-Whitney U** is used for tornado ground-duration comparison due to the right-skewed, non-normal distribution of track lengths.
- **Urban baseline:** A single reference station (NYC Central Park) is used as an urban climate index; findings reflect local conditions and should not be generalized nationally without additional stations.

---

## License

See repository for license details. NOAA data is public domain; derivative analysis and code are the author's.

---

## Citation

If you use this project or its findings, please cite the repository:

```
Sohaib Saleh. (2026). noaa-storm-analysis [Computer software].
https://github.com/SohaibSaleh77/noaa-storm-analysis
```
