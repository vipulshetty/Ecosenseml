import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import joblib
import os

# Define dummy data to train a model that predicts NPK from environmental factors
# Inputs: SoilMoisture, Temperature, Humidity, Light
# Outputs: Nitrogen, Phosphorus, Potassium
data = [
    # Soil, Temp, Hum, Light,  N,  P,  K
    [50,    25,   60,  1000,   40, 50, 60], # Ideal conditions -> Balanced NPK
    [10,    25,   30,  1000,   10, 20, 30], # Dry/Poor soil -> Low NPK
    [90,    25,   80,  1000,   30, 40, 50], # Wet -> Diluted/Leached? (Just dummy data)
    [50,    25,   60,  100,    40, 50, 60], # Low light -> NPK might still be normal
    [45,    24,   65,  900,    35, 45, 55],
    [15,    28,   20,  1200,   15, 25, 35],
    [85,    22,   85,  800,    30, 40, 50],
    [55,    23,   62,  50,     40, 50, 60]
]

df = pd.DataFrame(data, columns=["SoilMoisture", "Temperature", "Humidity", "Light", "Nitrogen", "Phosphorus", "Potassium"])

X = df[["SoilMoisture", "Temperature", "Humidity", "Light"]]
y = df[["Nitrogen", "Phosphorus", "Potassium"]]

# Train model (Multi-output Regression)
# We use RandomForestRegressor wrapped in MultiOutputRegressor (though RF supports multi-output natively, this is explicit)
regr = MultiOutputRegressor(RandomForestRegressor(n_estimators=10, random_state=42))
regr.fit(X, y)

# Save model
model_path = "plant_health_rf.pkl"
joblib.dump(regr, model_path)

print(f"✅ Dummy NPK-predictor model created successfully at: {os.path.abspath(model_path)}")
