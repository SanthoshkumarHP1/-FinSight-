import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from alpha_data_feed import get_price  # Make sure to import your get_price function from alpha_data_feed.py

# Define the RSI calculation function
def calculate_rsi(data, window=14):
    delta = data['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Define a list of stock symbols (including US and Indian stocks like NIFTY, BSE)
stock_symbols = [
    'MSFT', 'AAPL', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'NVDA', 'AMD', 'NFLX', 'INTC',
    'BA', 'GE', 'DIS', 'V', 'MA', 'SPY', 'QQQ', 'BRK.A', 'BRK.B', 'WMT', 'KO', 'TSM',
    'UBER', 'LYFT', 'SNAP',
    # Add Nifty and other Indian stocks
    'NIFTY', 'BANKNIFTY', 'RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 'LT',
    'SBIN', 'AXISBANK', 'HDFC', 'KOTAKBANK', 'BHARTIARTL', 'MARUTI', 'TATAMOTORS', 'M&M',
    'ITC', 'NTPC', 'ONGC', 'WIPRO', 'TCS', 'TECHM', 'HCLTECH', 'UPL', 'BAJFINANCE', 'BAJAJFINSV',
    'ADANIGREEN', 'ADANIPORTS', 'DIVISLAB', 'HINDUNILVR', 'MOTHERSONSUMI', 'TATACONSUM', 'VEDANTA',
    'BSE', 'BOMDIA', 'RELIANCE.NS', 'HDFCBANK.NS', 'SBIN.NS', 'NSEBANK', 'NSEAUTO', 'NSEFMCG',
    'NSEINFRA', 'NSEPHARMA', 'NSEIT',  # NSE sector indices
]

# Streamlit app UI
st.title("🚀 Real-time Stock Trading Dashboard")

# Dropdown menu for selecting stock symbol
symbol = st.selectbox("Select Stock Symbol", stock_symbols)

# Fetch stock data using the get_price function (assuming you have this function in alpha_data_feed.py)
df = get_price(symbol)

# Check if data was received and show it
if df is not None and not df.empty:
    st.write(f"### Stock Data for {symbol}")
    st.write(df.tail())  # Display the last few rows of data for the selected symbol

    # Add trading analysis here (e.g., calculating RSI, moving averages)
    st.write(f"### Additional Trading Analysis for {symbol}")
    
    # Calculate RSI for the stock data
    df['RSI'] = calculate_rsi(df)  # Calculate RSI

    # Show the latest price and RSI values
    st.write(df[['price', 'RSI']].tail())  # Show the latest price and RSI

    # Example buy/sell signals based on RSI
    latest = df.iloc[-1]
    if latest['RSI'] < 30:
        st.write(f"🟢 BUY SIGNAL for {symbol}")
    elif latest['RSI'] > 70:
        st.write(f"🔴 SELL SIGNAL for {symbol}")
    else:
        st.write(f"⚪ HOLD SIGNAL for {symbol}")

    # ---- Plot Price and RSI Trend Lines ----

    # Plot Price Trend
    fig = plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['price'], label="Price", color='blue')
    plt.title(f"Price Trend for {symbol}")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig)

    # Plot RSI Trend
    fig = plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['RSI'], label="RSI", color='orange')
    plt.axhline(30, color='red', linestyle='--', label="Buy Signal (RSI < 30)")
    plt.axhline(70, color='green', linestyle='--', label="Sell Signal (RSI > 70)")
    plt.title(f"RSI Trend for {symbol}")
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig)

    # ---- Plot Candlestick Chart with Plotly ----
    # Prepare candlestick data
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['open'], high=df['high'],
                                         low=df['low'], close=df['price'],
                                         name="Candlestick")])

    fig.update_layout(
        title=f'Candlestick Chart for {symbol}',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )
    st.plotly_chart(fig)

else:
    st.write("No data available for the selected stock symbol.")
