import requests
import json

# ThingSpeak credentials
READ_API_KEY = "E6MTY3AFE7C0LQI6"
CHANNEL_ID = "3173091"

print("🔍 Fetching RAW data from ThingSpeak...\n")

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"
params = {
    "api_key": READ_API_KEY,
    "results": 5  # Get last 5 entries
}

try:
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    
    print("📋 Channel Info:")
    print(f"   Name: {data.get('channel', {}).get('name', 'N/A')}")
    print(f"   Description: {data.get('channel', {}).get('description', 'N/A')}")
    print(f"   Field 1: {data.get('channel', {}).get('field1', 'N/A')}")
    print(f"   Field 2: {data.get('channel', {}).get('field2', 'N/A')}")
    print(f"   Field 3: {data.get('channel', {}).get('field3', 'N/A')}")
    print(f"   Field 4: {data.get('channel', {}).get('field4', 'N/A')}")
    
    feeds = data.get("feeds", [])
    
    if not feeds:
        print("\n❌ No data entries found.")
    else:
        print(f"\n📊 Last {len(feeds)} Entries (RAW VALUES):\n")
        for i, feed in enumerate(feeds, 1):
            print(f"Entry {i}:")
            print(f"   Timestamp: {feed.get('created_at', 'N/A')}")
            print(f"   Field 1 (RAW): {feed.get('field1', 'NULL')}")
            print(f"   Field 2 (RAW): {feed.get('field2', 'NULL')}")
            print(f"   Field 3 (RAW): {feed.get('field3', 'NULL')}")
            print(f"   Field 4 (RAW): {feed.get('field4', 'NULL')}")
            print()
    
    print("\n💡 Full JSON Response (for debugging):")
    print(json.dumps(data, indent=2))
    
except Exception as e:
    print(f"❌ Error: {e}")
