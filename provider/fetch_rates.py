import os
import json
import urllib.request
import urllib.error

TARGET_CURRENCIES = ["USD", "GBP", "EUR", "CAD", "AUD", "JPY"]

def fetch_rates():
    api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
    if not api_key:
        print("Error: EXCHANGE_RATE_API_KEY environment variable not set.")
        exit(1)

    # Using USD as the base currency
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('result') != 'success':
                print(f"API Error: {data}")
                exit(1)

            conversion_rates = data.get('conversion_rates', {})
            filtered_rates = {
                curr: conversion_rates[curr] 
                for curr in TARGET_CURRENCIES 
                if curr in conversion_rates
            }
            
            # Save to compact rates.json
            with open('rates.json', 'w') as f:
                json.dump(filtered_rates, f, separators=(',', ':'))
                
            print("Successfully saved rates.json")
            
    except urllib.error.URLError as e:
        print(f"Failed to reach the API: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_rates()
