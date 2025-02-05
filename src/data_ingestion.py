import requests
import json
import os

def fetch_crypto_data(coin_id="bitcoin", vs_currency="usd", days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    response = requests.get(url, params=params)
    
    # Debug prints to check what we're getting
    print(f"Request URL: {response.url}")
    print(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("Fetched Data (sample):", str(data)[:1500])  # print first 300 chars
            return data
        except Exception as e:
            print("Error parsing JSON:", e)
            return None
    else:
        print("Error fetching data:", response.status_code)
        print("Response Text:", response.text)
        return None

def save_data_to_file(data, filename="data/bitcoin_data.json"):
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    crypto_data = fetch_crypto_data()
    if crypto_data:
        save_data_to_file(crypto_data)
    else:
        print("No data fetched.")

