import requests
import csv
import time
from datetime import datetime
import pytz

# API Key
API_KEY = "AIzaSyDeU40JTOwi2EtX38E8ZNLrSx_HYNfE1os"

# Origin & Destination
ORIGIN = "Unit no. 304, Sentinel Hiranandani Business Park, Powai, Mumbai, Maharashtra 400076"
DESTINATION = "New Mahada Colony, SV Patel Nagar, Andheri West, Mumbai, Maharashtra 400061"

# Timezone
IST = pytz.timezone('Asia/Kolkata')

# Function to fetch travel time
def get_travel_time():
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={ORIGIN}&destinations={DESTINATION}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "rows" in data and data["rows"][0]["elements"][0]["status"] == "OK":
        duration = data["rows"][0]["elements"][0]["duration"]["text"]
        current_time = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')
        return current_time, duration
    else:
        return datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'), "API Error"

# Run the script every minute
while True:
    timestamp, travel_time = get_travel_time()

    # Save to CSV
    with open("travel_time_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, travel_time])
    
    print(f"{timestamp} - Travel Time: {travel_time}")

    # Wait for 1 minute before running again
    time.sleep(60)
