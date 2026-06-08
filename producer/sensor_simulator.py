import random
import time
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_sensor_data():
    return {
        "machine_id": random.randint(1, 10),
        "temperature": round(random.uniform(50, 120), 2),
        "vibration": round(random.uniform(0.1, 5.0), 2),
        "pressure": round(random.uniform(10, 100), 2),
        "energy_usage": round(random.uniform(100, 1000), 2),
        "timestamp": time.time()
    }

while True:
    data = generate_sensor_data()
    producer.send('iot-sensors', data)
    print("Sent:", data)
    time.sleep(2)