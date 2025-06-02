import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# Load cafe and prediction data
DATA_PATH = os.path.join("..", "data", "heidelberg_cafes_sunlight.csv")
df = pd.read_csv(DATA_PATH)

# Page configuration
st.set_page_config(page_title="☀️ SunCafe Dashboard", layout="wide")
st.title("☕ Heidelberg SunCafe Map")
st.markdown("Visualizing cafe sunlight predictions in real-time 🌞🌑")

# Initialize folium map
map_center = [49.4077, 8.6908]  # Heidelberg center
m = folium.Map(location=map_center, zoom_start=14)

# Emoji representation
def get_status_emoji(status):
    return "☀️" if status == "Sunny" else "🌒"

# Add cafe markers to the map
for _, row in df.iterrows():
    name = row["Cafe Name"]
    lat = row["Latitude"]
    lon = row["Longitude"]
    status = row.get("Sunlight Status", "Unknown")
    emoji = get_status_emoji(status)
    
    popup = f"<b>{name}</b><br>{emoji} {status}"
    folium.Marker([lat, lon], popup=popup, tooltip=name, icon=folium.Icon(color="orange" if status == "Sunny" else "gray")).add_to(m)

# Render map
st_data = st_folium(m, width=900, height=600)

st.markdown("✅ Click on a cafe marker to view its name and predicted sunlight status.")
