import requests

api_key = "YOUR_FRED_API_KEY"  # Replace with your actual FRED API key
fred_url = "https://api.stlouisfed.org/fred/series/observations"

params = {
    "api_key": api_key,
    "id": "DFFFR",  # Interest Rate on Federal Funds (Effective)
    "observation_start": "2024-05-07",
    "observation_end": "2024-05-07",
    "output": "json"
}



response = requests.get(fred_url, params=params)

if response.status_code == 200:
    data = response.json()
    # Process the data to extract the yield
else:
    print("Error:", response.status_code)



if data and data["observations"]:
    latest_observation = data["observations"][0]
    yield_value = latest_observation["value"]
    print("Current Federal Funds Rate (as of", latest_observation["date"], "):", yield_value, "%")
else:
    print("Error: No data retrieved from FRED API")
