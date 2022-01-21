//Include modules
#include <Wire.h>
#include <DHT.h>

// intiialize temp & hum sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302)
#define DHTPIN 5
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  while (!Serial) {
    delay(10);
  }
}
 
void loop() {
  //Serial Data Out
  float temperature, humidity;

  humidity = dht.readHumidity();
  temperature = dht.readTemperature();
  
  Serial.print(humidity);
  Serial.print(" "); 
  Serial.print(temperature*(1.800)+32); //need to manually adjust the sensor smh
  Serial.print(" ");
  Serial.println();   
  
  delay(1);
}
