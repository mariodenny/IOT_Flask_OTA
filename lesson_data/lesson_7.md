# Lesson 7: Extending the System

Congratulations! You have built a full OTA system. But this is just the beginning.

## Ideas for Next Steps

### 1. Support Multiple Device Types
What if you have both ESP32 lights and ESP8266 temperature sensors?
- Our database already has a `device_type` column!
- You can upload firmware and type "esp8266_sensor".
- Change the Arduino code URL to: `http://192.168.1.100:5000/api/firmware/latest?device=esp8266_sensor`

### 2. Add a Rollback Feature
Sometimes new firmware has a bad bug. You can build a button in Flask to "Activate" an older version.
- Change the MySQL query from `ORDER BY uploaded_at DESC` to `WHERE status = 'active'`.

### 3. Display the IP Address on a Screen
If you add an OLED screen to your ESP32, you can print the current version and IP address on it. This makes debugging much easier.

### 4. Improve Security
Currently, the ESP32 downloads the firmware using standard HTTP. This means anyone on your network could intercept it.
For a real product, you would use HTTPS with certificates!

Good luck with your future IoT projects!
