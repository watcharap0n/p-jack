#include "DHT.h"
#include <BH1750FVI.h>
#include <SoftwareSerial.h>
#define DHTPIN 6
#define DHTTYPE DHT11

int val = 0;
int xkc = A0;

SoftwareSerial UnoSerial(3, 2);
DHT dht(DHTPIN, DHTTYPE);
BH1750FVI LightSensor(BH1750FVI::k_DevModeContLowRes);

void setup() {
  Serial.begin(9600);
  UnoSerial.begin(57600);
  Serial.println("Starting In Progress...");

  dht.begin();
  pinMode(xkc, INPUT);
  LightSensor.begin();
}


void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  val = analogRead(xkc);
  uint16_t lux = LightSensor.GetLightIntensity();


  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  float hi = dht.computeHeatIndex(f, h);

  Serial.print("Light: ");
  Serial.print(lux);
  Serial.print(" lux");
  Serial.print(" lv.water: ");
  Serial.print(val);
  Serial.print(" Temperature: ");
  Serial.println(t);
  delay(1000);

  UnoSerial.print(t);
  UnoSerial.print(" ");
  UnoSerial.print(lux);
  UnoSerial.print(" ");
  UnoSerial.print(val);
  UnoSerial.print("\n");
  delay(500);

}
