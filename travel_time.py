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

# Route Information
ROUTES = [
    {
        "origin": "Unit no. 304, Sentinel Hiranandani Business Park, Powai, Mumbai, Maharashtra 400076",
        "destination": "New Mahada Colony, SV Patel Nagar, Andheri West, Mumbai, Maharashtra 400061",
        "csv_file": "powai_to_andheri_log.csv"
    },
    {
        "origin": "New Mahada Colony, SV Patel Nagar, Andheri West, Mumbai, Maharashtra 400061",
        "destination": "Unit no. 304, Sentinel Hiranandani Business Park, Powai, Mumbai, Maharashtra 400076",
        "csv_file": "andheri_to_powai_log.csv"
    }
]

# Function to fetch travel time
def get_travel_time(origin, destination):
    params = {
        "origin": origin,
        "destination": destination,
        "departure_time": "now",
        "traffic_model": "best_guess",
        "key": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "routes" in data and data["routes"]:
        return data["routes"][0]["legs"][0]["duration_in_traffic"]["text"]
    else:
        print("Error fetching data:", data)
        return "API_ERROR"

# Function to log travel times
def log_travel_times():
    timestamp = datetime.datetime.now(pytz.utc).astimezone(ist).strftime('%Y-%m-%d %H:%M:%S')

    for route in ROUTES:
        duration = get_travel_time(route["origin"], route["destination"])

        # Ensure CSV exists with header
        try:
            with open(route["csv_file"], "r") as file:
                pass
        except FileNotFoundError:
            with open(route["csv_file"], "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp (IST)", "Travel Duration"])

        # Append the travel time
        with open(route["csv_file"], "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, duration])
            print(f"Logged: {timestamp} - {route['origin']} to {route['destination']}: {duration}")

if __name__ == "__main__":
    log_travel_times()

