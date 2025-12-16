#include <DHT.h>

#define DHTPIN 5      // Data pin
#define DHTTYPE DHT11  // DHT11 sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature(); 


  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    //  do not wait 30 seconds when we fail to read, try again quickly to 
    //  not end up with stale data 
    delay(2000);
    return;
  }

  Serial.print(temperature);
  Serial.print(",");
  Serial.print(humidity);
  // small delay of at least 2 seconds is needed by DHT11 to stablize the 
  // readings
  delay(2000); 
}
