import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import MapView, { Marker } from 'react-native-maps'; // Assuming you'll use react-native-maps

const App = () => {
  const [aqi, setAqi] = useState(null);
  const [location, setLocation] = useState({
    latitude: 37.7749, 
    longitude: -122.4194, 
  });
  const [loading, setLoading] = useState(true); 

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch('https://your-api-endpoint.com/aqi');
        const data = await response.json();
        setAqi(data.aqi);
        setLocation({ 
          latitude: data.latitude, 
          longitude: data.longitude 
        });
      } catch (error) {
        console.error("Error fetching data:", error);
        // Handle error (e.g., display error message)
      } finally {
        setLoading(false); 
      }
    };

    fetchData(); 
  }, []); 

  return (
    <View style={styles.container}>
      {loading ? ( 
        <ActivityIndicator size="large" color="#0000ff" /> 
      ) : (
        <>
          <Text style={styles.aqiText}>Current AQI: {aqi}</Text>
          <MapView
            style={styles.map}
            initialRegion={{
              latitude: location.latitude,
              longitude: location.longitude,
              latitudeDelta: 0.05, 
              longitudeDelta: 0.05,
            }}
          >
            <Marker
              coordinate={location}
              title="Your Location"
              description={`AQI: ${aqi}`} 
            />
          </MapView>
        </>
      )} 
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  aqiText: {
    fontSize: 20,
    padding: 10,
  },
  map: {
    flex: 1, 
  },
});

export default App;
