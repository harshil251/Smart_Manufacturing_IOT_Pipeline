import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.anomaly_detector import AnomalyDetector
import json
from kafka import KafkaConsumer
import psycopg2
import pandas as pd

# Kafka Consumer
consumer = KafkaConsumer(
    'iot-sensors',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# PostgreSQL Connection
conn = psycopg2.connect(
    database="iot_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5433"
)

cursor = conn.cursor()

# ML Setup
detector = AnomalyDetector()
buffer = []

# Stream Processing
for message in consumer:
    data = message.value

    buffer.append(data)

    # Run ML when buffer fills
    if len(buffer) >= 20:
        df = pd.DataFrame(buffer)

        detector.train(df)
        result = detector.predict(df)

        latest = result.iloc[-1]
        anomaly = latest["anomaly"]

        # Insert ALL rows with anomaly label
        for _, row in result.iterrows():
            cursor.execute("""
                INSERT INTO sensor_data (
                    machine_id,
                    temperature,
                    vibration,
                    pressure,
                    energy_usage,
                    timestamp,
                    anomaly
                ) VALUES (%s,%s,%s,%s,%s,to_timestamp(%s),%s)
            """, (
                row['machine_id'],
                row['temperature'],
                row['vibration'],
                row['pressure'],
                row['energy_usage'],
                row['timestamp'],
                row['anomaly']
            ))

        conn.commit()

        if anomaly == "ANOMALY":
            print("ALERT: Machine anomaly detected!", latest.to_dict())
        else:
            print("Normal behavior")

        buffer = []