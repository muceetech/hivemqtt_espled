import network
import time
from machine import ADC, Pin
from umqttsimple import MQTTClient

# ===== CONFIGURATION =====
WIFI_SSID = 'Wokwi-GUEST'
WIFI_PASS = ''

MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'esp32-analog-client'
MQTT_TOPIC = b'esp32/analog'

# ===== CONNECT TO WIFI =====
def connect_wifi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")
def connect_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Connected to MQTT broker")
    return client

# ===== MAIN PROGRAM =====
connect_wifi()
client = connect_mqtt()

adc = ADC(Pin(34))        # GPIO34
adc.atten(ADC.ATTN_11DB)  # Full range: 0 - 3.6V
adc.width(ADC.WIDTH_12BIT)

while True:
    value = adc.read()                    # 0-4095
    voltage = (value / 4095) * 3.3        # Convert to volts
    msg = "{:.2f}".format(voltage)
    print("Voltage:", msg, "V")
    client.publish(MQTT_TOPIC, msg)
    time.sleep(0.1)  # 100 ms sampling


