import io
import os

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

app = FastAPI(title="EV Desert Classifier")

GCS_BUCKET = "ev-analysis-data-cs163"
GCS_BLOB = "final.csv"

FEATURES = [
    "Median_Household_Income",
    "BachOrHigher_perc",
    "PovertyShare",
    "RenterShare",
    "CES_Score_ZIP",
    "Total_Ports",
]

model: LogisticRegression = None
scaler: StandardScaler = None


def load_data() -> pd.DataFrame:
    try:
        from google.cloud import storage
        client = storage.Client()
        data = client.bucket(GCS_BUCKET).blob(GCS_BLOB).download_as_bytes()
        return pd.read_csv(io.BytesIO(data))
    except Exception:
        local = os.path.join(os.path.dirname(__file__), "final.csv")
        return pd.read_csv(local)


@app.on_event("startup")
def train():
    global model, scaler
    df = load_data()
    df = df.dropna(subset=FEATURES + ["EV_perc"])

    threshold = df["EV_perc"].quantile(0.20)
    y = (df["EV_perc"] <= threshold).astype(int)
    X = df[FEATURES]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression(max_iter=1000, C=1.0)
    model.fit(X_scaled, y)
    print(f"Model trained on {len(df)} ZIP codes. EV desert threshold: {threshold:.4f}")


class Features(BaseModel):
    Median_Household_Income: float
    BachOrHigher_perc: float
    PovertyShare: float
    RenterShare: float
    CES_Score_ZIP: float
    Total_Ports: float


@app.get("/health")
def health():
    return {"status": "ok", "model_ready": model is not None}


@app.post("/predict")
def predict(features: Features):
    X = [[
        features.Median_Household_Income,
        features.BachOrHigher_perc,
        features.PovertyShare,
        features.RenterShare,
        features.CES_Score_ZIP,
        features.Total_Ports,
    ]]
    X_scaled = scaler.transform(X)
    pred = int(model.predict(X_scaled)[0])
    proba = model.predict_proba(X_scaled)[0]
    return {
        "ev_desert": bool(pred),
        "label": "EV Desert" if pred else "Not an EV Desert",
        "probability_ev_desert": round(float(proba[1]), 4),
        "probability_not_desert": round(float(proba[0]), 4),
    }
