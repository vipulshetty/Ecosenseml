# 🌿 EcoSense - Plant Health Monitoring System

Real-time plant health monitoring system that reads sensor data from ThingSpeak, performs ML predictions, and sends WhatsApp alerts when intervention is needed.

## 🚀 Features

- **Real-time Monitoring**: Polls ThingSpeak every 20 seconds for latest sensor data
- **ML Predictions**: Uses Random Forest model to classify plant health conditions
- **WhatsApp Alerts**: Automatically sends alerts via WhatsApp Web when issues detected
- **Data Logging**: Stores all readings in CSV file for historical analysis
- **Running Averages**: Tracks last 10 readings to smooth out sensor noise

## 📋 Prerequisites

1. **Python 3.8+**
2. **Chrome Browser** and **ChromeDriver** (for WhatsApp Web automation)
3. **ThingSpeak Account** with configured channel
4. **Trained ML Model** (`plant_health_rf.pkl`)

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install ChromeDriver

Download ChromeDriver matching your Chrome version from:
https://chromedriver.chromium.org/downloads

Add ChromeDriver to your system PATH.

### 3. Configure Settings

Edit `plant_monitor.py` and update these variables:

```python
READ_API_KEY = "YOUR_THINGSPEAK_READ_API_KEY"   # Your ThingSpeak Read API key
CHANNEL_ID   = "YOUR_CHANNEL_ID"                # Your ThingSpeak Channel ID
CONTACT_NAME = "My Number"                      # WhatsApp contact name (exact match)
```

### 4. ThingSpeak Channel Setup

Your ThingSpeak channel should have these fields:
- **Field 1**: Soil Moisture (%)
- **Field 2**: Temperature (°C)
- **Field 3**: Humidity (%)
- **Field 4**: Light Intensity (lux)

### 5. ML Model

Place your trained `plant_health_rf.pkl` model in the same directory.

The model should predict one of:
- `HEALTHY`
- `DRY_SOIL`
- `OVERWATERED`
- `LOW_LIGHT`

## 🎯 Usage

### Run the Monitor

```bash
python plant_monitor.py
```

### First Time Setup

1. Chrome will open to WhatsApp Web
2. Scan the QR code with your phone (you have 20 seconds)
3. Monitoring will start automatically

### What Happens

- Reads sensor data from ThingSpeak every 20 seconds
- Analyzes data using ML model
- Displays current readings and running averages
- Logs all data to `plant_logs.csv`
- Sends WhatsApp alerts when issues detected

## 📊 Output Example

```
=====================================
🕒 2025-11-24 14:30:45
🌱 PLANT IS HEALTHY
ℹ  All environmental conditions are within optimal range.
💧 Soil Moisture : 45.30 %
🌡 Temperature   : 24.50 °C
💦 Humidity      : 65.20 %
💡 Light         : 850.00 lux

📊 Running Averages (last 10 readings):
   Avg Soil Moisture : 44.85 %
   Avg Temperature   : 24.32 °C
   Avg Humidity      : 64.98 %
   Avg Light         : 842.50 lux
=====================================
```

## 🔔 Alert Conditions

WhatsApp alerts are sent for:
- **DRY_SOIL**: Soil moisture too low - watering needed
- **OVERWATERED**: Soil too wet - reduce watering
- **LOW_LIGHT**: Insufficient light - move plant

No alerts sent when plant is HEALTHY.

## 📁 Files Generated

- `plant_logs.csv`: Historical data log with all readings and predictions

## ⚙️ Configuration Options

```python
POLL_INTERVAL_SEC = 20  # Seconds between readings (adjust as needed)
N_AVG = 10              # Number of readings for running average
MODEL_PATH = "plant_health_rf.pkl"  # Path to ML model
CSV_FILE = "plant_logs.csv"         # Log file name
```

## 🛠️ Troubleshooting

### ChromeDriver Issues
- Ensure ChromeDriver version matches your Chrome browser version
- Make sure ChromeDriver is in your system PATH

### WhatsApp Connection
- If QR code scan fails, increase the `sleep(20)` duration
- Ensure your phone has WhatsApp installed and internet connection
- Contact name must exactly match your WhatsApp contact

### ThingSpeak Connection
- Verify your API key and Channel ID are correct
- Check that your ESP32 is uploading data to ThingSpeak
- Ensure poll interval is >= ESP32 update interval

### Model Errors
- Verify `plant_health_rf.pkl` exists in the same folder
- Ensure model expects features: SoilMoisture, Temperature, Humidity, Light
- Check model was trained with correct class labels

## 📝 Notes

- Keep the Chrome window open while monitoring
- Don't close WhatsApp Web manually
- The script runs continuously until stopped (Ctrl+C)
- All sensor values are logged regardless of health status

## 🔒 Security

- Never commit your API keys to version control
- Use environment variables for sensitive data in production
- Keep your WhatsApp session secure

## 📄 License

MIT License - Free to use and modify for your projects.
