from kafka import KafkaConsumer
import pickle
import pandas as pd
import json
from sklearn.metrics import classification_report

with open("../ml_model/rf_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("../ml_model/training_columns.pkl", "rb") as f:
    training_columns = pickle.load(f)

consumer = KafkaConsumer(
    "weather_topic",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="sunlight-predictor"
)

print("🟢 Waiting for weather data...")

for message in consumer:
    data = message.value
    df = pd.DataFrame([data])
    features = df.drop(columns=["Cafe Name", "Sunlight Status", "Outdoor Seating", "Indoor Seating"], errors="ignore")
    features = pd.get_dummies(features)

    for col in training_columns:
        if col not in features.columns:
            features[col] = 0
    features = features[training_columns]

    pred = model.predict(features)[0]
    status = "☀️ Sunny" if pred == 1 else "🌒 Shady"
    print(f"\n📍 {data.get('Cafe Name', 'Unknown Cafe')} Prediction: {status}")
