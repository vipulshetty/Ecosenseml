from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
READ_API_KEY = "E6MTY3AFE7C0LQI6"
CHANNEL_ID = "3173091"

@app.route('/')
def home():
    return "<h1>🌿 Ecosense API is Running!</h1><p>Go to <a href='/api/plant-status'>/api/plant-status</a> to see the data.</p>"

# Lightweight NPK Estimation (Since we can't load heavy ML libs on Vercel free tier)
def estimate_npk(soil, temp, hum, light):
    """
    Estimate NPK values based on environmental factors using simple heuristics
    instead of a heavy Random Forest model.
    """
    # Base values (Ideal conditions)
    n, p, k = 40, 50, 60
    
    # Adjust based on Soil Moisture
    if soil < 30:
        n -= 10; p -= 10; k -= 10  # Dry soil reduces nutrient availability
    elif soil > 80:
        n -= 5; p -= 5; k -= 5     # Leaching risk
        
    # Adjust based on Temperature
    if temp > 30:
        n -= 5  # High temp might increase volatilization
        
    return max(0, n), max(0, p), max(0, k)

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

        # 2. Estimate NPK (Lightweight)
        nitrogen, phosphorus, potassium = estimate_npk(soil, temp, hum, light)

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
