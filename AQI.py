# ... (Data fetching code from above)

# Example: Assuming 'data' contains CO concentration in ppb
co_concentration = data['data'][0] 

def calculate_aqi(pollutant, concentration):
    """
    Calculates the Air Quality Index (AQI) based on pollutant concentration.

    This is a simplified example for CO. You'll need to adapt it for 
    other pollutants and consult official EPA guidelines for accurate 
    calculations and breakpoints.

    Args:
        pollutant (str): The pollutant type (e.g., "CO", "O3", "PM2.5").
        concentration (float): Pollutant concentration in relevant units.

    Returns:
        tuple: AQI value (int) and AQI category (str).
    """

    if pollutant == "CO":
        if 0 <= concentration <= 4.4:
            aqi = 0 + (50 / 4.4) * concentration 
            category = "Good"
        elif 4.5 <= concentration <= 9.4:
            aqi = 51 + (49 / 4.9) * (concentration - 4.5)
            category = "Moderate"
        elif 9.5 <= concentration <= 12.4:
            aqi = 101 + (49 / 2.9) * (concentration - 9.5)
            category = "Unhealthy for Sensitive Groups"
        # ... Add more conditions for higher AQI categories ...
        else:
            aqi = 500  # Assign maximum AQI if outside defined ranges
            category = "Hazardous" 
    # ... Add logic for other pollutants (O3, PM2.5, etc.) ... 
    else:
        aqi = -1  # Indicate an error or unsupported pollutant
        category = "Unknown"

    return int(aqi), category

aqi, category = calculate_aqi("CO", co_concentration)

print(f"AQI: {aqi} ({category})") 
