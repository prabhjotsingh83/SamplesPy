import csv
import json
import os
import ssl
import urllib.parse
import urllib.request

import certifi


SYMBOL = "^GSPC"
OUTPUT_FILE = "data/sp500_index_returns.csv"


def pct_return(current: float, previous: float) -> float:
    return ((current / previous) - 1.0) * 100.0


def fetch_sp500_daily_prices() -> list[dict[str, float | str]]:
    encoded_symbol = urllib.parse.quote(SYMBOL, safe="")
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded_symbol}"
        "?range=5y&interval=1d"
    )

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(request, timeout=30, context=ssl_context) as response:
        payload = json.loads(response.read().decode("utf-8"))

    result = payload["chart"]["result"][0]
    timestamps = result["timestamp"]
    closes = result["indicators"]["quote"][0]["close"]

    prices = []

    for timestamp, close in zip(timestamps, closes):
        if close is None:
            continue

        prices.append(
            {
                "date": __import__("datetime").datetime
                .fromtimestamp(timestamp)
                .strftime("%Y-%m-%d"),
                "close": float(close),
            }
        )

    return prices


def main() -> None:
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    rows = fetch_sp500_daily_prices()

    if len(rows) < 301:
        raise RuntimeError("Not enough historical data to calculate 300-day return.")

    latest = rows[-1]
    close_latest = latest["close"]

    close_1d_ago = rows[-2]["close"]
    close_10d_ago = rows[-11]["close"]
    close_300d_ago = rows[-301]["close"]

    output_row = {
        "index": "S&P 500",
        "symbol": SYMBOL,
        "as_of_date": latest["date"],
        "close_price": round(close_latest, 2),
        "return_1d_pct": round(pct_return(close_latest, close_1d_ago), 4),
        "return_10d_pct": round(pct_return(close_latest, close_10d_ago), 4),
        "return_300d_pct": round(pct_return(close_latest, close_300d_ago), 4),
    }

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=output_row.keys())
        writer.writeheader()
        writer.writerow(output_row)

    print(f"Created {OUTPUT_FILE}")


if __name__ == "__main__":
    main()