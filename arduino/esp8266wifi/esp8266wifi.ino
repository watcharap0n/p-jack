#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include <SoftwareSerial.h>
SoftwareSerial NodeSerial(D2, D3);

int Relay1 = D4;
int Relay2 = D5;
int Relay3 = D6;
int Relay4 = D7;

#define FIREBASE_HOST "p-user01-jack-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "yhKZT7vcnXkvIChclTFOvqORiFaqVNUHMPC3s5cZ"

#define WIFI_SSID "admin_01"
#define WIFI_PASSWORD "user!@#$"

void setup() {
  pinMode(D2, INPUT);
  pinMode(D3, OUTPUT);
  pinMode(Relay1, OUTPUT);
  pinMode(Relay2, OUTPUT);
  pinMode(Relay3, OUTPUT);
  pinMode(Relay4, OUTPUT);

  Serial.begin(9600);
  NodeSerial.begin(57600);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Serial.println("NodeMCU/ESP8266 Run");
  Firebase.stream("/p1/relays/node");
}

void loop() {
  while (NodeSerial.available() > 0)
  {
    float temperature = NodeSerial.parseFloat();
    uint16_t lux = NodeSerial.parseInt();
    int lv_water = NodeSerial.parseInt();
    if (NodeSerial.read() == '\n')
    {
      Serial.print("temperature: ");
      Serial.print(temperature);
      Serial.print("\t");
      Serial.print("lux : ");
      Serial.print(lux);
      Serial.print("\t");
      Serial.print("lv.Water : ");
      Serial.println(lv_water);

      StaticJsonBuffer<200> jsonBuffer;
      JsonObject& root = jsonBuffer.createObject();
      root["lux"] = lux;
      root["level_water"] = lv_water;
      root["temperature"] = temperature;

      Firebase.set("p1/sensors/", root);
      if (Firebase.failed()) {
        Serial.print("pushing /sensor failed:");
        Serial.println(Firebase.error());
        return;
      }



      if (Firebase.available()) {
        int sr1 = Firebase.getInt("p1/relays/node");
        delay(1000);
        if (sr1 == 0) {
          if (lux  > 40000) { // ถ้าแสงเกิน 40,000 ไฟจะดับ
            digitalWrite(Relay1, HIGH);
            digitalWrite(Relay2, HIGH);
          }
          if (lux < 39999) { // ถ้าน้อยกว่า 40,000 ไฟจะติด
            digitalWrite(Relay1, LOW);
            digitalWrite(Relay2, LOW);
          }
          if (temperature >= 35) { // ถ้าเกินกว่า 35 มัััันจะปล่อนละอองน้ำ
            digitalWrite(Relay3, LOW);
          }
          else {
            digitalWrite(Relay3, HIGH);
          }
          if (lv_water >= 10) {
            digitalWrite(Relay4, LOW); // ถ้า 
          }
          else {
            digitalWrite(Relay4, HIGH);
          }
        }
        else {
          if (Firebase.available()) {
            FirebaseObject event = Firebase.readEvent();
            String eventType = event.getString("type");
            eventType.toLowerCase();
            if (eventType == "") return ;
            Serial.print("event: ");
            Serial.println(eventType);
            if (eventType == "put") {
              String path = event.getString("path");
              int data = event.getInt("data");
              Serial.println("[" + path + "] " + String(data));
              if (data == 1) {
                digitalWrite(Relay1, LOW);
                digitalWrite(Relay2, LOW); // ไฟตัว 1,2 ติด คู่
              }
              else if (data == 2) {
                digitalWrite(Relay1, HIGH); // ไฟตัวแ 1,2 ดับ คู่
                digitalWrite(Relay2, HIGH);
              }
              else if (data == 3) {
                digitalWrite(Relay1, LOW); // ไฟดวงแรก ติด 
              }
              else if (data == 4) {
                digitalWrite(Relay1, HIGH); // ไฟดวงแรก ดับ
              }
              else if (data == 5 ) {
                digitalWrite(Relay2, LOW); // ไฟดวงสอง ติด
              }
              else if (data == 6) {
                digitalWrite(Relay2, HIGH); // ไฟดวงสอง ดับ
              }
              else if (data == 7) {
                digitalWrite(Relay3, HIGH); // pump แรกดับ
              }
              else if (data == 8) {
                digitalWrite(Relay3, LOW); // pump แรกติด
              }
              else if (data == 9) {
                digitalWrite(Relay4, HIGH); // pump ตัวสองดับ
              }
              else if (data == 10) {
                digitalWrite(Relay4, LOW); // pump ตัวสองติด
              }
            }
          }
        }
      }
      delay(1000);
    }
  }




}
