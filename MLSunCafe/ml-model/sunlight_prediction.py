# ml_model/sunlight_prediction.py

from kafka import KafkaConsumer
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import pickle
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "rf_model.pkl")
COLUMNS_PATH = os.path.join(BASE_DIR, "training_columns.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(COLUMNS_PATH, "rb") as f:
    training_columns = pickle.load(f)

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'cafe_sunlight_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='sunlight-prediction-group'
)

print("✅ Listening for messages on 'cafe_sunlight_data'...")

# Process each message
for message in consumer:
    data = message.value
    print(f"\n📥 Received message: {data['Cafe Name']} at {data['Time of Day']} on {data['Date']}")

    # Prepare data for model
    try:
        df = pd.DataFrame([data])
        features = df.drop(columns=["Cafe Name", "Outdoor Seating", "Indoor Seating", "Sunlight Status", "Weather Condition"], errors="ignore")

        # One-hot encode categorical features
        features = pd.get_dummies(features)

        # Add missing columns as zeros to avoid fragmentation and ensure all training columns are present
        missing_cols = [col for col in training_columns if col not in features.columns]
        if missing_cols:
            missing_df = pd.DataFrame(0, index=features.index, columns=missing_cols)
            features = pd.concat([features, missing_df], axis=1)

        # Reorder columns to match training columns exactly
        features = features[training_columns]

        # Make prediction
        pred = model.predict(features)[0]
        result = "☀️ Sunny" if pred == 1 else "🌒 Shady"
        print(f"✅ Prediction for {data['Cafe Name']}: {result}")
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
