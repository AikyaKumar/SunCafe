import requests

def fetch_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&daily=sunrise,sunset,sunshine_duration"
        f"&current=rain,wind_speed_10m,temperature_2m,cloud_cover"
        f"&timezone=Europe%2FBerlin"
    )
    response = requests.get(url)
    data = response.json()

    current = data.get("current", {})
    return {
        "Rain": current.get("rain", 0),
        "Wind Speed": current.get("wind_speed_10m", 0),
        "Temperature": current.get("temperature_2m", 0),
        "Cloud Cover": current.get("cloud_cover", 0)
    }
