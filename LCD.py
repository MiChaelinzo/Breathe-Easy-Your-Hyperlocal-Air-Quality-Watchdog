#include <Wire.h> 
#include <LiquidCrystal_I2C.h> // LCD Library
#include "MQ135.h"           // CO2 sensor library
#include "DHT.h"             // Temperature/humidity sensor library
#include "PMS.h"             // PM2.5 sensor library
#include "SGP30.h"            // TVOC/HCHO sensor library

// Pin Definitions (adjust as needed)
#define CO2_PIN A0
#define DHT_PIN 2  // Digital pin for DHT sensor
#define PMS_RX 19
#define PMS_TX 18 

// LCD setup (adjust address and dimensions as needed)
LiquidCrystal_I2C lcd(0x27, 16, 2); // I2C address, columns, rows

// Sensor objects
MQ135 co2Sensor(CO2_PIN);
DHT dht(DHT_PIN, DHT11); // Replace with DHT22 if using that model
PMS pms(Serial1);  // PM2.5 sensor connected to Serial1
SGP30 sgpc3;        // TVOC and HCHO sensor

// Air quality index (AQI) variables
int aqiPM25 = 0;
int aqiHCHO = 0; 
int aqiTVOC = 0; 

// AQI Breakpoints (Simplified - you should use accurate EPA/regional breakpoints)
// (PM2.5 - µg/m3, HCHO - µg/m3, TVOC - ppb)

const int AQI_BREAKPOINTS[4][3] = {
  {0, 0, 0},      // Green - Healthy (All values below)
  {12, 40, 220}, // Yellow - Moderate (Up to these values)
  {35, 100, 660},  // Orange - Poor (Up to these values)
  {55, 150, 1200} // Red - Hazardous (Values above these)
};

void setup() {
  Serial.begin(9600); 
  Serial1.begin(9600);  // For the PM2.5 sensor
  
  lcd.init(); 
  lcd.backlight();

  dht.begin();

  // Initialize SGP30 sensor 
  if (!sgpc3.begin()){
    Serial.println("Failed to start sensor! Please check your wiring.");
    while (1); 
  }
  Serial.print("SGP30 serial #"); 
  Serial.print(sgpc3.serialnumber[0], HEX); 
  Serial.print(sgpc3.serialnumber[1], HEX); 
  Serial.println(sgpc3.serialnumber[2], HEX);

  // Wait for the SGP30 to stabilize
  delay(1000);

  co2Sensor.setR0(9.7);  // Adjust based on calibration 

  lcd.print("Initializing...");
  delay(2000);
  lcd.clear(); 
}

void loop() {
  readSensorData();
  calculateAQIs();
  displayData();
  delay(2000); // Update every 2 seconds
}

void readSensorData() {
  // Read CO2 (example - calibrate your sensor!)
  float co2PPM = co2Sensor.getPPM();
  Serial.print("CO2: ");
  Serial.print(co2PPM);
  Serial.println(" ppm");

  // Read temperature and humidity
  float temperature = dht.readTemperature(); 
  float humidity = dht.readHumidity();
  Serial.print("Temperature: "); 
  Serial.print(temperature);
  Serial.println("°C");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println("%");

  // Read PM2.5 data
  pms.read();
  Serial.print("PM2.5 (CF1): ");
  Serial.print(pms.pm25);
  Serial.print("  PM2.5 (Atmospheric): ");
  Serial.print(pms.pm25_atm);
  Serial.println(" µg/m3");

  // Read TVOC and HCHO data from SGP30 
  if (! sgpc3.IAQmeasure()) {
    Serial.println("Measurement failed");
    return;
  }
  Serial.print("TVOC  "); 
  Serial.print(sgpc3.TVOC); 
  Serial.print("ppb\t");
  Serial.print("HCHO  "); 
  Serial.print(sgpc3.HCHO); 
  Serial.println("ppb");
}

void calculateAQIs() {
  // PM2.5 AQI
  aqiPM25 = calculateIndividualAQI(pms.pm25_atm, 0); 

  // HCHO AQI
  aqiHCHO = calculateIndividualAQI(sgpc3.HCHO / 1000.0, 1);  // Assuming SGP30 HCHO is in ppb, convert to µg/m3

  // TVOC AQI
  aqiTVOC = calculateIndividualAQI(sgpc3.TVOC, 2); 

  // --- For demonstration, find the highest AQI for the overall status ---
  // In a real system, you'd likely calculate a separate AQI for each pollutant
  int highestAQI = max(max(aqiPM25, aqiHCHO), aqiTVOC);

  // --- Set LCD backlight color based on overall AQI ---
  if (highestAQI >= AQI_BREAKPOINTS[3][0]) {
    // Red - Hazardous
    // (Set LCD backlight to red) 
  } else if (highestAQI >= AQI_BREAKPOINTS[2][0]) {
    // Orange - Poor
    // (Set LCD backlight to orange)
  } else if (highestAQI >= AQI_BREAKPOINTS[1][0]) {
    // Yellow - Moderate
    // (Set LCD backlight to yellow)
  } else {
    // Green - Healthy
    // (Set LCD backlight to green) 
  }
}

// Function to calculate individual AQI for each pollutant 
// (adjust to your specific regional/EPA breakpoints and formulas)
int calculateIndividualAQI(float concentration, int pollutantIndex) {
  // Simple linear interpolation between breakpoints - inaccurate for real AQI!
  int aqi = 0; 
  for (int i = 1; i < 4; i++) {
    if (concentration <= AQI_BREAKPOINTS[i][pollutantIndex]) {
      int lowerConc = AQI_BREAKPOINTS[i - 1][pollutantIndex];
      int upperConc = AQI_BREAKPOINTS[i][pollutantIndex];
      int lowerAQI = (i - 1) * 50; // 0, 50, 100, ...
      int upperAQI = i * 50;

      aqi = map(concentration, lowerConc, upperConc, lowerAQI, upperAQI);
      break; // Exit the loop after finding the correct range
    } else {
      aqi = 500; // Default to Hazardous if concentration exceeds the highest breakpoint
    }
  }
  return aqi; 
}

void displayData() {
  // --- You will likely want a more complex LCD display strategy ---
  // This example just shows the overall AQI

  lcd.clear();

  // --- Display the calculated AQI --- 
  lcd.setCursor(0, 0);
  lcd.print("Overall AQI:");
  lcd.setCursor(0, 1);
  // You should display a more informative message (e.g., "Good", "Moderate") based on the AQI range.

  lcd.print(max(max(aqiPM25, aqiHCHO), aqiTVOC)); 
}
