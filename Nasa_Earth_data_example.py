import requests

# Replace with your actual API key
api_key = "YOUR_NASA_EARTHDATA_API_KEY"

base_url = "https://api.nasa.gov/planetary/earth/imagery?"

# Example: Fetching AIRS Carbon Monoxide data
parameters = {
    "lon": "-122.4194",  # Example coordinates (San Francisco)
    "lat": "37.7749",
    "date": "2023-12-18",
    "dim": "0.1",  # Image dimension (degrees)
    "api_key": api_key,
}

response = requests.get(base_url, params=parameters)

if response.status_code == 200:
    data = response.json()
    # Process and extract relevant air quality data from the 'data' field
    print(data)
else:
    print("Error:", response.status_code)
