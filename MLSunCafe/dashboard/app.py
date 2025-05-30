import streamlit as st
import pandas as pd
import pickle
import os
import folium
from streamlit_folium import st_folium

# Paths
MODEL_PATH = os.path.join("..", "ml-model", "rf_model.pkl")
COLUMNS_PATH = os.path.join("..", "ml-model", "training_columns.pkl")
DATA_PATH = os.path.join("..", "data", "heidelberg_cafes_sunlight.csv")

# Load model and training columns
@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(COLUMNS_PATH, "rb") as f:
        training_columns = pickle.load(f)
    return model, training_columns

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

model, training_columns = load_model()
df = load_data()

st.title("☕ Heidelberg Cafe Sunlight Predictor with Map Visualization")
st.write("Enter a cafe name to check if it’s sunny or shady, and see all cafes on the map!")

# Input box for cafe name search
cafe_name_input = st.text_input("Enter Cafe Name:")

def get_sunlight_emoji(status):
    if status == "Sunny" or status == 1:
        return "☀️"
    else:
        return "🌥️"

# Show prediction for input cafe
if cafe_name_input:
    matches = df[df["Cafe Name"].str.contains(cafe_name_input, case=False, na=False)]

    if matches.empty:
        st.error(f"No matching cafe found for '{cafe_name_input}'.")
    else:
        latest = matches.sort_values("Date").iloc[-1]

        st.subheader(f"📋 Latest Record for {latest['Cafe Name']}:")
        st.write(latest)

        # Prepare features for prediction
        features = latest.drop(labels=[
            "Cafe Name", "Outdoor Seating", "Indoor Seating", "Sunlight Status", "Weather Condition"
        ], errors='ignore')
        features = pd.DataFrame([features])
        features = pd.get_dummies(features)

        # Add missing columns with zeros
        missing_cols = [col for col in training_columns if col not in features.columns]
        if missing_cols:
            missing_df = pd.DataFrame(0, index=features.index, columns=missing_cols)
            features = pd.concat([features, missing_df], axis=1)

        # Ensure the order of columns matches training columns
        features = features[training_columns]

        # Predict sunlight
        prediction = model.predict(features)[0]
        result_text = "☀️ Sunny" if prediction == 1 else "🌥️ Shady"
        st.success(f"Prediction for '{latest['Cafe Name']}': **{result_text}**")

# -------- Folium Map Section ---------

st.subheader("🗺️ Heidelberg Cafes Map")

# Initialize map centered roughly on Heidelberg
map_center = [49.3988, 8.6724]
m = folium.Map(location=map_center, zoom_start=13)

# Add markers for all cafes with coffee cup icon and popup showing sunlight status + temp
for idx, row in df.iterrows():
    # FontAwesome coffee icon (brown color)
    icon = folium.Icon(icon="coffee", prefix="fa", color="brown")

    # Popup content with emoji
    sunlight_emoji = get_sunlight_emoji(row["Sunlight Status"])
    popup_html = f"""
    <b>{row['Cafe Name']}</b><br>
    Sunlight: {row['Sunlight Status']} {sunlight_emoji}<br>
    Temperature: {row['Temperature (°C)']} °C
    """

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(popup_html, max_width=300),
        icon=icon,
        tooltip=row["Cafe Name"]
    ).add_to(m)

# Render the folium map in Streamlit
st_folium(m, width=700, height=500)
