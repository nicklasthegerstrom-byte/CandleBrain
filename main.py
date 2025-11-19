from core.indicators import (
    get_stock_data,
    add_rsi,
    generate_rsi_signal,
    add_macd, generate_macd_signal, combine_signals
)


def main():
    ticker = input("Enter stock ticker: ").upper()

    print(f"\nFetching data for {ticker}...\n")
    df = get_stock_data(ticker)

    if df.empty:
        print("No data found. Check symbol or internet.")
        return

    # Lägg till RSI och MACD i samma dataframe
    df = add_rsi(df)
    df = add_macd(df)

    # Plocka ut senaste RSI-värdena
    latest_rsi_14 = df["RSI_14"].iloc[-1]
    latest_rsi_50 = df["RSI_50"].iloc[-1]

    print(f"RSI 14-day: {round(latest_rsi_14, 2)}")
    print(f"RSI 50-day: {round(latest_rsi_50, 2)}")

    # Generera RSI-signal
    

    # Plocka ut senaste MACD-värdena (bara för att se dem)
    latest_macd = df["MACD_Line"].iloc[-1]
    latest_signal = df["Signal_Line"].iloc[-1]
    latest_hist = df["MACD_Hist"].iloc[-1]

    print(f"\nMACD Line: {round(latest_macd, 4)}")
    print(f"Signal Line: {round(latest_signal, 4)}")
    print(f"Histogram: {round(latest_hist, 4)}")

    prev_macd = df["MACD_Line"].iloc[-2]
    prev_signal = df["Signal_Line"].iloc[-2]


    rsi_decision = generate_rsi_signal(latest_rsi_14, latest_rsi_50)
    print(f"RSI Signal: {rsi_decision}")
    
    macd_signal = generate_macd_signal(latest_macd, latest_signal, prev_macd, prev_signal)
    print(f"MACD Signal: {macd_signal}")

    combined_signal = combine_signals(rsi_decision, macd_signal)
    print(f"\n→ Combined Signal: {combined_signal}")


if __name__ == "__main__":
    main()