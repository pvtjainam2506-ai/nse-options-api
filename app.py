from flask import Flask, jsonify
import requests

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com"
}

session = requests.Session()
session.get("https://www.nseindia.com", headers=headers)

@app.route("/stocks")
def stocks():
    url = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"
    data = session.get(url, headers=headers).json()
    symbols = [s["symbol"] for s in data["data"]]
    return jsonify(symbols)

if __name__ == "__main__":
    app.run()

