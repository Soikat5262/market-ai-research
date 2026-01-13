import requests
import json
import os

API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"
FILE_NAME = "data.json"

def fetch_data():
    try:
        response = requests.get(API_URL)
        data = response.json()
        if data['code'] == 0:
            new_list = data['data']['list']
            
            if os.path.exists(FILE_NAME):
                with open(FILE_NAME, 'r') as f:
                    old_data = json.load(f)
            else:
                old_data = []

            existing_ids = {item['issueNumber'] for item in old_data}
            added = 0
            for item in new_list:
                if item['issueNumber'] not in existing_ids:
                    old_data.append({
                        "id": item['issueNumber'],
                        "num": item['number'],
                        "time": item['addTime']
                    })
                    added += 1
            
            old_data = old_data[-20000:]
            with open(FILE_NAME, 'w') as f:
                json.dump(old_data, f, indent=2)
            print(f"Added {added} records.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_data()
      
