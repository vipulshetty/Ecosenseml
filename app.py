from flask import Flask, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
READ_API_KEY = "E6MTY3AFE7C0LQI6"
CHANNEL_ID = "3173091"
MODEL_PATH = "plant_health_rf.pkl"

# Load Model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded from {MODEL_PATH}")
else:
    print("❌ Model not found! Please run create_dummy_model.py first.")
    model = None

def get_plant_status(soil, temp, hum, light, nitrogen, phosphorus, potassium):
    """Determine plant status based on rules."""
    status = "HEALTHY"
    detail = "All conditions are optimal."

    if soil < 20:
        status = "DRY_SOIL"
        detail = "Soil moisture is too low."
    elif soil > 80:
        status = "OVERWATERED"
        detail = "Soil is too wet."
    elif light < 200:
        status = "LOW_LIGHT"
        detail = "Insufficient light."
    elif nitrogen < 20:
        status = "LOW_NITROGEN"
        detail = "Nitrogen levels are low."
    elif phosphorus < 20:
        status = "LOW_PHOSPHORUS"
        detail = "Phosphorus levels are low."
    elif potassium < 20:
        status = "LOW_POTASSIUM"
        detail = "Potassium levels are low."
    
    return status, detail

@app.route('/api/plant-status', methods=['GET'])
def plant_status():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # 1. Fetch data from ThingSpeak
        url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"
        params = {"api_key": READ_API_KEY, "results": 1}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        
        feeds = data.get("feeds", [])
        if not feeds:
            return jsonify({"error": "No data from ThingSpeak"}), 404

        feed = feeds[0]
        
        # Parse sensor values (Handle None/Null)
        temp  = float(feed["field1"]) if feed["field1"] is not None else 0.0
        hum   = float(feed["field2"]) if feed["field2"] is not None else 0.0
        soil  = float(feed["field3"]) if feed["field3"] is not None else 0.0
        light = float(feed["field4"]) if feed["field4"] is not None else 0.0

        # 2. Predict NPK
        df = pd.DataFrame([{
            "SoilMoisture": soil,
            "Temperature": temp,
            "Humidity": hum,
            "Light": light
        }])
        
        npk_pred = model.predict(df)[0]
        nitrogen, phosphorus, potassium = npk_pred[0], npk_pred[1], npk_pred[2]

        # 3. Determine Status
        status, detail = get_plant_status(soil, temp, hum, light, nitrogen, phosphorus, potassium)

        # 4. Return JSON response
        response = {
            "timestamp": feed.get("created_at"),
            "sensors": {
                "soil_moisture": soil,
                "temperature": temp,
                "humidity": hum,
                "light": light
            },
            "predicted_nutrients": {
                "nitrogen": round(nitrogen, 2),
                "phosphorus": round(phosphorus, 2),
                "potassium": round(potassium, 2)
            },
            "analysis": {
                "status": status,
                "detail": detail
            }
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
