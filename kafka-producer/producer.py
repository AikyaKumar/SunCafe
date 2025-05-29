# producer/producer.py
import json
import time
import requests
from kafka import KafkaProducer

API_KEY = 'f9a9bee312967b7fe92d64655cb08fde'
CITY = 'Heidelberg'
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'weather_updates'

while True:
    try:
        res = requests.get(URL)
        data = res.json()
        message = {
            'temp': data['main']['temp'],
            'clouds': data['clouds']['all'],
            'timestamp': time.time()
        }
        print(f"Produced: {message}")
        producer.send("weather_updates", json.dumps(data).encode("utf-8"))
        time.sleep(10)  # every 10 seconds
    except Exception as e:
        print(f"Error fetching/sending: {e}")
        time.sleep(10)
