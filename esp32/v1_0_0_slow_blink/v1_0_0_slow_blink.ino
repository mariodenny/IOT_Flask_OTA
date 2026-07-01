#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32httpUpdate.h>
#include <ArduinoJson.h>

// ----------------------------------------------------
// SETTINGS TO CHANGE
// ----------------------------------------------------
const char* ssid = "ikan terbang";
const char* password = "11221122";

// THIS IS VERSION 1.0.0 (The Slow Blink)
const char* CURRENT_VERSION = "1.0.0";

// Replace with the IP address of the computer running Flask
const char* SERVER_URL = " http://10.157.245.125:5000//api/firmware/latest?device=esp32";
// ----------------------------------------------------

const unsigned long CHECK_INTERVAL = 10000; 
unsigned long lastCheckTime = 0;

// LED Blink Variables
const int LED_PIN = 2; // Onboard LED for DOIT ESP32
unsigned long previousMillis = 0;
// SLOW BLINK: 1000ms (1 second on, 1 second off)
const long interval = 1000; 
int ledState = LOW;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println();
  Serial.print("Booting v");
  Serial.println(CURRENT_VERSION);
  Serial.println("FEATURE: SLOW BLINK");

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  unsigned long currentMillis = millis();

  // 1. BLINK THE LED (The "Feature")
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    if (ledState == LOW) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }
    digitalWrite(LED_PIN, ledState);
  }

  // 2. CHECK FOR OTA UPDATES
  if (currentMillis - lastCheckTime >= CHECK_INTERVAL) {
    lastCheckTime = currentMillis;
    
    if (WiFi.status() == WL_CONNECTED) {
      checkForUpdates();
    }
  }
}

void checkForUpdates() {
  Serial.println("Checking for updates...");
  
  HTTPClient http;
  http.begin(SERVER_URL);
  int httpCode = http.GET();
  
  if (httpCode == 200) {
    String payload = http.getString();
    
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, payload);
    
    if (error) {
      Serial.println("deserializeJson() failed");
      return;
    }
    
    String latest_version = doc["version"];
    String download_url = doc["url"];
    
    if (latest_version != CURRENT_VERSION) {
      Serial.println("New version found! Starting update...");
      t_httpUpdate_return ret = ESPhttpUpdate.update(download_url);
      
      if(ret == HTTP_UPDATE_OK) {
        Serial.println("HTTP_UPDATE_OK"); 
      }
    } else {
      Serial.println("Already up to date.");
    }
  }
  http.end();
}
