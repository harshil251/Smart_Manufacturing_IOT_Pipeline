import psycopg2
import pandas as pd
from ml.anomaly_detector import AnomalyDetector

conn = psycopg2.connect(
    database="iot_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5433"
)

query = "SELECT * FROM sensor_data"
df = pd.read_sql(query, conn)

detector = AnomalyDetector()
detector.train(df)
detector.save_model()

print("Model retrained and saved successfully!")