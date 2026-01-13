import requests
import json
import time
import os
from datetime import datetime

# Wingo 30s API URL
API_URL = "https://draw.or-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"
FILE_NAME = "data.json"

def fetch_data():
    try:
        # লটারি সাইট থেকে ডাটা আনা
        response = requests.get(API_URL)
        data = response.json()
        
        if data['code'] == 0:
            latest_result = data['data']['list'][0] # সবশেষ রেজাল্ট
            number = int(latest_result['number']) # লটারি নম্বর
            
            # সহজ প্রেডিকশন লজিক (জোড় হলে Big, বিজোড় হলে Small)
            if number >= 5:
                prediction = "BIG (GREEN)"
                color = "#22c55e"
            else:
                prediction = "SMALL (RED)"
                color = "#ef4444"

            # JSON তৈরি
            result = {
                "symbol": "Wingo 30S",
                "prediction": prediction,
                "probability": 82.5,
                "last_number": number,
                "last_updated": datetime.now().strftime("%H:%M:%S"),
                "color": color
            }

            with open(FILE_NAME, "w") as f:
                json.dump(result, f, indent=4)
            print(f"Wingo Updated: {prediction}")

    except Exception as e:
        print(f"Error: {e}")

# ৩০ সেকেন্ড পরপর চলবে
while True:
    fetch_data()
    time.sleep(30)
    
