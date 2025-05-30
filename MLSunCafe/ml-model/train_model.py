import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "heidelberg_cafes_sunlight.csv")
MODEL_DIR = os.path.join(BASE_DIR)
MODEL_PATH = os.path.join(MODEL_DIR, "rf_model.pkl")
COLUMNS_PATH = os.path.join(MODEL_DIR, "training_columns.pkl")

# ✅ Ensure model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

# Drop non-predictive columns
df_model = df.drop(columns=["Cafe Name", "Outdoor Seating", "Indoor Seating"])

# Encode target
df_model["Sunlight Status"] = df_model["Sunlight Status"].map({"Sunny": 1, "Shady": 0})

# One-hot encode categorical features
df_model = pd.get_dummies(df_model)

# Split into features and target
X = df_model.drop(columns=["Sunlight Status"])
y = df_model["Sunlight Status"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.2%}")

# Optional: Detailed report
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Shady", "Sunny"]))

# Save model and columns
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

with open(COLUMNS_PATH, "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print(f"\n✅ Model saved to {MODEL_PATH}")
print(f"✅ Training columns saved to {COLUMNS_PATH}")
