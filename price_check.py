import requests, os
from dotenv import load_dotenv

load_dotenv()
COINGECKO_API = os.getenv('COINGECKO_API')
if not COINGECKO_API:
    raise ValueError("YOUTUBE_API_KEY environment variable is not set.")

ROOT_URL = "https://api.coingecko.com/api/v3"
TOKEN = 'energy-web'

def ping_coingecko_api():
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

# Example usage

ping_coingecko_api()
