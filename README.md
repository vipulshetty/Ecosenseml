---
title: Ecosense Plant Monitor
emoji: 🌿
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
---

# Ecosense Plant Monitor API 🌿

This is a Flask API that:
1. Fetches live plant sensor data from **ThingSpeak**.
2. Uses a **Random Forest ML Model** to predict NPK levels.
3. Returns the plant health status and nutrient analysis.

## API Usage

**Endpoint:** `/api/plant-status`

**Example Response:**
```json
{
  "analysis": {
    "status": "HEALTHY",
    "detail": "All conditions are optimal."
  },
  "predicted_nutrients": {
    "nitrogen": 40.5,
    "phosphorus": 50.2,
    "potassium": 60.1
  },
  "sensors": {
    "humidity": 60.5,
    "light": 1000.0,
    "soil_moisture": 50.0,
    "temperature": 25.0
  },
  "timestamp": "2025-11-20T08:14:49Z"
}
```
