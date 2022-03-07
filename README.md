<!--
SPDX-FileCopyrightText: 2022 Daniel Griswold

SPDX-License-Identifier: MIT
-->

# Temperature/Humidity Monitor


## Overview

This repository contains code and details that collect local environmental data and publish that data to MQTT.  Data points include temperature and humidity.  See https://github.com/dgriswo/Feather-AQI-Monitor for monitoring air quality and particultates in addition to temperature and humidity.

MQTT is a standard, lightweight, messaging protocol for IoT devices and provides a nice medium for integrations into other systems, such as Home Assistant or InfluxDB.


## Hardware

- Feather development board https://www.adafruit.com/product/4769
  - CircuitPython compatible
  - Standard wifi library (not airlift)
  > Note: This was built on an Unexpected Maker FeatherS2 using CircuitPython 7.1.0, but should be compatible with other wifi-enabled boards and later CircuitPython versions.
- AHT20 Temperature and Humidity Sensor https://www.adafruit.com/product/4566


Optional:
- 1 STEMMA QT cable https://www.adafruit.com/product/4399


## 3D Printed Enclosure

This is a snap together enclosure to contain the Feather dev board and allow mounting the AHT20 outside of the enclosure.  By mounting the temperature sensor outside, it is protected from the heat output of the ESP32-S2.  There is also a small notch to allow a fingernail to split the lid from the base.

The enclosure will accomodate a 400 MAh battery. https://www.adafruit.com/product/3898  However, the code is not optimized for battery life.

Holes are designed to use M2.5 screws and will support most Adafruit STEMMA sensors in the 1.0" x 0.7" form factor.

  https://www.tinkercad.com/things/bblzmxxe0jq (Licensed under CC BY-SA 3.0)

<img src="https://user-images.githubusercontent.com/15717486/156970389-4094a82a-aa19-4676-ac66-46b542086f32.jpeg" width=336 height=252>
<img src="https://user-images.githubusercontent.com/15717486/156970422-b3a7e013-bcf3-4392-b2c2-1e63ed37244b.jpeg" width=336 height=252>

 ## Install

 1. Copy the repository contents to the CIRCUITPY drive.
 2. Use circup to install the required libraries. [Circup Overview](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup)

         circup install -r requirements.txt

3. Copy secrets.example to secrets.py and edit with appropriate values.

Other settings in code.py
- UPDATE_INTERVAL = 60 # Frequency to publish sensor data to MQTT in seconds.


## Sample output to MQTT

/environment:
    {
        "temperature": 23.8124,
        "humidity": 26.1576,
    }

/system:
    {
        "time": 3237.76,
        "ip_address": 192.168.x.x,
        "board_id": "unexpectedmaker_feathers2",
        "reset_reason": "POWER_ON"
    }
