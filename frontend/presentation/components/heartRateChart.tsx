import React, { useState, useEffect } from 'react';
import { View, Text, Dimensions, StyleSheet } from 'react-native';
import { LineChart } from 'react-native-chart-kit';

export default function HeartRateChart() {
  const [heartRateData, setHeartRateData] = useState<number[]>([]);
  const maxDataPoints = 10; 

  
  const generateHeartRate = () => Math.floor(60 + Math.random() * 40); 

  
  useEffect(() => {
    const interval = setInterval(() => {
      setHeartRateData((prevData) => {
        const newHeartRate = generateHeartRate();
        const updatedData = [...prevData, newHeartRate];

        
        if (updatedData.length > maxDataPoints) {
          updatedData.shift(); 
        }
        return updatedData;
      });
    }, 1000); 

    return () => clearInterval(interval);  
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Real-time Heart Rate Chart</Text>
      {heartRateData.length > 0 ? (
        <LineChart
          data={{
            labels: Array(heartRateData.length).fill(''), 
            datasets: [
              {
                data: heartRateData,
                color: (opacity = 1) => 'red', 
              },
            ],
          }}
          width={300} 
          height={240}
          chartConfig={{
            backgroundColor: "white",
            backgroundGradientFrom: "white",
            backgroundGradientTo: "white",
            decimalPlaces: 0,
            color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
            labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
            style: {
              borderRadius: 16,
            },
            propsForDots: {
              r: '6',
              strokeWidth: '2',
              stroke: 'black',
            },
          }}
          style={styles.chart}
         
        />
      ) : (
        <Text>Loading heart rate data...</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
    borderRadius: 10
  },
  title: {
    fontSize: 20,
    marginBottom: 16,
    color: "green",
    fontWeight: 'bold',
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
});