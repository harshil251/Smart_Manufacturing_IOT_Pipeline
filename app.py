import streamlit as st
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    database="iot_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5433"
)

st.title("🏭 Smart Manufacturing IoT Dashboard")

query = "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 100"
df = pd.read_sql(query, conn)

st.subheader("Latest Sensor Data")
st.dataframe(df)

st.subheader("Temperature Trend")
st.line_chart(df['temperature'])

st.subheader("Vibration Trend")
st.line_chart(df['vibration'])