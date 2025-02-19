import requests
import datetime
import pytz
import csv
import time

# Google Maps API Key (Ensure it's securely stored in GitHub Secrets for production use)
API_KEY = "AIzaSyDeU40JTOwi2EtX38E8ZNLrSx_HYNfE1os"

# Origin & Destination
ORIGIN = "Unit no. 304, Sentinel Hiranandani Business Park, Powai, Mumbai, Maharashtra 400076"
DESTINATION = "New Mahada Colony, SV Patel Nagar, Andheri West, Mumbai, Maharashtra 400061"

# API URL
BASE_URL = "https://maps.googleapis.com/maps/api/directions/json"

# Set IST timezone
ist = pytz.timezone("Asia/Kolkata")

# CSV File Name
CSV_FILE = "travel_time_log.csv"

# Function to fetch travel time
def get_travel_time():
    params = {
        "origin": ORIGIN,
        "destination": DESTINATION,
        "departure_time": "now",
        "traffic_model": "best_guess",
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "routes" in data and data["routes"]:
        duration = data["routes"][0]["legs"][0]["duration_in_traffic"]["text"]
        current_time_ist = datetime.datetime.now(pytz.utc).astimezone(ist).strftime('%Y-%m-%d %H:%M:%S')

        # Print the result
        print(f"IST Time: {current_time_ist}, Travel Duration: {duration}")

        # Append data to CSV
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([current_time_ist, duration])
    else:
        print("Error fetching data:", data)

# Run function once
get_travel_time()


