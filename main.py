import yfinance as yf
from ta.momentum import RSIIndicator

def get_stock_data(ticker: str):
    """Fetches daily price data for a given stock."""
    return yf.download(ticker, period="6mo", interval="1d")


def add_rsi(data):
    close = data["Close"].astype(float).squeeze()

    data["RSI_14"] = RSIIndicator(close, window=14).rsi()
    data["RSI_50"] = RSIIndicator(close, window=50).rsi()

    return data

def generate_rsi_signal(rsi_fast, rsi_slow):
    # Setup identifiering
    if rsi_fast < 30 and rsi_slow > rsi_fast:
        return "SETUP: Oversold short-term but trend stronger. Watch for reversal."

    # Bekräftad vändning (RSI passerar 30 från undersidan)
    if rsi_fast > 30 and rsi_fast < rsi_slow:
        return "BUY: Reversal confirmation."

    # Överköpt situation
    if rsi_fast > 70 and rsi_fast < rsi_slow:
        return "SELL: Short-term exhaustion."

    return "WAIT"

def main():
    ticker = input("Enter stock ticker: ").upper()

    print(f"\nFetching data for {ticker}...\n")
    df = get_stock_data(ticker)

    if df.empty:
        print("No data found. Check symbol or internet.")
        return

    df = add_rsi(df)

    latest_rsi_14 = df["RSI_14"].iloc[-1]
    latest_rsi_50 = df["RSI_50"].iloc[-1]

    decision = generate_rsi_signal(latest_rsi_14, latest_rsi_50)

    print(f"RSI (14): {round(latest_rsi_14, 2)}")
    print(f"RSI (50): {round(latest_rsi_50, 2)}")
    print(f"Signal: {decision}\n")

if __name__ == "__main__":
    main()