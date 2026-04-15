import os
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("EXCHANGE_RATE_API_KEY")
if not API_KEY:
    raise ValueError("EXCHANGE_RATE_API_KEY environment variable is missing.")

URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
TARGET_CURRENCIES = ["USD", "GBP", "EUR", "CAD", "AUD", "JPY"]

try:
    # Fetch data from API
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        if data.get("result") != "success":
            raise ValueError(f"API returned error: {data.get('error-type')}")
        
        rates = data.get("conversion_rates", {})
        
        # Filter only the target currencies
        filtered_rates = {cur: rates[cur] for cur in TARGET_CURRENCIES if cur in rates}
        
        # Save output as a compact JSON
        with open("rates.json", "w") as f:
            json.dump(filtered_rates, f, separators=(',', ':'))
            
        print("Successfully fetched and saved rates.json")

except urllib.error.URLError as e:
    print(f"Failed to fetch rates: {e}")
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
