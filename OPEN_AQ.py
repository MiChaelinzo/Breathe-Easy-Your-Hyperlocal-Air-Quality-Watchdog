import requests

# You might need an API key for OpenAQ (check their documentation)
api_key = "YOUR_OPENAQ_API_KEY" 
base_url = "https://api.openaq.org/v2/latest"

# Example: Fetch latest CO measurements near San Francisco
parameters = {
    "coordinates": "37.7749,-122.4194",  
    "radius": 10000,  # Search radius in meters
    "parameter": "co", 
    "limit": 10,  # Limit the number of results
    # "date_from": "2023-12-18T00:00:00Z", # Optional date filters
    # "date_to": "2023-12-18T23:59:59Z", 
}

response = requests.get(base_url, params=parameters)

if response.status_code == 200:
    data = response.json()
    for result in data['results']:
        print("Location:", result['location'])
        print("CO Concentration:", result['measurements'][0]['value'], result['measurements'][0]['unit']) 
else:
    print("Error:", response.status_code) 
