air_quality_data = {
    "CO2": [],         # List to store CO2 readings (ppm)
    "TVOC": [],        # List to store TVOC readings (ppb)
    "HCHO": [],        # List to store HCHO readings (ppb)
    "PM2.5": [],       # List to store PM2.5 readings (µg/m³)
    "humidity": [],     # List to store humidity readings (%)
    "temperature": [], # List to store temperature readings (°C)
}
# Assuming you have functions to read data from your sensors:
co2_reading = read_co2_sensor() # Replace 'read_co2_sensor()' with your actual function
tvoc_reading = read_tvoc_sensor()
# ... Read data from other sensors 

# Store data in the dictionary:
air_quality_data["CO2"].append(co2_reading)
air_quality_data["TVOC"].append(tvoc_reading)
# ... Append data from other sensors

# Example: Print the latest readings
print("Latest Readings:")
for pollutant, reading in air_quality_data.items():
  if reading:  # Check if the reading list is not empty
      print(f"{pollutant}: {reading[-1]}")
  else:
      print(f"{pollutant}: No data available.") 
def calculate_aqi(pollutant, concentration):
    """Calculates AQI for various pollutants based on EPA guidelines.
       Note: This is a simplified example, consult actual EPA tables and formulas.

    Args:
        pollutant (str): The pollutant ("CO2", "TVOC", "HCHO", "PM2.5").
        concentration (float): The concentration in the relevant unit.

    Returns:
        int: The AQI value (0-500). 
    """

    if pollutant == "CO2":
        # CO2 is usually not included in standard AQI calculations
        return -1  # Indicate unsupported pollutant for AQI

    aqi = 0 # Default value, will be updated if valid calculation is found

    # Example (replace with accurate AQI calculation logic for each pollutant)
    if pollutant == "TVOC":
        if concentration <= 220:
            aqi = 50  # Good
        elif concentration <= 660:
            aqi = 100 # Moderate 
        # ... Add more breakpoints and categories based on EPA guidelines ...
        
    elif pollutant == "HCHO": 
        # Add breakpoints and AQI calculation based on HCHO (Formaldehyde) 

    elif pollutant == "PM2.5":
        # Add breakpoints and AQI calculation based on PM2.5
    else:
        return -1 # Indicate an error or unsupported pollutant

    return int(aqi)

# Calculate AQI for each pollutant
for pollutant, reading_list in air_quality_data.items():
  if reading_list:
      latest_reading = reading_list[-1]
      aqi_value = calculate_aqi(pollutant, latest_reading)
      if aqi_value >= 0:
        print(f"{pollutant} AQI: {aqi_value}")
