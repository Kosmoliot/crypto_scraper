import requests, os
from dotenv import load_dotenv

load_dotenv()
COINGECKO_API = os.getenv('COINGECKO_API')
if not COINGECKO_API:
    raise ValueError("YOUTUBE_API_KEY environment variable is not set.")


def ping_coingecko_api():
    # CoinGecko API endpoint for ping
    url = "https://pro-api.coingecko.com/api/v3/ping"

    # Replace 'YOUR_API_KEY' with your actual API key
    headers = {
        'Content-Type': 'application/json',
        'x-cg-pro-api-key': COINGECKO_API
    }

    try:
        # Send GET request to CoinGecko API
        response = requests.get(url, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            print("CoinGecko API is accessible.")
        else:
            print(f"Failed to ping CoinGecko API: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage

ping_coingecko_api()
