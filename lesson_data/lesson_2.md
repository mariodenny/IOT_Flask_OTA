# Lesson 2: ESP32 Wi-Fi & HTTP Basics

To do an OTA update, the ESP32 must connect to the internet (or local network) to download the file.

## Connecting to Wi-Fi
Here is the standard code to connect an ESP32 to Wi-Fi:

```cpp
#include <WiFi.h>

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi!");
}

void loop() {
  // Nothing here yet
}
```

## Making an HTTP GET Request
Once connected, the ESP32 can act like a web browser. It can make an HTTP request to our server.

```cpp
#include <HTTPClient.h>

void checkServer() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    // Replace with your computer's IP address
    http.begin("http://192.168.1.100:5000/api/firmware/latest");
    
    int httpResponseCode = http.GET();
    
    if (httpResponseCode > 0) {
      String payload = http.getString();
      Serial.println(payload);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
}
```

In the next lessons, we will build the server that answers this request!
