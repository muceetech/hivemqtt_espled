import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# WiFi Configuration
WIFI_SSID = 'muceetech'
WIFI_PASSWORD = '12345678'

# MQTT Configuration
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'esp_led'
MQTT_TOPIC = b'esp/led'

# Setup LED
led = Pin(2, Pin.OUT)  # Built-in LED is on GPIO2 (active LOW)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('WiFi Connected, IP:', wlan.ifconfig()[0])

# Callback function for received MQTT messages
def mqtt_callback(topic, msg):
    print('Received message:', topic, msg)
    if msg == b'on':
        led.value(0)  # Turn ON (LOW)
    elif msg == b'off':
        led.value(1)  # Turn OFF (HIGH)

# Main program
def main():
    connect_wifi()
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(mqtt_callback)
    client.connect()
    print('Connected to MQTT Broker:', MQTT_BROKER)
    client.subscribe(MQTT_TOPIC)
    print('Subscribed to topic:', MQTT_TOPIC)

    try:
        while True:
            client.check_msg()  # Check for new messages
            time.sleep(1)
    finally:
        client.disconnect()

# Run the main program
main()
