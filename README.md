# Electric Vehicle Adoption and Infrastructure Disparities in California

**CS 163 Capstone · San Jose State University · Spring 2026**

Live Website → [sp26-project-491005.wm.r.appspot.com](https://sp26-project-491005.wm.r.appspot.com)

![Dashboard Preview](docs/preview.png)

---

## About the project

This project analyzes EV adoption and public charging infrastructure disparities across 1,800+ California ZIP codes. Using vehicle registration data, census demographics, environmental justice indicators, and charging station records, we build a unified dataset, run six ML experiments, and serve the results through an interactive web dashboard deployed on Google Cloud.

---

## About the repo
This repo contains our data acquisition, eda/analysis, and modeling notebooks, a six-model ML pipeline, a FastAPI inference service (live model) containerized for Cloud Run, and a multi-page Plotly Dash app deployed on Google App Engine — all connected through Google Cloud Storage.

---

## Research Questions

1. How are EV adoption rates associated with income, education, housing value, and homeownership?
2. Do structural socioeconomic factors explain apparent racial/ethnic disparities in adoption?
3. Is the relationship between income and EV adoption nonlinear?
4. Is charging infrastructure distributed unevenly, and does it interact with socioeconomic conditions?
5. Do communities with greater environmental burden show lower EV adoption?

---

## Pipeline

```
notebooks/get_data.ipynb          →   notebooks/eda_analysis.ipynb
(collect from 4 APIs/sources)         (clean, engineer features, surface initial insights, visualizations)
                                                  ↓
                                    notebooks/modeling.ipynb
                                    (6 ML experiments, export charts)
                                                  ↓
                                       appengine/ (Dash web app)
                                                  ↓
                              Google App Engine  +  Cloud Run (live inference)
```

**Step 1 — Data Collection** (`notebooks/get_data.ipynb`): Pull EV registrations (CalMatters/DMV), census demographics (ACS API), environmental burden scores (CalEnviroScreen 4.0), and charging station data (NREL API). Raw outputs land in `data/`.

**Step 2 — Feature Engineering, EDA & Analysis** (`notebooks/eda_analysis.ipynb`): Normalize counts to shares (`RenterShare`, `MultiUnitShare`, `PovertyShare`), aggregate CalEnviroScreen tract data to ZIP level via population-weighted averages, fill unmatched charging ZIPs with zero, and derive infrastructure features (`PortsPer10kPeople`, `ChargersPer1000EV`). Also contains our full exploratory analysis — distribution plots, correlation heatmaps, geographic visualizations, and initial regression analyses. Final integrated table: `data/final.csv`.

**Step 3 — Modeling** (`notebooks/modeling.ipynb`): Six experiments using Ridge Regression, Random Forest, and Logistic Regression. Exported charts are saved to `appengine/static/images/`.

**Step 4 — Web App** (`appengine/`): Plotly Dash multi-page app reads `final.csv` from Google Cloud Storage on startup and serves all analysis interactively.

**Step 5 — Deployment**: App Engine hosts the dashboard; Cloud Run hosts a live inference API that retrains the EV desert classifier from GCS data at each cold start.

---

## Repository Structure

```
EV_Analysis-CS163Capstone/
├── appengine/                        # Dash web app (deployed to Google App Engine)
│   ├── app.py                        # App entry point, navbar, dark/light theme
│   ├── app.yaml                      # App Engine config (runtime, scaling, env vars)
│   ├── requirements.txt
│   ├── assets/
│   │   ├── style.css                 # Custom stylesheet (light + dark themes)
│   │   └── images/                   # UI assets served at /assets/images/
│   │       ├── sam.png               # Contributor photo
│   │       ├── bhavya.png            # Contributor photo
│   │       ├── car_bg.png            # Home page background
│   │       └── forecast.png          # UI graphic
│   ├── pages/                        # One file per route
│   │   ├── home.py
│   │   ├── methods.py
│   │   ├── data.py
│   │   ├── eda.py
│   │   ├── analysis.py               # Regression analysis and interactive CA map
│   │   ├── further_analysis.py       # Extended analysis (continuation of analysis page)
│   │   ├── ml.py                     # Interactive ML model explorer (6 models)
│   │   ├── live_service.py           # Live EV Desert Predictor (calls Cloud Run)
│   │   └── findings.py
│   ├── static/images/                # Exported notebook charts served at /static/images/
│   └── data/                         # Local fallback dataset + GeoJSON map
├── inference_service/                # Logistic regression API (deployed to Cloud Run)
│   ├── main.py                       # FastAPI app: trains at startup, serves /predict
│   ├── Dockerfile
│   └── requirements.txt
├── notebooks/                        # Exploration and modeling (Jupyter)
│   ├── get_data (1).ipynb            # Data collection from APIs
│   ├── eda_analysis.ipynb            # EDA, feature engineering, analysis, visuals
│   └── modeling (1).ipynb            # ML experiments
├── data/                             # Raw and intermediate data files
│   ├── ev-zipcode-demographics.csv
│   ├── acs_extra_data.csv
│   ├── ev_acs_cal.csv
│   ├── ca_california_zip_codes_geo.min.json   # GeoJSON for CA ZIP code boundaries
│   ├── calenviroscreen40resultsdatadictionary_f_2021.xlsx  # CalEnviroScreen data dictionary
│   ├── final.csv                     # Final merged dataset
│   └── final_clean.csv               # Cleaned version of final dataset
└── docs/                             # README images and project documents (not served by app)
    ├── preview.png
    └── ML_demopic.png
```

---

## Setup

**Prerequisites:** Python 3.10+, pip

```bash
git clone https://github.com/samriddhi-m1227/EV_Analysis-CS163Capstone.git
cd EV_Analysis-CS163Capstone/appengine
pip install -r requirements.txt
python app.py
# → http://127.0.0.1:8050
```

> The app loads `final.csv` from Google Cloud Storage on startup. If GCS credentials aren't configured locally, it falls back to the copy in `appengine/data/` automatically — no extra setup needed.

To explore or re-run the analysis, open the notebooks in Colab in order: `get_data` → `eda_analysis` → `modeling`. The final merged dataset (`data/final.csv`) is already included in the repo, so you can run `eda_analysis` and `modeling` directly without needing any API keys. API keys (Census, NREL) are only required if you want to re-collect the raw data from scratch via `get_data`.

---

## System Design

```
                        User (Browser)
                              │
                              ▼
              ┌─── Google App Engine ───────────────┐
              │  Dash / Flask (appengine/app.py)     │
              │  - Serves all dashboard pages        │
              │  - Reads dataset from GCS on start   │
              └──────────┬──────────────┬────────────┘
                         │              │
                         ▼              ▼
            Google Cloud Storage    Google Cloud Run
            (ev-analysis-data-cs163) (inference_service/)
            final.csv, assets         POST /predict
                                   (logistic regression)
```

**How the components connect:**
- The App Engine app loads `final.csv` directly from Google Cloud Storage at startup using the `google-cloud-storage` SDK, so no CSV is bundled into the container image.
- When a user submits inputs on the Live Service page, the Dash callback POSTs to the Cloud Run `/predict` endpoint, which returns a classification and probability in real time.
- Cloud Run also reads `final.csv` from GCS and retrains the logistic regression classifier at each cold start — no model artifact needs to be stored or versioned separately.

**Scalability:**
- App Engine is configured with `instance_class: F2` (512MB RAM, 1.2GHz CPU) and `automatic_scaling` (`target_cpu_utilization: 0.65`, `min_instances: 1`, `max_instances: 3`). A minimum of 1 instance is kept warm to eliminate cold start delays, and the cluster scales up to 3 instances under load.
- Cloud Run is fully serverless and scales to zero when idle, each inference request is stateless and handled independently.
- GCS decouples data from compute: updating the dataset requires only re-uploading `final.csv` to the bucket; neither service needs redeployment.

---

## Inference Service

**Location:** `inference_service/main.py` · `inference_service/Dockerfile`

The inference service is a FastAPI application deployed to Google Cloud Run. On startup it downloads `final.csv` from GCS, fits a `StandardScaler` and `LogisticRegression` classifier (scikit-learn), and holds the trained objects in memory. No model artifact is persisted — the model re-trains from the data at each cold start (~1 second).

**Why Logistic Regression:** Produces well-calibrated probabilities, is interpretable, trains instantly, and achieves 0.968 AUC on this task — comparatively competitive with the Random Forest (0.974 AUC).

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Returns `{"status": "ok", "model_ready": true}` |
| `POST` | `/predict` | Accepts 6  features, returns classification + probabilities |

**Input (JSON body):**
```json
{
  "Median_Household_Income": 75000,
  "BachOrHigher_perc": 30,
  "PovertyShare": 0.15,
  "RenterShare": 0.50,
  "CES_Score_ZIP": 50,
  "Total_Ports": 10
}
```

**Output:**
```json
{
  "ev_desert": true,
  "label": "EV Desert",
  "probability_ev_desert": 0.823,
  "probability_not_desert": 0.177
}
```

---

## Cloud Data

**Bucket:** `ev-analysis-data-cs163` (Google Cloud Storage)

| File | Description | How it's used |
|------|-------------|---------------|
| `final.csv` | 1,800+ ZIP codes × 34 features — the fully merged analytical dataset | Loaded by App Engine at startup for all dashboard pages; loaded by Cloud Run to train the inference model |

The App Engine app uses the `google-cloud-storage` Python SDK to stream the file at startup. If GCS is unreachable (e.g., local development), both services fall back to a local copy of `final.csv` in `appengine/data/` and `inference_service/` respectively.

---

## ML Models

| # | Model | Type | Question |
|---|-------|------|----------|
| 1 | EV Adoption Prediction | Ridge + Random Forest | Which factors most predict EV adoption? |
| 2 | Income × Infrastructure Interaction | Ridge w/ Interaction | Does infrastructure help all income groups equally? |
| 3 | EV Desert Classification | Logistic + RF Classifier | Who is left behind in the EV transition? |
| 4 | Infrastructure Desert Classification | Logistic + RF Classifier | Who lacks access to public charging? |
| 5 | Adoption Pathway Model | Ridge + Random Forest | Are plug-in hybrids a stepping stone to full EVs? |
| 6 | High-Income Subset Analysis | Ridge Regression | Within wealthy areas, what still explains variation? |

Full model details, coefficient plots, and feature importance charts are in the [ML section of the dashboard](https://sp26-project-491005.wm.r.appspot.com/ml).

---

## Key Findings

1. **Education is the strongest predictor** — consistent across every model.
2. **EV deserts are highly predictable** — the bottom 20% by adoption cluster tightly around structural disadvantage (AUC 0.968).
3. **Infrastructure reinforces advantage** — charging access has a stronger effect in higher-income areas, potentially widening gaps.
4. **Charging deserts follow different logic** — infrastructure placement (AUC 0.714) is far harder to predict than adoption, reflecting private investment and policy decisions rather than community need.
5. **PHEV adoption signals EV readiness** — plug-in hybrid share is the single strongest vehicle predictor of full EV adoption.

---

## Data Sources

| Source | What it provides |
|--------|-----------------|
| [CalMatters EV Dataset](https://calmatters.org/environment/2023/03/california-electric-cars-demographics/) | ZIP-level EV registrations, adoption rate, income, education, home value |
| [ACS 5-Year Estimates](https://www.census.gov/data/developers/data-sets/acs-5year.html) | Poverty rate, housing tenure, unit type, vehicle availability |
| [CalEnviroScreen 4.0](https://oehha.ca.gov/calenviroscreen) | Pollution burden, traffic exposure, environmental disadvantage score |
| [NREL Alt Fuel Stations API](https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/) | Public EV charging station locations and port counts |

---

## Limitations

- **Cross-sectional** — associations are observable but causal direction cannot be established.
- **ZIP code aggregation** — within-ZIP variation is invisible to the model.
- **Geographic mismatch** — CalEnviroScreen is tract-level; population-weighted aggregation to ZIP introduces noise.
- **2021 snapshot** — EV prices and infrastructure have changed significantly since then.

---

## Authors

### Samriddhi Matharu
<img src="appengine/assets/images/sam.png" alt="Samriddhi Matharu" width="120" style="border-radius:50%"/>

B.S. Data Science, San Jose State University ('26)

Samriddhi has experience across data, software, and product roles and holds leadership positions in technical consulting on campus. On this project, she led the data pipeline, exploratory analysis, machine learning modeling, and end-to-end web application development.

[LinkedIn](https://www.linkedin.com/in/samriddhi-matharu-827082235/)

### Bhavya Vatsavayi
<img src="appengine/assets/images/bhavya.png" alt="Bhavya Vatsavayi" width="120" style="border-radius:50%"/>

B.S. Data Science, San Jose State University ('26)

Bhavya has experience across data analytics, BI, and ML focused roles and holds leadership roles in research and analytics. On this project, she led the further analysis and contributed to exploratory data analysis, supporting the development and validation of the machine learning models.

[LinkedIn](https://www.linkedin.com/in/bhavyapreethika/)

---

*CS 163 Capstone · San Jose State University · Spring 2026*
