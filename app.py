from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_btc_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "4h",
        "limit": 10
    }
    response = requests.get(url, params=params)
    data = response.json()

    # On garde: [Heure d'ouverture, Open, High, Low, Close, Volume]
    candles = []
    for c in data:
        candles.append({
            "time": c[0],
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5])
        })
    return candles

@app.route("/")
def home():
    btc_data = get_btc_data()
    return render_template("btc.html", data=btc_data, title="BTC/USD - Dernières 10 bougies (4h)")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
