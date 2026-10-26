# Tobacco Tax & Consumption Analysis (U.S., 1990–2019)

An applied policy analytics and geospatial data analysis project examining the relationship between cigarette taxation and tobacco consumption trends across U.S. states over a 30-year period.

---

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/e489cce9-2956-4fb1-b9f6-36199f49a538" />


## Run locally

Tested with Python 3.12. The dashboard uses the original long-format **The Tax Burden on Tobacco (1970–2019)** CSV and filters to 1990–2019, retaining all 50 states and DC (1,530 state-year records for the supplied complete export).

```bash
git clone https://github.com/HIRAL13CHOKSI/tobacco-tax-consumption-analysis.git
cd tobacco-tax-consumption-analysis
python -m venv .venv
```

Activate with `source .venv/bin/activate` on macOS/Linux or `.venv\\Scripts\\Activate.ps1` in Windows PowerShell, then:

```bash
python -m pip install -r requirements.txt
python tobacco_analysis_dashboard.py --data "/path/to/The_Tax_Burden_on_Tobacco__1970-2019.csv"
```

Open **http://127.0.0.1:8060**. The CSV is supplied separately and is not committed. Pass its local path with `--data`; no Colab paths, notebook commands, or API keys are required. The app defaults to localhost with debug disabled.

### Data preparation and implementation notes

- Required raw columns: `LocationAbbr`, `Year`, `SubMeasureDesc`, and `Data_Value`.
- The loader pivots the six source measures into one row per state-year and rejects duplicate records, missing measures, nonnumeric values, and invalid prices.
- State tax share = state tax per pack / average cost per pack. Federal share = (combined federal and state tax − state tax) / average cost per pack. Shares are fractions; multiply by 100 for percentage points. The source-reported combined percentage is retained separately because rounding may differ.
- Pack sales per capita are the consumption proxy. The overview uses an unweighted mean across jurisdictions, not a population-weighted national estimate.
- Four K-means clusters retain the original dashboard's two unscaled inputs (mean state tax share and mean consumption), with `random_state=42` and explicit `n_init=10`. Consumption's larger numerical scale can dominate distances; this repair does not introduce a new clustering method.
- The seven original tabs remain, with a light/dark chart selector and a searchable, sortable data table. The binned tax-share trend is descriptive rather than a formal elasticity estimate.
- Maps use Plotly's built-in USA-state locations. Browser map rendering may require access to Plotly's geographic assets; no unused GeoJSON download blocks Python startup.
- Regression coefficients and diagnostics are documented in the final report; this dashboard repair does not reproduce that separate regression analysis.

### Project evidence

- [Original final course report](docs/CSE5520_Final_Report_Hiral_Choksi.pdf): statistical modeling, diagnostics, and visual analytics.
- [Portfolio project summary](Hiral_Choksi_Tobacco_Tax_Policy_Analysis.pdf).
- A recorded demonstration exists separately; a public video URL has not yet been added.

### Checks

```bash
python -m unittest discover -s tests -v
python tobacco_analysis_dashboard.py --help
```

Tests use synthetic data to verify reshaping, tax shares, input errors, tab generation, chart themes, comparisons, and HTTP endpoints. The supplied CSV was also checked locally without committing it. Full browser visual verification and reproduction of historical statistical results remain separate checks.


## Project Overview

This project explores how state-level tobacco taxation policies influence cigarette consumption behavior across different regions of the United States between 1990 and 2019. The analysis combines statistical trend exploration, clustering, geospatial visualization, and interactive dashboards to identify long-term behavioral patterns, regional disparities, and policy-related shifts in consumption trends.

The project was developed as an interdisciplinary quantitative analysis workflow integrating panel-style datasets, policy event analysis, and geospatial analytical methods.

---

## Research Objective

Evaluate how state-level tax policy interventions affect cigarette consumption patterns across different U.S. regions over time while examining:

* Long-term national consumption trends
* Regional disparities in smoking behavior
* Relationships between tax burden and cigarette consumption
* Temporal effects of major policy interventions
* State-level clustering patterns and policy behavior similarities

---

## Dataset Scope

### Panel Dataset

* 50 U.S. States
* 1990–2019
* 1,500+ observations

### Variables Included

* Per-capita cigarette consumption
* State tax as percentage of retail price
* Federal tax burden
* Average cigarette pack price
* Regional classifications
* Temporal policy indicators
* Derived behavioral and economic metrics

### Policy Context Considered

* 1998 Master Settlement Agreement (MSA)
* 2009 Federal Tobacco Tax Increase
* 2019 Tobacco 21 Law
* Regional taxation differences across states

---

# Research Architecture & Workflow

<p align="center">
  <img src="assets/workflow.png" width="1100">
</p>

---

## Data Preprocessing & Feature Engineering

The workflow includes:

* Multi-year panel data cleaning and validation
* State-level normalization and consistency checks
* Missing value handling and preprocessing
* Regional aggregation and mapping
* Temporal feature engineering
* Tax burden percentage calculations
* Structured dataset preparation for visualization and analysis

---

## Analytical Methods

### Statistical Analysis

* LOESS Trend Smoothing
* Correlation Analysis
* Elasticity Exploration
* Temporal Trend Analysis
* Changepoint Detection (`ruptures`)

### Machine Learning & Pattern Discovery

* K-Means Clustering
* State Pattern Grouping
* Regional Behavioral Segmentation

### Geospatial Analysis

* Choropleth Mapping
* Regional Aggregation
* Geographic Trend Analysis
* State-Level Comparative Visualization

---

## Interactive Dashboard Features

The project includes a multi-tab interactive analytical dashboard built with Plotly Dash.

### Dashboard Modules

1. National Trend Analysis
2. State Clustering Visualization
3. Geographic Map Analysis
4. Elasticity Exploration
5. State-to-State Comparison
6. Regional Pattern Analysis
7. Data Table & Summary Metrics

---

## Key Visualizations

### National Trend Analysis

LOESS-smoothed national consumption trends with policy intervention markers and changepoint detection.
<img width="975" height="548" alt="image" src="https://github.com/user-attachments/assets/dead746d-954a-4161-8aef-db1f57adddd4" />


### State Clustering Analysis

K-means clustering identifying groups of states with similar tax burden and cigarette consumption behavior.
<img width="975" height="545" alt="image" src="https://github.com/user-attachments/assets/c619ec8c-2a82-4973-a9bb-93e786c51138" />


### Geographic Distribution

Animated choropleth visualization showing temporal changes in cigarette tax burden across U.S. states.
<img width="975" height="538" alt="image" src="https://github.com/user-attachments/assets/02f18d3e-e1dd-4338-8f50-c7693ad502a8" />
<img width="975" height="541" alt="image" src="https://github.com/user-attachments/assets/0e485362-eed0-47e3-ad9c-6a11d704ab69" />


### Regional Comparisons

Interactive comparison tools highlighting regional consumption disparities and long-term behavioral trends.
<img width="975" height="533" alt="image" src="https://github.com/user-attachments/assets/c051083c-b418-40e8-bf91-36dafe02aa73" />
<img width="975" height="546" alt="image" src="https://github.com/user-attachments/assets/7e2e6fc9-0e80-42ef-be5d-d77e9c07978f" />



---

## Key Findings

* National cigarette consumption shows a clear long-term decline with observable structural shifts near major policy intervention periods.

* States cluster into distinct groups based on taxation patterns and cigarette consumption behavior.

* Higher cigarette tax burden is generally associated with lower cigarette consumption trends across states.

* Regional disparities persist despite overall national decline, with some regions maintaining consistently higher consumption patterns.

* Temporal and spatial analysis reveals both short-term and longer-term behavioral responses to policy changes.

---

## Research Relevance

This project demonstrates:

* Longitudinal panel-style data analysis
* Policy-oriented quantitative research workflows
* Geospatial analytical thinking
* Interactive research visualization
* Structured data engineering and preprocessing
* Temporal trend and intervention analysis
* Interdisciplinary analytical system design

---

## Technical Stack

### Languages & Libraries

* Python
* Pandas
* NumPy
* Plotly
* Dash

### Statistical & ML Tools

* statsmodels
* ruptures
* scikit-learn

### Geospatial Tools

* GeoJSON
* Choropleth Mapping
* Regional Aggregation

---


---

## Future Improvements

Potential extensions include:

* Difference-in-differences policy evaluation
* Additional demographic variables
* County-level geospatial analysis
* Predictive temporal modeling
* Expanded behavioral health datasets
* Integration with additional public policy indicators

---

## Author

**Hiral Choksi**
Graduate Student - M.S. Computer Science & Engineering
University of Connecticut
Graduate Research Assistant, CIRCA

GitHub: [https://github.com/HIRAL13CHOKSI](https://github.com/HIRAL13CHOKSI)



