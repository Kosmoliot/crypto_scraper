import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
COINGECKO_API = os.getenv('COINGECKO_API')
if not COINGECKO_API:
    raise ValueError("COINGECKO_API environment variable is not set.")

ROOT_URL = "https://api.coingecko.com/api/v3"


def epoch_converter(timestamp):
    """Convert epoch time in milliseconds to human-readable date."""
    try:
        epoch_time = timestamp / 1000  # Convert milliseconds to seconds
        date = datetime.fromtimestamp(epoch_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        return date
    except Exception as e:
        print(f"Error converting epoch time: {e}")
        return None


def date_converter(date_str):
    """Convert human-readable date to epoch time in seconds."""
    try:
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        epoch_time = int(datetime_obj.timestamp())  # Convert datetime object to UTC timestamp in seconds
        return epoch_time
    except ValueError as e:
        print(f"Error converting date to epoch time: {e}")
        return None


def get_token_price(token):
    """Get current token price."""
    url = f"{ROOT_URL}/simple/price?ids={token}&vs_currencies=usd&x_cg_demo_api_key={COINGECKO_API}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token price: {e}")
        return None


def get_token_price_on_date(date, token):
    """Get token price on a specific date."""
    formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
    url = f"{ROOT_URL}/coins/{token}/history?date={formatted_date}&x_cg_demo_api_key={COINGECKO_API}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        token_price = data['market_data']['current_price']['usd']
        print(f"Token price on {date}: ${token_price}")
        return token_price
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token price for {date}: {e}")
    except KeyError:
        print(f"No data available for {date}")
    return None


def get_historical_chart(token, currency, period, interval):
    """Get historical chart data for a token."""
    url = f"{ROOT_URL}/coins/{token}/market_chart?vs_currency={currency}&days={period}&interval={interval}"
    try:
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        for key in response_dict:
            for r_list in response_dict[key]:
                r_list[0] = epoch_converter(r_list[0])
        return response_dict
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical chart data: {e}")
        return None


def get_time_range_price(token, start_date, end_date, currency="usd"):
    """Get token prices within a time range."""
    start_epoch = date_converter(start_date)
    end_epoch = date_converter(end_date)
    url = f"{ROOT_URL}/coins/{token}/market_chart/range?vs_currency={currency}&from={start_epoch}&to={end_epoch}"
    try:
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        for key in response_dict:
            for r_list in response_dict[key]:
                r_list[0] = epoch_converter(r_list[0])
        return response_dict.get('prices', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching time range price data: {e}")
        return None

# Example usage
# if __name__ == "__main__":
#     date = '10-05-2024'
#     token = 'energy-web-token'
#     get_token_price_on_date(date, token)


# token = "energy-web-token"
# currency = "usd"
# period = 1
# interval = "daily"
# print(get_historical_chart(token, currency, period, interval))

# Example usage
if __name__ == "__main__":
    token = "energy-web-token"
    start_date = "2024-05-20 00:00:00"
    end_date = "2024-05-21 00:00:00"
    prices = get_time_range_price(token, start_date, end_date)
    if prices:
        for price in prices:
            print(f"Price at {price[0]}: {price[1]} USD")

