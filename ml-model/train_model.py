import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

df = pd.read_csv("../data/heidelberg_cafes_sunlight.csv")

df_model = df.drop(columns=["Cafe Name", "Outdoor Seating", "Indoor Seating"])
df_model["Sunlight Status"] = df_model["Sunlight Status"].map({"Sunny": 1, "Shady": 0})
df_model = pd.get_dummies(df_model)

X = df_model.drop("Sunlight Status", axis=1)
y = df_model["Sunlight Status"]

X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open("rf_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("training_columns.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("✅ Model and columns saved.")
