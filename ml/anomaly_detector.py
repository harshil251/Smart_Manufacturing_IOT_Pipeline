import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,  # 5% anomalies
            random_state=42
        )

    def train(self, df):
        features = df[[
            "temperature",
            "vibration",
            "pressure",
            "energy_usage"
        ]]
        self.model.fit(features)

    def predict(self, df):
        features = df[[
            "temperature",
            "vibration",
            "pressure",
            "energy_usage"
        ]]
        df["anomaly"] = self.model.predict(features)
        
        # -1 = anomaly, 1 = normal
        df["anomaly"] = df["anomaly"].apply(lambda x: "ANOMALY" if x == -1 else "NORMAL")
        return df
    
    def save_model(self, path="ml/model.pkl"):
        joblib.dump(self.model, path)
    
    def load_model(self, path="ml/model.pkl"):
        self.model = joblib.load(path)