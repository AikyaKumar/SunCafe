import json
import sys
from kafka import KafkaProducer
from utils.weather_fetcher import fetch_weather

cafe = json.loads(sys.argv[1])  # Pass JSON cafe dict as arg

weather_data = fetch_weather(cafe["lat"], cafe["lon"])
weather_data.update(cafe)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

producer.send("weather_topic", value=weather_data)
producer.flush()
print("✅ Weather data sent for selected cafe.")
