# Lesson 1: What is OTA?

Welcome to the OTA (Over-The-Air) IoT course!

## What does OTA mean?
**Over-The-Air (OTA)** means updating the software (firmware) of a device without plugging a cable into it.

Imagine you have 100 smart lights installed in the ceilings of a large building. If you find a bug in the code, climbing a ladder with a laptop and a USB cable for every single light would be a nightmare! With OTA, you can send the new code to all 100 lights over Wi-Fi.

## How does it work?
In this course, we will use a **pull mechanism**:
1. The ESP32 is connected to Wi-Fi.
2. The ESP32 asks our Flask server: *"Hey, what is the latest version?"*
3. The server replies: *"The latest is v1.2, download it from this URL."*
4. The ESP32 compares `v1.2` with its current version. If it's newer, it downloads the file and updates itself.

## What you will learn
- How to connect an ESP32 to Wi-Fi.
- How to make the ESP32 talk to a server using HTTP.
- How to build a server in Python using Flask.
- How to store data in a MySQL database.
- How to safely upload and serve new firmware files.
