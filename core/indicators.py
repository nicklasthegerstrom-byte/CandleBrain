from ta.trend import MACD
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


def add_macd(data):
    close = data["Close"].astype(float).squeeze()
    macd = MACD(close=close)

    data["MACD_Line"] = macd.macd()
    data["Signal_Line"] = macd.macd_signal()
    data["MACD_Hist"] = macd.macd_diff()

    return data

def generate_macd_signal(current_macd, current_signal, prev_macd, prev_signal):
    # Bullish crossover
    if prev_macd < prev_signal and current_macd > current_signal:
        return "BUY: MACD bullish crossover"
    
    # Bearish crossover
    if prev_macd > prev_signal and current_macd < current_signal:
        return "SELL: MACD bearish crossover"
    
    return "WAIT"

def combine_signals(rsi_signal, macd_signal):
    rsi_signal = rsi_signal.upper()
    macd_signal = macd_signal.upper()

    # Strong alignment BUY
    if "BUY" in rsi_signal and "BUY" in macd_signal:
        return "Positive RSI and MACD: STRONG BUY"

    # Early hint: RSI reacts first, MACD hasn't crossed yet
    if "SETUP" in rsi_signal and "WAIT" in macd_signal:
        return "WATCH: Momentum shift forming"

    # Strong alignment SELL
    if "SELL" in rsi_signal and "SELL" in macd_signal:
        return "Negative RSI and MACD: STRONG SELL"

    # Disagreement = uncertainty
    if ("BUY" in rsi_signal and "SELL" in macd_signal) or ("SELL" in rsi_signal and "BUY" in macd_signal):
        return "RSI and MACD conflict: Be careful!"
    
    return "WAIT"