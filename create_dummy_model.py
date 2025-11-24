import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Define dummy data to train a simple model
# Features: SoilMoisture, Temperature, Humidity, Light
data = [
    [50, 25, 60, 1000, "HEALTHY"],
    [10, 25, 30, 1000, "DRY_SOIL"],
    [90, 25, 80, 1000, "OVERWATERED"],
    [50, 25, 60, 100,  "LOW_LIGHT"],
    [45, 24, 65, 900,  "HEALTHY"],
    [15, 28, 20, 1200, "DRY_SOIL"],
    [85, 22, 85, 800,  "OVERWATERED"],
    [55, 23, 62, 50,   "LOW_LIGHT"]
]

df = pd.DataFrame(data, columns=["SoilMoisture", "Temperature", "Humidity", "Light", "Status"])

X = df[["SoilMoisture", "Temperature", "Humidity", "Light"]]
y = df["Status"]

# Train model
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X, y)

# Save model
model_path = "plant_health_rf.pkl"
joblib.dump(clf, model_path)

print(f"✅ Dummy model created successfully at: {os.path.abspath(model_path)}")
