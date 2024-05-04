import requests, os
from dotenv import load_dotenv

load_dotenv()
COINGECKO_API = os.getenv('COINGECKO_API')
if not COINGECKO_API:
    raise ValueError("YOUTUBE_API_KEY environment variable is not set.")

ROOT_URL = "https://api.coingecko.com/api/v3"
TOKEN = 'energy-web-token'

def get_token_price():
    # Construct the URL for the ping endpoint with the API key as a query parameter
    url = f"{ROOT_URL}/simple/price?ids={TOKEN}&vs_currencies=usd&x_cg_demo_api_key{COINGECKO_API}"
    
    try:
        # Send GET request to CoinGecko API
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Failed to ping CoinGecko API: {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def get_token_price_on_date(date):
    # Construct the URL for the historical price endpoint with the required parameters and API key
    url = f"{ROOT_URL}/coins/bitcoin/history?date={date}&localization=false&x_cg_demo_api_key={COINGECKO_API}"
    
    try:
        # Send GET request to CoinGecko API
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            if data:
                token_price = data[0]['market_data']['current_price']['usd']
                print(f"Bitcoin price on {date}: ${token_price}")
            else:
                print(f"No data available for {date}")
        else:
            print(f"Failed to get token price for {date}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage

date = '01-01-2024'
get_token_price_on_date(date)
