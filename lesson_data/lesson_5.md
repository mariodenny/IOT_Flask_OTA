# Lesson 5: ESP32 OTA Update

Now we put everything together on the ESP32!

We will use a library called `ESP32httpUpdate` which does all the hard work of downloading the file and saving it into the ESP32's memory. We also use `ArduinoJson` to read the JSON from our server.

## Full OTA Code Example

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32httpUpdate.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* CURRENT_VERSION = "1.0.0";
const char* SERVER_URL = "http://192.168.1.100:5000/api/firmware/latest";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  Serial.println("Connected!");
  
  checkForUpdates();
}

void loop() { }

void checkForUpdates() {
  HTTPClient http;
  http.begin(SERVER_URL);
  int httpCode = http.GET();
  
  if (httpCode == 200) {
    String payload = http.getString();
    
    // Parse JSON
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, payload);
    
    String latest_version = doc["version"];
    String download_url = doc["url"];
    
    if (latest_version != CURRENT_VERSION) {
      Serial.println("New version found! Updating...");
      t_httpUpdate_return ret = ESPhttpUpdate.update(download_url);
      
      if (ret == HTTP_UPDATE_OK) {
        Serial.println("Update success! Rebooting...");
      } else {
        Serial.println("Update failed.");
      }
    } else {
      Serial.println("Already up to date.");
    }
  }
  http.end();
}
```

*Note: You must install the `ArduinoJson` library in your Arduino IDE to use this.*
