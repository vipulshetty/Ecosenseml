import joblib
import pandas as pd
import os

# Load model
model_path = "plant_health_rf.pkl"
if not os.path.exists(model_path):
    print("❌ Model not found! Please run create_dummy_model.py first.")
    exit()

print(f"✅ Loading model from {model_path}...")
model = joblib.load(model_path)

def test_prediction(soil, temp, hum, light, case_name):
    print(f"\n--- Testing Case: {case_name} ---")
    print(f"📥 Inputs: Soil={soil}%, Temp={temp}°C, Hum={hum}%, Light={light} lux")

    # 1. Predict NPK
    df = pd.DataFrame([{
        "SoilMoisture": soil,
        "Temperature": temp,
        "Humidity": hum,
        "Light": light
    }])

    npk_pred = model.predict(df)[0]
    nitrogen, phosphorus, potassium = npk_pred[0], npk_pred[1], npk_pred[2]

    print(f"🔮 Predicted NPK: Nitrogen={nitrogen:.2f}, Phosphorus={phosphorus:.2f}, Potassium={potassium:.2f}")

    # 2. Determine Status (Logic copied from plant_monitor.py)
    status = "🌱 PLANT IS HEALTHY"
    detail = "All environmental conditions are within optimal range."

    if soil < 20:
        status = "⚠ SOIL TOO DRY — WATER REQUIRED"
    elif soil > 80:
        status = "⚠ SOIL TOO WET — REDUCE WATERING"
    elif light < 200:
        status = "⚠ INSUFFICIENT LIGHT"
    elif nitrogen < 20:
        status = "⚠ LOW NITROGEN — ADD FERTILIZER"
    elif phosphorus < 20:
        status = "⚠ LOW PHOSPHORUS — ADD FERTILIZER"
    elif potassium < 20:
        status = "⚠ LOW POTASSIUM — ADD FERTILIZER"
    
    print(f"📋 Status: {status}")

# Test Cases
test_prediction(50, 25, 60, 1000, "Ideal Conditions")
test_prediction(10, 28, 30, 1200, "Dry Soil")
test_prediction(45, 24, 65, 900, "Low Nitrogen Scenario (Simulated)")
