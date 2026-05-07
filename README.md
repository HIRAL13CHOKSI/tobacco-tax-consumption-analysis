# Tobacco Tax & Consumption Analysis (U.S., 1990–2019)

An applied policy analytics and geospatial data analysis project examining the relationship between cigarette taxation and tobacco consumption trends across U.S. states over a 30-year period.

---

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/e489cce9-2956-4fb1-b9f6-36199f49a538" />

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


