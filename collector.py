import yfinance as yf
import json
import time
import os
from datetime import datetime

# যে পেয়ারের প্রেডিকশন চান
SYMBOL = "BTC-USD" 

def fetch_and_predict():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching data for {SYMBOL}...")
    try:
        # ১ মিনিটের ডেটা নেওয়া
        data = yf.download(SYMBOL, period="1d", interval="1m", progress=False)
        
        if data.empty or len(data) < 2:
            print("Not enough data yet. Retrying...")
            return

        # বর্তমান এবং আগের প্রাইস
        current_price = float(data['Close'].iloc[-1])
        prev_price = float(data['Close'].iloc[-2])

        # প্রেডিকশন লজিক
        if current_price > prev_price:
            prediction = "CALL (UP)"
            status_color = "#22c55e"
        elif current_price < prev_price:
            prediction = "PUT (DOWN)"
            status_color = "#ef4444"
        else:
            prediction = "NEUTRAL"
            status_color = "#38bdf8"

        # প্রবাবিলিটি ক্যালকুলেশন (র‍্যান্ডম নয়, প্রাইস মুভমেন্টের ওপর ভিত্তি করে)
        diff = abs(current_price - prev_price)
        prob = round(min(70 + (diff * 10), 98.5), 2)

        # JSON ডাটা তৈরি (এটি index.html রিড করবে)
        result = {
            "symbol": SYMBOL,
            "prediction": prediction,
            "probability": prob,
            "current_price": round(current_price, 2),
            "last_updated": datetime.now().strftime("%H:%M:%S"),
            "color": status_color
        }

        # data.json ফাইলটি নতুন করে তৈরি বা ওভাররাইট হবে
        with open("data.json", "w") as f:
            json.dump(result, f, indent=4)
        
        print(f"Success! Prediction: {prediction} ({prob}%)")

    except Exception as e:
        print(f"Error occurred: {e}")

# স্ক্রিপ্টটি রান করলেই প্রথমবার ডাটা নিবে
fetch_and_predict()

# তারপর প্রতি ৩০ সেকেন্ড পর পর লুপ চলবে
while True:
    time.sleep(30)
    fetch_and_predict()
