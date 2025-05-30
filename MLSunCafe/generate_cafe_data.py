import random
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import math

fake = Faker()

HEIDELBERG_LAT = 49.3988
HEIDELBERG_LON = 8.6724

def day_of_year(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.timetuple().tm_yday

def approximate_sun_times(day_of_year):
    sunrise = datetime.strptime("05:00", "%H:%M") + timedelta(minutes=60 * math.cos(2 * math.pi * (day_of_year - 172) / 365))
    sunset = datetime.strptime("21:30", "%H:%M") - timedelta(minutes=60 * math.cos(2 * math.pi * (day_of_year - 172) / 365))
    return sunrise.strftime("%H:%M"), sunset.strftime("%H:%M")

def generate_random_time():
    hour = random.randint(6, 20)
    minute = random.choice([0, 15, 30, 45])
    return f"{hour:02}:{minute:02}"

def estimate_solar_angle(lat, time_str, doy):
    hour = int(time_str.split(':')[0])
    angle = max(0, 90 * math.cos((hour - 12) * math.pi / 12) * math.sin(2 * math.pi * (doy - 80) / 365))
    return round(angle, 2)

def generate_weather_data(time_str):
    hour = int(time_str.split(':')[0])
    temperature = round(random.normalvariate(18 if 10 < hour < 16 else 14, 4), 1)
    humidity = random.randint(40, 90)
    cloud_cover = random.randint(0, 100)
    sunshine = max(0, 60 - cloud_cover + random.randint(-10, 10))
    wind_speed = round(random.uniform(0, 15), 1)
    condition = random.choices(['Clear', 'Fog', 'Rain', 'Cloudy'], weights=[0.5, 0.1, 0.2, 0.2])[0]
    is_cloudy = 'Yes' if cloud_cover > 50 else 'No'
    return temperature, humidity, cloud_cover, sunshine, wind_speed, condition, is_cloudy

def determine_sunlight_status(outdoor_seating, cloud_cover, solar_angle, time_str, sunrise, sunset):
    if outdoor_seating == "No":
        return "Shady"
    if cloud_cover > 50 or solar_angle < 15:
        return "Shady"
    time_val = datetime.strptime(time_str, "%H:%M")
    if time_val < datetime.strptime(sunrise, "%H:%M") or time_val > datetime.strptime(sunset, "%H:%M"):
        return "Shady"
    return "Sunny"

def generate_cafe_data(num_records=1500):
    data = []
    orientations = ['North', 'South', 'East', 'West']
    cafe_name_templates = [
        "Cafe {}", "{} Café", "Café {}", "{} Coffee", "{} Roasters", "{} Brew House",
        "Cafe de {}", "{} Espresso", "{} Beans", "The {} Cafe"
    ]
    name_words = [
        "Rossi", "Deer", "Oak", "Willow", "Cedar", "Elm", "Pine", "Maple", "Valley", "River",
        "Brook", "Stream", "Hill", "Meadow", "Forest", "Cliff", "Stone", "Rock", "Moss", "Flint",
        "Bloom", "Petal", "Fern", "Vine", "Sun", "Moon", "Luna", "Cloud", "Rain", "Storm",
        "Sky", "Aurora", "Mist", "Haze", "Dawn", "Twilight", "Breeze", "Zephyr", "Fog", "Star",
        "Nova", "Haven", "Nest", "Nook", "Den", "Alcove", "Loft", "Gallery", "Studio", "Atelier",
        "Porch", "Hearth", "Lantern", "Chalet", "Cabin", "Barn", "Heidel", "Berg", "Alba", "Berlin",
        "Vienna", "Zurich", "Mont", "Grove", "Soho", "Borough", "Station", "Depot", "Harbor", "Bay",
        "Quay", "Corner", "Bean", "Brew", "Grind", "Roast", "Espresso", "Cocoa", "Caramel",
        "Vanilla", "Cinnamon", "Hazel", "Choco", "Latte", "Crema", "Macchiato", "Mochi", "Echo",
        "Drift", "Pulse", "Muse", "Verse", "Frame", "Hollow", "Velvet", "Silk", "Brass", "Marble",
        "Obsidian", "Indigo", "Amber", "Coral", "Onyx"
    ]

    for _ in range(num_records):
        cafe_name = random.choice(cafe_name_templates).format(random.choice(name_words))
        outdoor_seating = random.choice(["Yes", "No"])
        indoor_seating = random.choice(["Yes", "No"])
        latitude = round(np.random.normal(HEIDELBERG_LAT, 0.005), 6)
        longitude = round(np.random.normal(HEIDELBERG_LON, 0.005), 6)
        orientation = random.choice(orientations)
        date = fake.date_between(start_date='-2y', end_date='today').strftime("%Y-%m-%d")
        time_of_day = generate_random_time()
        doy = day_of_year(date)
        sunrise, sunset = approximate_sun_times(doy)
        solar_angle = estimate_solar_angle(latitude, time_of_day, doy)
        temperature, humidity, cloud_cover, sunshine, wind_speed, condition, is_cloudy = generate_weather_data(time_of_day)
        sunlight_status = determine_sunlight_status(outdoor_seating, cloud_cover, solar_angle, time_of_day, sunrise, sunset)

        data.append({
            "Cafe Name": cafe_name,
            "Outdoor Seating": outdoor_seating,
            "Indoor Seating": indoor_seating,
            "Latitude": latitude,
            "Longitude": longitude,
            "Orientation": orientation,
            "Date": date,
            "Day of Year": doy,
            "Time of Day": time_of_day,
            "Sunrise Time": sunrise,
            "Sunset Time": sunset,
            "Solar Angle (°)": solar_angle,
            "Temperature (°C)": temperature,
            "Humidity (%)": humidity,
            "Cloud Cover (%)": cloud_cover,
            "Sunshine Duration (min)": sunshine,
            "Wind Speed (km/h)": wind_speed,
            "Weather Condition": condition,
            "Is Cloudy": is_cloudy,
            "Sunlight Status": sunlight_status
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Force a 75% Sunny, 25% Shady distribution
    current_sunny = df[df["Sunlight Status"] == "Sunny"]
    current_shady = df[df["Sunlight Status"] == "Shady"]

    target_sunny_count = int(len(df) * 0.75)
    target_shady_count = len(df) - target_sunny_count

    if len(current_sunny) > target_sunny_count:
        excess_sunny = current_sunny.sample(n=len(current_sunny) - target_sunny_count, random_state=42)
        df.loc[excess_sunny.index, "Sunlight Status"] = "Shady"
    elif len(current_sunny) < target_sunny_count:
        shortage_sunny = current_shady.sample(n=target_sunny_count - len(current_sunny), random_state=42)
        df.loc[shortage_sunny.index, "Sunlight Status"] = "Sunny"

    return df

# Generate and save
df = generate_cafe_data(1500)
df.to_csv("heidelberg_cafes_sunlight.csv", index=False)
print("Enhanced dataset with 1500 records saved to 'heidelberg_cafes_sunlight.csv'")
