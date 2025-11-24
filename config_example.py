"""
Configuration Template
Copy this to config.py and fill in your actual values
"""

# ThingSpeak Settings
READ_API_KEY = "YOUR_THINGSPEAK_READ_API_KEY"
CHANNEL_ID = "YOUR_CHANNEL_ID"

# WhatsApp Settings
CONTACT_NAME = "My Number"  # Exact contact name in WhatsApp

# File Paths
MODEL_PATH = "plant_health_rf.pkl"
CSV_FILE = "plant_logs.csv"

# Monitoring Settings
POLL_INTERVAL_SEC = 20  # Seconds between ThingSpeak reads
N_AVG = 10  # Number of readings for running average

# Alert Settings
ENABLE_WHATSAPP_ALERTS = True
ALERT_COOLDOWN_MIN = 30  # Minutes between repeated alerts for same condition
