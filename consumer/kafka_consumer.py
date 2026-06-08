import json
from kafka import KafkaConsumer
import psycopg2

consumer = KafkaConsumer(
    'iot-sensors',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = psycopg2.connect(
    database="iot_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5433"
)

cursor = conn.cursor()

for message in consumer:
    data = message.value

    cursor.execute("""
        INSERT INTO sensor_data (
            machine_id,
            temperature,
            vibration,
            pressure,
            energy_usage,
            timestamp
        ) VALUES (%s,%s,%s,%s,%s,to_timestamp(%s))
    """, (
        data['machine_id'],
        data['temperature'],
        data['vibration'],
        data['pressure'],
        data['energy_usage'],
        data['timestamp']
    ))

    conn.commit()
    print("Inserted into DB:", data)