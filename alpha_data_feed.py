# alpha_data_feed.py
import requests
import pandas as pd

API_KEY = '2Z7PD6IC0OQH9OX7'  # Replace with your key
BASE_URL = 'https://www.alphavantage.co/query'

def get_price(symbol):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": API_KEY,
        "outputsize": "compact"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    key = [k for k in data.keys() if "Time Series" in k]
    if not key or key[0] not in data:
        print("No time series found in API response:", data)
        return None

    df = pd.DataFrame.from_dict(data[key[0]], orient='index')
    df = df.rename(columns={"1. open": "open", "2. high": "high", "3. low": "low", "4. close": "price", "5. volume": "volume"})
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.astype(float)
    return df
