import requests
import pandas as pd
import joblib

# ThingSpeak credentials
READ_API_KEY = "E6MTY3AFE7C0LQI6"
CHANNEL_ID = "3173091"

print("🔌 Testing ThingSpeak API Connection...")
print(f"📡 Channel ID: {CHANNEL_ID}")

# Fetch data from ThingSpeak
url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"
params = {
    "api_key": READ_API_KEY,
    "results": 1
}

try:
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    
    print(f"\n✅ API Response Status: {r.status_code}")
    
    feeds = data.get("feeds", [])
    if not feeds:
        print("❌ No data found in ThingSpeak channel yet.")
        exit()
    
    feed = feeds[0]
    
    temp  = float(feed["field1"]) if feed["field1"] is not None else 0.0  # Field1 = Temperature
    hum   = float(feed["field2"]) if feed["field2"] is not None else 0.0  # Field2 = Humidity
    soil  = float(feed["field3"]) if feed["field3"] is not None else 0.0  # Field3 = Soil Moisture
    light = float(feed["field4"]) if feed["field4"] is not None else 0.0  # Field4 = Light
    
    print(f"\n📥 Latest Sensor Readings from ThingSpeak:")
    print(f"   💧 Soil Moisture: {soil:.2f}%")
    print(f"   🌡 Temperature:   {temp:.2f}°C")
    print(f"   💦 Humidity:      {hum:.2f}%")
    print(f"   💡 Light:         {light:.2f} lux")
    
    # Load model and predict NPK
    print(f"\n🤖 Loading ML Model...")
    model = joblib.load("plant_health_rf.pkl")
    
    df = pd.DataFrame([{
        "SoilMoisture": soil,
        "Temperature": temp,
        "Humidity": hum,
        "Light": light
    }])
    
    npk_pred = model.predict(df)[0]
    nitrogen, phosphorus, potassium = npk_pred[0], npk_pred[1], npk_pred[2]
    
    print(f"\n🔮 Predicted NPK Values:")
    print(f"   🧪 Nitrogen:   {nitrogen:.2f} mg/kg")
    print(f"   🧪 Phosphorus: {phosphorus:.2f} mg/kg")
    print(f"   🧪 Potassium:  {potassium:.2f} mg/kg")
    
    # Determine Status
    status = "🌱 PLANT IS HEALTHY"
    
    if soil < 20:
        status = "⚠ SOIL TOO DRY"
    elif soil > 80:
        status = "⚠ SOIL TOO WET"
    elif light < 200:
        status = "⚠ INSUFFICIENT LIGHT"
    elif nitrogen < 20:
        status = "⚠ LOW NITROGEN"
    elif phosphorus < 20:
        status = "⚠ LOW PHOSPHORUS"
    elif potassium < 20:
        status = "⚠ LOW POTASSIUM"
    
    print(f"\n📋 Plant Status: {status}")
    print("\n✅ All systems working! Ready to run plant_monitor.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Please check your API key and Channel ID.")
