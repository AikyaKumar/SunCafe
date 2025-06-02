import json
import requests
from kafka import KafkaProducer
from utils.cafe_fetcher import fetch_cafes

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

cafes = fetch_cafes()

for cafe in cafes:
    producer.send("cafe_topic", value=cafe)

producer.flush()
print("✅ All cafes sent.")
