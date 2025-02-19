import requests
import csv
import os
import datetime
import pytz

# API Key (Make sure it's directly in the script or stored securely in GitHub secrets)
API_KEY = "AIzaSyDeU40JTOwi2EtX38E8ZNLrSx_HYNfE1os"

# Origin & Destination
ORIGIN = "Unit no. 304, Sentinel Hiranandani Business Park, Powai, Mumbai, Maharashtra 400076"
DESTINATION = "New Mahada Colony, SV Patel Nagar, Andheri West, Mumbai, Maharashtra 400061"

# Timezone for IST
IST = pytz.timezone('Asia/Kolkata')

# Get current IST time
now = datetime.datetime.now(IST)
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

# API Request URL
url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={ORIGIN}&destinations={DESTINATION}&key={API_KEY}"

# Fetch data from Google Maps API
response = requests.get(url)
data = response.json()

# Extract travel time (in minutes)
try:
    duration_seconds = data["rows"][0]["elements"][0]["duration"]["value"]
    duration_minutes = duration_seconds // 60
except (KeyError, IndexError):
    duration_minutes = "API_ERROR"  # If API fails, log error

# CSV file path
csv_file = "travel_time_log.csv"

# Ensure file exists with headers
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "duration_minutes"])

# Append new data
with open(csv_file, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([timestamp, duration_minutes])

# Debugging output
print(f"Logged at {timestamp}: {duration_minutes} minutes")
print("Current directory:", os.getcwd())

