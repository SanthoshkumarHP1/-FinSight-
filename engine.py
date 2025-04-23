# engine.py
from alpha_data_feed import get_price
import pandas as pd
import time

def calculate_rsi(data, window=14):
    delta = data['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def trade_logic(symbol):
    df = get_price(symbol)
    if df is None or df.empty:
        print("No data received. Skipping...")
        return

    df['RSI'] = calculate_rsi(df)

    latest = df.iloc[-1]
    print(f"🔍 Latest Price: {latest['price']} | RSI: {latest['RSI']:.2f}")

    if latest['RSI'] < 30:
        print(f"🟢 BUY SIGNAL for {symbol}")
    elif latest['RSI'] > 70:
        print(f"🔴 SELL SIGNAL for {symbol}")
    else:
        print(f"⚪ HOLD SIGNAL for {symbol}")

if __name__ == "__main__":
    print("🚀 Starting Trading Engine...")
    trade_logic("MSFT")  # US stock symbols only
    trade_logic("AAPL")