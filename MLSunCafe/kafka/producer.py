import pandas as pd
import json
from kafka import KafkaProducer
import os

print("Starting Kafka producer...")

DATA_PATH = os.path.join("..", "data", "heidelberg_cafes_sunlight.csv")
KAFKA_TOPIC = "cafe_sunlight_data"
KAFKA_BROKER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

df = pd.read_csv(DATA_PATH)
print(f"Data loaded, total records: {len(df)}")

for i, (_, row) in enumerate(df.iterrows(), 1):
    message = row.to_dict()
    producer.send(KAFKA_TOPIC, message)
    if i % 100 == 0 or i == len(df):
        print(f"Sent {i}/{len(df)} messages")

producer.flush()
producer.close()

print("All messages sent!")
