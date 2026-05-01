# Electric Vehicle Adoption Disparities in California

**CS 163 Capstone Project · San Jose State University · Spring 2026**

A data science investigation into why EV adoption in California is not evenly distributed — and what structural, economic, and environmental factors explain the gap.

**Live site:** [https://sp26-project-491005.wm.r.appspot.com](https://sp26-project-491005.wm.r.appspot.com)

---

## The Question

California leads the nation in EV adoption, but that adoption is concentrated. Wealthy, highly-educated communities cluster at the top while communities carrying heavier environmental and economic burdens lag behind. This project asks: why, and by how much?

We built a unified ZIP-code-level dataset spanning over 1,800 California ZIP codes, ran exploratory analysis across 34 features, fit six machine learning models, and built an interactive web application to communicate the findings.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data collection | Python, Census API, NREL Alt Fuel Stations API |
| Data processing | Pandas |
| Modeling | Scikit-learn (Ridge, Random Forest, Logistic Regression) |
| Web framework | Plotly Dash + Flask |
| Styling | Custom CSS (light/dark theme, CSS variables) |
| Deployment | Google App Engine, Gunicorn, Google Cloud Storage |
| Version control | Git + GitHub |

---

## Data Sources

Four public datasets were integrated into a single ZIP-level analytical table.

| Source | What it provides | Level |
|---|---|---|
| **CalMatters EV Dataset** | ZIP-level EV registration counts, vehicle types, Zillow home value indicators, and demographic context | ZIP code |
| **American Community Survey (ACS)** | Socioeconomic and housing variables: Gini index, housing tenure, housing structure, poverty status, vehicle availability | ZCTA |
| **CalEnviroScreen 4.0** | Environmental burden scores, pollution burden, traffic exposure, CES composite score | Census tract |
| **NREL Alt Fuel Stations API** | Public EV charging station counts, port counts, Level 2 and DC Fast ports, filtered to operational CA stations as of end of 2021 | Point location → ZIP |

---

## Data Pipeline

```
CalMatters EV Data (base layer)
        |
        v
ACS Feature Construction
  - Gini Index, housing tenure, housing structure
  - Poverty share, renter share, multi-unit share
  - Retrieved via Census API at ZCTA level
        |
        v
CalEnviroScreen Aggregation
  - Tract-level data aggregated to ZIP using population-weighted averages
  - CES 4.0 Score, Pollution Burden, Traffic Exposure
        |
        v
NREL Charging Infrastructure
  - Filtered to public, operational CA stations open by end of 2021
  - Station counts, total ports, L2 ports, DC Fast ports per ZIP
        |
        v
Final Integrated Dataset
  - 1,800+ California ZIP codes × 34 features
  - One row per ZIP, no duplicates
```

**Key pipeline decisions:**
- ZIP code used as the universal merge key across all sources
- ACS margin-of-error columns removed before feature construction
- CalEnviroScreen tract data aggregated up to ZIP via population weights (note: where tract and ZIP boundaries don't align well, this introduces some geographic imprecision)
- Infrastructure ZIPs with no charger match filled with zeros
- Derived features engineered post-merge: `RenterShare`, `MultiUnitShare`, `HomeownerShare`, `PortsPer10kPeople`, `ChargersPer1000EV`

---

## Modeling

Six machine learning models were fit to answer distinct questions about EV adoption.

### Model 1 — EV Adoption Prediction
**Question:** Which structural factors most predict EV adoption rates?  
**Approach:** Ridge Regression + Random Forest Regressor  
**Performance:** Ridge R² = 0.873, RF R² = 0.894  
**Finding:** Education level is the single strongest predictor, followed by home value and household income. Infrastructure plays a positive but secondary role.

### Model 2 — Income × Infrastructure Interaction
**Question:** Does charging infrastructure help all income groups equally?  
**Approach:** Ridge Regression with an income × infrastructure interaction term  
**Performance:** R² = 0.872  
**Finding:** The interaction term is positive — higher-income communities benefit more from each additional charger. Infrastructure investment can reinforce existing gaps rather than close them.

### Model 3 — EV Desert Classification
**Question:** Who is left behind in the EV transition?  
**Approach:** Logistic Regression + Random Forest Classifier on bottom 20% of ZIP codes by adoption  
**Performance:** Logistic AUC = 0.968, RF AUC = 0.974  
**Finding:** EV deserts are highly predictable from structural disadvantage. The communities with the least EV adoption are not randomly distributed — they cluster by education, income, and home value.

### Model 4 — Infrastructure Desert Classification
**Question:** Who lacks access to public charging?  
**Approach:** Logistic Regression + Random Forest Classifier on lowest-infrastructure ZIP codes  
**Performance:** Logistic AUC = 0.714, RF AUC = 0.692  
**Finding:** Infrastructure gaps are much harder to predict than adoption gaps. Charger placement follows investment and policy logic rather than community need.

### Model 5 — Adoption Pathway Model
**Question:** Are plug-in hybrids a stepping stone to full EV adoption?  
**Approach:** Ridge Regression + Random Forest Regressor  
**Performance:** R² = 0.943  
**Finding:** PHEV (plug-in hybrid) share is the single dominant predictor of full EV adoption. Traditional gasoline hybrid share carries a negative coefficient — it is plug-in exposure specifically that signals community readiness.

### Model 6 — High-Income Subset Analysis
**Question:** Within wealthy communities, what still explains variation?  
**Approach:** Ridge Regression on the top income quintile only  
**Finding:** Even after controlling for wealth, PHEV adoption and education remain the top differentiators. Infrastructure still contributes positively, and multi-unit housing share shows a negative coefficient.

---

## Key Findings

1. **Education is the strongest predictor.** Bachelor's degree attainment has a stronger positive association with EV adoption than income alone — consistent across every model.

2. **Socioeconomic advantage drives adoption.** Home value and household income are the next strongest predictors. EV adoption closely tracks economic and educational privilege.

3. **Environmental burden works in the opposite direction.** Communities with higher pollution burden and higher poverty rates show lower EV adoption — the places that would benefit most from cleaner transportation are the furthest behind.

4. **Infrastructure helps, but not equally.** Charging access is positively associated with adoption, but the benefit is strongest in higher-income communities. Infrastructure investments can widen gaps rather than close them if placed where demand already exists.

5. **EV deserts are highly predictable.** The bottom 20% of ZIP codes by EV adoption can be classified with very high accuracy. They are systematically concentrated in communities with lower education, housing wealth, and income.

6. **Charging deserts follow a different logic.** Infrastructure-poor ZIP codes are much harder to classify — charger placement depends on private investment, policy, and geography more than community need.

7. **Plug-in hybrids signal a transition pathway.** PHEV share is the single strongest behavioral predictor of full EV adoption. Communities already familiar with electrified vehicles are far more likely to transition.

8. **Income's effect on EV adoption is nonlinear.** A polynomial model confirms an accelerating threshold effect — once a community crosses a certain income level, adoption takes off rapidly. Lower-income communities face compounding barriers, not just a linear disadvantage.

---

## Research Questions

1. How are EV adoption rates associated with income, education, housing value, and homeownership?
2. Do communities with greater environmental burden and socioeconomic vulnerability show lower EV adoption?
3. Is the relationship between income and EV adoption nonlinear, suggesting affordability thresholds?
4. Is charging infrastructure distributed unevenly across California ZIP codes?
5. Do structural socioeconomic factors explain the racial and ethnic disparities that appear in raw EV adoption data?

---

## Project Structure

```
EV_Analysis-CS163Capstone/
├── appengine/
│   ├── app.py                  # Dash app entry point, navbar, theme toggle
│   ├── app.yaml                # App Engine deployment config
│   ├── requirements.txt        # Python dependencies
│   ├── assets/
│   │   ├── style.css           # Full custom stylesheet (light + dark themes)
│   │   └── images/             # Contributor photos
│   ├── pages/
│   │   ├── home.py             # Landing page
│   │   ├── data.py             # Data sources and pipeline page
│   │   ├── eda.py              # Exploratory data analysis page
│   │   ├── analysis.py         # Regression and structural analysis page
│   │   ├── ml.py               # Interactive ML model explorer (6 models)
│   │   └── findings.py         # Key findings, implications, limitations
│   ├── static/images/          # All visualization images
│   └── data/
│       └── final.csv           # Final integrated dataset
├── eda_analysis.ipynb          # Full EDA and modeling notebook
├── get_data.ipynb              # Data acquisition notebook
└── docs/
    └── ProjectProposal.pdf
```

---

## Running Locally

```bash
cd appengine
pip install -r requirements.txt
python app.py
```

App runs at `http://127.0.0.1:8050`.

---

## Limitations

- **Cross-sectional data only.** We observe associations but cannot establish causal direction.
- **ZIP code aggregation.** A single ZIP can span very different neighborhoods — within-ZIP variation is invisible.
- **Geographic level mismatch.** EV and demographic data are at the ZIP code level; CalEnviroScreen is at the census tract level. Aggregating tract data to ZIP using population weights introduces some noise where boundaries don't align.
- **Unobserved variables.** Consumer attitudes, dealership proximity, utility electricity rates, and available EV model options are all unobserved.
- **2021 snapshot.** EV prices have fallen and infrastructure has expanded since then — structural relationships may be shifting.

---

## Authors

### Samriddhi Matharu
B.S. Data Science, San Jose State University ('26)

Samriddhi has experience across data, software, and product roles and holds leadership positions in technical consulting on campus. She is passionate about responsible computing and using data to surface equity patterns that aggregate statistics miss. On this project, she led the data pipeline, exploratory analysis, machine learning modeling, and end-to-end web application development.

### Bhavya Vatsavayi
B.S. Data Science, San Jose State University

Bhavya has a strong background in machine learning and statistical modeling. She led the regression and ML modeling components of this project and contributed to the analytical framing of the research questions. She is passionate about applying rigorous quantitative methods to problems with real-world social implications.

---

*CS 163 Capstone · San Jose State University · Spring 2026*
