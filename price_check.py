import requests
import os
from dotenv import load_dotenv

load_dotenv()
COINGECKO_API = os.getenv('COINGECKO_API')
if not COINGECKO_API:
    raise ValueError("COINGECKO_API environment variable is not set.")

ROOT_URL = "https://api.coingecko.com/api/v3"

def get_token_price(token):
    # Construct the URL for fetching token price with the API key as a query parameter
    url = f"{ROOT_URL}/simple/price?ids={token}&vs_currencies=usd&x_cg_demo_api_key={COINGECKO_API}"
    
    try:
        # Send GET request to CoinGecko API
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Failed to fetch token price: {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def get_token_price_on_date(date, token):
    # Construct the URL for the historical token price endpoint with the required parameters and API key
    url = f"{ROOT_URL}/coins/{token}/history?date={date}&x_cg_demo_api_key={COINGECKO_API}"
    
    try:
        # Send GET request to CoinGecko API
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            if data:
                token_price = data['market_data']['current_price']['usd']
                print(f"Token price on {date}: ${token_price}")
            else:
                print(f"No data available for {date}")
        else:
            print(f"Failed to get token price for {date}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Response content: {response.text}")  # Print response content for debugging

# Example usage
date = '08-05-2024'
token = 'energy-web-token'
get_token_price_on_date(date, token)


# get_token_price()