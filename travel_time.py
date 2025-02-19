import requests
import csv
import datetime
import pytz

API_KEY = "AIzaSyDeU40JTOwi2EtX38E8ZNLrSx_HYNfE1os"
ORIGIN = "Unit no. 304, Sentinel Hiranandani Business Park, Powai, Mumbai, Maharashtra 400076"
DESTINATION = "New Mahada Colony, SV Patel Nagar, Andheri West, Mumbai, Maharashtra 400061"

URL = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={ORIGIN}&destinations={DESTINATION}&key={API_KEY}"

def fetch_travel_time():
    response = requests.get(URL)
    data = response.json()

    if data["status"] == "OK":
        duration = data["rows"][0]["elements"][0]["duration"]["text"]
        now = datetime.datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")

        return now, duration
    else:
        return None, None

def write_to_csv():
    now, duration = fetch_travel_time()
    if now and duration:
        file_path = "travel_time_log.csv"
        header = ["Timestamp (IST)", "Duration"]

        try:
            with open(file_path, "r") as file:
                pass  # Check if file exists
        except FileNotFoundError:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)

        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now, duration])

if __name__ == "__main__":
    write_to_csv()
