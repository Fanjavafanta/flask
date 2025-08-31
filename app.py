from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_btc_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",   # BTC/USD sur Binance (pair USDT)
        "interval": "4h",
        "limit": 10
    }
    response = requests.get(url, params=params)

    try:
        data = response.json()
    except Exception as e:
        return [{"error": f"Impossible de parser la réponse: {e}"}]

    # Vérifier si on a une liste (bougies) ou un dict (erreur Binance)
    if isinstance(data, dict) and "msg" in data:
        return [{"error": f"Erreur Binance: {data['msg']}"}]

    candles = []
    for c in data:
        candles.append({
            "open": round(float(c[1]), 2),
            "high": round(float(c[2]), 2),
            "low": round(float(c[3]), 2),
            "close": round(float(c[4]), 2),
            "volume": round(float(c[5]), 2)
        })
    return candles

@app.route("/")
def home():
    btc_data = get_btc_data()
    return render_template("btc.html", data=btc_data, title="BTC/USD - Dernières 10 bougies (4h)")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
