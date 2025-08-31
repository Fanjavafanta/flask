from flask import Flask, render_template
import requests
import datetime
import MetaTrader5 as mt5


app = Flask(__name__)

def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": 2,          # Pour être sûr d’avoir 10 bougies 4h
        "interval": "hourly"
    }
    response = requests.get(url, params=params)
    data = response.json()

    prices = data.get("prices", [])  # [[timestamp, price], ...]
    
    # Regrouper par 4h pour faire bougies simples
    candles = []
    for i in range(0, len(prices), 4):
        slice_prices = prices[i:i+4]
        if len(slice_prices) < 4:
            continue
        open_price = slice_prices[0][1]
        close_price = slice_prices[-1][1]
        high_price = max(p[1] for p in slice_prices)
        low_price = min(p[1] for p in slice_prices)
        volume = 0  # CoinGecko API "market_chart" fournit volume séparément si besoin

        # timestamp pour la bougie (ouverture)
        ts = slice_prices[0][0]
        time_str = datetime.datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M")

        candles.append({
            "time": time_str,
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": volume
        })

    # On ne garde que les 10 dernières bougies
    return candles[-10:]

@app.route("/")
def home():
    btc_data = get_btc_data()
    if mt5.initialize(login="27782555", server="Deriv-Demo",password="Xurit##mag2"):
        btc_title = "MT5 initialized Successfully"
    else: btc_title = mt5.last_error()
    return render_template("btc.html", data=btc_data, title=btc_title)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
