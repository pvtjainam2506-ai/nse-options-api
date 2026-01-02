from flask import Flask, jsonify
import requests
from time import sleep

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com",
}

BASE_URL = "https://www.nseindia.com"
STOCKS_API = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"

session = requests.Session()

def get_nse_data(url):
    """
    Properly fetch NSE data with cookies and retries.
    """
    # Step 1: Get NSE homepage to initialize cookies
    for attempt in range(3):
        try:
            session.get(BASE_URL, headers=HEADERS, timeout=5)
            response = session.get(url, headers=HEADERS, timeout=5)
            
            # Check if we got JSON
            if response.headers.get("Content-Type", "").startswith("application/json"):
                return response.json()
            else:
                sleep(1)  # NSE sometimes returns HTML, wait & retry
        except Exception as e:
            print(f"NSE fetch error: {e}, retrying...")
            sleep(1)
    return None

@app.route("/")
def home():
    return "API WORKING"

@app.route("/stocks")
def stocks():
    data = get_nse_data(STOCKS_API)
    if not data or "data" not in data:
        return jsonify({"error": "Failed to fetch NSE data"}), 500
    
    symbols = [item["symbol"] for item in data["data"]]
    return jsonify(symbols)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
