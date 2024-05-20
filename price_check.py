import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

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


def get_historical_chart(token, currency, period, interval):
    # Construct the URL for the historical chart price endpoint with the required parameters and API key
    url = f"{ROOT_URL}/coins/{token}/market_chart?vs_currency={currency}&days={period}&interval={interval}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_dict = response.json()
    for r_dict in response_dict:
        for r_list in response_dict[r_dict]:
            r_list[0] = epoch_converter(r_list[0])
    return response_dict

def epoch_converter(timestamp):
    epoch_time = timestamp / 1000  # Convert milliseconds to seconds
    date = datetime.fromtimestamp(epoch_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return date

def date_converter(date):
    # Convert the date string to a datetime object
    datetime_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    epoch_time = datetime_obj.timestamp()    # Convert the datetime object to a UTC timestamp in seconds
    return epoch_time

def get_time_range_price(token, start_date, end_date, currency="usd"):
    start_epoch = date_converter(start_date)
    end_epoch = date_converter(end_date)
    url = f"{ROOT_URL}/coins/{token}/market_chart/range?vs_currency={currency}&from={start_epoch}&to={end_epoch}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_dict = response.json()
    for r_dict in response_dict:
        for r_list in response_dict[r_dict]:
            r_list[0] = epoch_converter(r_list[0])
    return response_dict['prices']

# Example usage
# if __name__ == "__main__":
#     date = '10-05-2024'
#     token = 'energy-web-token'
#     get_token_price_on_date(date, token)


token = "energy-web-token"
currency = "usd"
period = 10
interval = "daily"
print(get_historical_chart(token, currency, period, interval))

print(get_time_range_price("energy-web-token", "2024-05-01 00:00:00", "2024-05-07 00:00:00"))

