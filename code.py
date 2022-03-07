# SPDX-FileCopyrightText: 2022 Daniel Griswold
#
# SPDX-License-Identifier: MIT

"""

Temperature Sensor with data published to MQTT.


"""

import time
import ssl
import json
import board
import socketpool
import wifi
import digitalio
import microcontroller

import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_ahtx0

# pylint: disable=no-name-in-module,wrong-import-order
from secrets import secrets

UPDATE_INTERVAL = 60
MQTT_ENVIRONMENT = secrets["mqtt_topic"] + "/environment"
MQTT_SYSTEM = secrets["mqtt_topic"] + "/system"


def get_sensor_data():
    """ Creates dictionary of sensor values. """
    _data = {}
    _data["temperature"] = aht20.temperature
    _data["humidity"] = aht20.relative_humidity
    return _data


def get_system_data():
    """Creates dictionary of system information"""
    _data = {}
    _data["reset_reason"] = str(microcontroller.cpu.reset_reason)[28:]
    _data["time"] = time.monotonic()
    _data["ip_address"] = wifi.radio.ipv4_address
    _data["board_id"] = board.board_id
    return _data


if board.id == "unexpectedmaker_feathers2":
    ldo2 = digitalio.DigitalInOut(board.LDO2)
    ldo2.switch_to_output(True)

if board.id == "unexpectedmaker_feathers3":
    ldo2 = digitalio.DigitalInOut(board.LDO2)
    ldo2.switch_to_output(True)

if board.id == "adafruit_feather_esp32s2":
    i2c_power = digitalio.DigitalInOut(board.I2C_POWER_INVERTED)
    i2c_power.switch_to_output(False)

if board.id == "adafruit_feather_esp32s2_tft":
    i2c_power = digitalio.DigitalInOut(board.TFT_I2C_POWER)
    i2c_power.switch_to_output(True)

aht20 = adafruit_ahtx0.AHTx0(board.I2C())

try:
    print("Connecting to %s..." % secrets["ssid"])
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("Connected to %s!" % secrets["ssid"])
    pool = socketpool.SocketPool(wifi.radio)
except Exception as error:
    print("Could not initialize network. {}".format(error))
    raise

try:
    mqtt_client = MQTT.MQTT(
        broker=secrets["mqtt_broker"],
        port=secrets["mqtt_port"],
        username=secrets["mqtt_username"],
        password=secrets["mqtt_password"],
        socket_pool=pool,
        ssl_context=ssl.create_default_context(),
    )
    mqtt_client.connect()
except MQTT.MMQTTException as error:
    print("Could not connect to mqtt broker. {}".format(error))
    raise

last_update = 0  # pylint: disable=invalid-name

while True:
    _now = time.monotonic()

    if last_update + UPDATE_INTERVAL < _now:
        last_update = _now

        print("Publishing environmental data")
        try:
            mqtt_client.publish(
                MQTT_ENVIRONMENT, json.dumps(get_sensor_data()), retain=True
            )
        except MQTT.MMQTTException as error:
            print("Could not publish to mqtt broker. {}".format(error))

        print("Publishing system data")
        try:
            mqtt_client.publish(MQTT_SYSTEM, json.dumps(get_system_data()), retain=True)
        except MQTT.MMQTTException as error:
            print("Could not publish to mqtt broker. {}".format(error))
