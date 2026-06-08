CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    machine_id INT,
    temperature FLOAT,
    vibration FLOAT,
    pressure FLOAT,
    energy_usage FLOAT,
    timestamp TIMESTAMP
);