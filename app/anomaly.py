import pandas as pd
from sklearn.ensemble import IsolationForest
from app.config import CSV_PATH

def detect_anomalies():
    df = pd.read_csv(CSV_PATH)
    if len(df) < 10:
        return []
    model = IsolationForest(contamination=0.15, random_state=42)
    df["anomaly"] = model.fit_predict(df[["Average"]])
    return df[df["anomaly"] == -1]
