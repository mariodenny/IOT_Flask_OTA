#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32httpUpdate.h>
#include <ArduinoJson.h>

// ----------------------------------------------------
// SETTINGS TO CHANGE
// ----------------------------------------------------
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// The current version of this code. 
// When you upload a new version to Flask, make this "1.0.1", "1.0.2", etc.
const char* CURRENT_VERSION = "1.0.0";

// Replace with the IP address of the computer running Flask
const char* SERVER_URL = "http://192.168.1.100:5000/api/firmware/latest?device=esp32";
// ----------------------------------------------------

// Time to wait between checks (in milliseconds). E.g., 10 seconds for testing.
const unsigned long CHECK_INTERVAL = 10000; 
unsigned long lastCheckTime = 0;

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.print("Booting v");
  Serial.println(CURRENT_VERSION);

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
  if (millis() - lastCheckTime >= CHECK_INTERVAL) {
    lastCheckTime = millis();
    
    if (WiFi.status() == WL_CONNECTED) {
      checkForUpdates();
    } else {
      Serial.println("Wi-Fi disconnected.");
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
    
    // Parse JSON
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, payload);
    
    if (error) {
      Serial.print("deserializeJson() failed: ");
      Serial.println(error.c_str());
      return;
    }
    
    String latest_version = doc["version"];
    String download_url = doc["url"];
    
    Serial.print("Server latest version: ");
    Serial.println(latest_version);
    Serial.print("Current version: ");
    Serial.println(CURRENT_VERSION);
    
    if (latest_version != CURRENT_VERSION) {
      Serial.println("New version found! Starting update...");
      
      // Start the update process
      t_httpUpdate_return ret = ESPhttpUpdate.update(download_url);
      
      switch (ret) {
        case HTTP_UPDATE_FAILED:
          Serial.printf("HTTP_UPDATE_FAILED Error (%d): %s\n", ESPhttpUpdate.getLastError(), ESPhttpUpdate.getLastErrorString().c_str());
          break;
        case HTTP_UPDATE_NO_UPDATES:
          Serial.println("HTTP_UPDATE_NO_UPDATES");
          break;
        case HTTP_UPDATE_OK:
          Serial.println("HTTP_UPDATE_OK"); // Note: Device will reboot automatically on success
          break;
      }
    } else {
      Serial.println("Already up to date.");
    }
  } else {
    Serial.print("Server error code: ");
    Serial.println(httpCode);
  }
  
  http.end();
}
