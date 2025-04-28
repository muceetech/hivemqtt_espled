import network
import time
from umqttsimple import MQTTClient
import machine

# --- WiFi details
ssid = 'Rajnarain'
password = 'narain12'

# --- MQTT broker
mqtt_server = 'broker.emqx.io'
mqtt_topic = b'esp/led'

# --- LED pin
led = machine.Pin(2, machine.Pin.OUT)  # GPIO2 is the onboard LED (active LOW)

# --- Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(0.5)
            print('.', end='')
    print('WiFi connected:', wlan.ifconfig())

# --- MQTT callback
def mqtt_callback(topic, msg):
    print((topic, msg))
    if msg == b'on':
        led.value(0)  # Turn ON (active LOW)
    elif msg == b'off':
        led.value(1)  # Turn OFF

# --- Connect to MQTT
def connect_mqtt():
    client = MQTTClient('esp8266_client', mqtt_server)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(mqtt_topic)
    print('Connected to MQTT broker and subscribed to', mqtt_topic)
    return client

# --- Main
connect_wifi()
client = connect_mqtt()

while True:
    try:
        client.check_msg()
    except OSError as e:
        print('MQTT error:', e)
        time.sleep(5)
        machine.reset()
