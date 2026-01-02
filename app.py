from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

BASE_URL = "https://www.nseindia.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/market-data/equity-derivatives"
}

session = requests.Session()

def init_session():
    session.get(BASE_URL, headers=headers)
    time.sleep(1)

@app.route("/")
def home():
    return "API WORKING"

@app.route("/stocks")
def stocks():
    init_session()
    url = BASE_URL + "/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"
    r = session.get(url, headers=headers, timeout=10)
    data = r.json()
    symbols = [i["symbol"] for i in data["data"]]
    return jsonify(symbols)

if __name__ == "__main__":
    app.run()
    
