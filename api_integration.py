import requests
import csv
from datetime import datetime

def get_crypto_prices(cryptos, currency="usd"):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": ",".join(cryptos), "vs_currencies": currency}

        response = requests.get(url, params=params)
        response.raise_for_status()  # check for HTTP errors
        data = response.json()

        results = []
        for crypto in cryptos:
            if crypto in data:
                price = data[crypto][currency]
                print(f"The current price of {crypto.capitalize()} is {price} {currency.upper()}")
                results.append([crypto, price, currency.upper(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            else:
                print(f"⚠️ {crypto} not found. Skipping.")

        # Save results to CSV
        if results:
            with open("crypto_prices.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Crypto", "Price", "Currency", "Timestamp"])
                writer.writerows(results)
            print("✅ Results saved to crypto_prices.csv")

    except requests.exceptions.RequestException as e:
        print("❌ Error fetching data:", e)

if __name__ == "__main__":
    print("🔹 Crypto Price Checker 🔹")
    cryptos = input("Enter cryptocurrencies (comma separated, e.g., bitcoin, ethereum): ").lower().split(",")
    currency = input("Enter currency (e.g., usd, inr, eur): ").lower()
    get_crypto_prices([c.strip() for c in cryptos], currency)
