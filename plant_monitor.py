import os
import time
from datetime import datetime

import pandas as pd
import requests
import joblib

from collections import deque

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# =============== USER SETTINGS ===============

READ_API_KEY = "YOUR_THINGSPEAK_READ_API_KEY"   # 🔁 CHANGE
CHANNEL_ID   = "YOUR_CHANNEL_ID"                # 🔁 CHANGE

CONTACT_NAME = "My Number"                      # 🔁 CHANGE (WhatsApp contact name)
MODEL_PATH   = "plant_health_rf.pkl"            # must be in same folder
CSV_FILE     = "plant_logs.csv"

POLL_INTERVAL_SEC = 20  # seconds between ThingSpeak reads (>= ESP32 delay)

# =============== LOAD ML MODEL ===============

model = joblib.load(MODEL_PATH)

# Keep last N readings for running averages
N_AVG = 10
soil_history  = deque(maxlen=N_AVG)
temp_history  = deque(maxlen=N_AVG)
hum_history   = deque(maxlen=N_AVG)
light_history = deque(maxlen=N_AVG)

# =============== WHATSAPP WEB SETUP ===============

print("🚀 Launching Chrome for WhatsApp Web...")
driver = webdriver.Chrome()   # Make sure ChromeDriver is installed and in PATH
driver.get("https://web.whatsapp.com")
print("📱 Scan the QR code with your phone to log in to WhatsApp Web...")
sleep(20)  # Give time to scan

def send_whatsapp(message: str):
    """Send a WhatsApp message to CONTACT_NAME using WhatsApp Web via Selenium."""
    try:
        # Click on search box
        search_xpath = "//div[@title='Search input textbox' or @title='Search or start a new chat']"
        search_box = driver.find_element(By.XPATH, search_xpath)
        search_box.click()
        search_box.clear()
        search_box.send_keys(CONTACT_NAME)
        sleep(2)
        search_box.send_keys(Keys.ENTER)
        sleep(2)

        # Find the message input box
        msg_box_xpath = "//div[@title='Type a message' or @contenteditable='true'][@data-tab='10' or @data-tab='9']"
        message_box = driver.find_element(By.XPATH, msg_box_xpath)
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

        print("📩 WhatsApp alert sent!")
    except Exception as e:
        print("⚠ Error sending WhatsApp message:", e)

# =============== THINGSPEAK READ ===============

def read_latest_from_thingspeak():
    """Fetch latest sensor reading from ThingSpeak channel."""
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"
    params = {
        "api_key": READ_API_KEY,
        "results": 1
    }
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    feeds = data.get("feeds", [])
    if not feeds:
        raise ValueError("No data in ThingSpeak channel yet.")

    feed = feeds[0]

    soil  = float(feed["field1"]) if feed["field1"] is not None else 0.0
    temp  = float(feed["field2"]) if feed["field2"] is not None else 0.0
    hum   = float(feed["field3"]) if feed["field3"] is not None else 0.0
    light = float(feed["field4"]) if feed["field4"] is not None else 0.0

    return soil, temp, hum, light

# =============== ML PREDICTION ===============

def analyze_condition(soil, temp, hum, light):
    df = pd.DataFrame([{
        "SoilMoisture": soil,
        "Temperature": temp,
        "Humidity": hum,
        "Light": light
    }])

    pred = model.predict(df)[0]

    if pred == "HEALTHY":
        status = "🌱 PLANT IS HEALTHY"
        detail = "All environmental conditions are within optimal range."
    elif pred == "DRY_SOIL":
        status = "⚠ SOIL TOO DRY — WATER REQUIRED"
        detail = "Soil moisture is too low. Please water the plant."
    elif pred == "OVERWATERED":
        status = "⚠ SOIL TOO WET — REDUCE WATERING"
        detail = "Soil is holding too much water. Reduce watering and improve drainage."
    elif pred == "LOW_LIGHT":
        status = "⚠ INSUFFICIENT LIGHT — MOVE PLANT NEAR WINDOW"
        detail = "Light intensity is too low. Move the plant to a brighter area."
    else:
        status = f"UNKNOWN CONDITION ({pred})"
        detail = "Model returned an unexpected label. Check training classes."

    return pred, status, detail

# =============== LOGGING ===============

def log_to_csv(timestamp, soil, temp, hum, light, status):
    row = {
        "Timestamp":    timestamp,
        "SoilMoisture": soil,
        "Temperature":  temp,
        "Humidity":     hum,
        "Light":        light,
        "Status":       status
    }
    df = pd.DataFrame([row])

    file_exists = os.path.exists(CSV_FILE)
    df.to_csv(CSV_FILE, mode="a", header=not file_exists, index=False)

# =============== DISPLAY ===============

def print_reading(timestamp, soil, temp, hum, light, status, detail):
    print("\n=====================================")
    print(f"🕒 {timestamp}")
    print(f"{status}")
    print(f"ℹ  {detail}")
    print(f"💧 Soil Moisture : {soil:.2f} %")
    print(f"🌡 Temperature   : {temp:.2f} °C")
    print(f"💦 Humidity      : {hum:.2f} %")
    print(f"💡 Light         : {light:.2f} lux")

    if len(soil_history) > 1:
        avg_soil  = sum(soil_history) / len(soil_history)
        avg_temp  = sum(temp_history) / len(temp_history)
        avg_hum   = sum(hum_history) / len(hum_history)
        avg_light = sum(light_history) / len(light_history)

        print("\n📊 Running Averages (last {} readings):".format(len(soil_history)))
        print(f"   Avg Soil Moisture : {avg_soil:.2f} %")
        print(f"   Avg Temperature   : {avg_temp:.2f} °C")
        print(f"   Avg Humidity      : {avg_hum:.2f} %")
        print(f"   Avg Light         : {avg_light:.2f} lux")
    print("=====================================")

# =============== ALERT LOGIC ===============

def maybe_send_alert(status, detail, timestamp, soil, temp, hum, light):
    if status.startswith("🌱 PLANT IS HEALTHY"):
        return  # no alert

    msg = (
        f"🪴 Plant Health Alert!\n"
        f"{status}\n"
        f"{detail}\n\n"
        f"🕒 Time: {timestamp}\n"
        f"💧 Soil Moisture: {soil:.2f}%\n"
        f"🌡 Temperature : {temp:.2f}°C\n"
        f"💦 Humidity    : {hum:.2f}%\n"
        f"💡 Light       : {light:.2f} lux"
    )
    send_whatsapp(msg)

# =============== MAIN LOOP ===============

print("🌿 Starting Plant Health Monitoring via ThingSpeak + WhatsApp...\n")

while True:
    try:
        soil, temp, hum, light = read_latest_from_thingspeak()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # update histories
        soil_history.append(soil)
        temp_history.append(temp)
        hum_history.append(hum)
        light_history.append(light)

        pred, status, detail = analyze_condition(soil, temp, hum, light)
        print_reading(timestamp, soil, temp, hum, light, status, detail)
        log_to_csv(timestamp, soil, temp, hum, light, status)
        maybe_send_alert(status, detail, timestamp, soil, temp, hum, light)

    except Exception as e:
        print("⚠ Error in loop:", e)

    time.sleep(POLL_INTERVAL_SEC)
