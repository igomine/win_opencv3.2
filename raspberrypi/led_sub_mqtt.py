import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json


def gpio_setup():
    GPIO.setmode(GPIO.BOARD)
    time.sleep(1)
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(5, GPIO.OUT)
    time.sleep(1)
    GPIO.output(3, GPIO.HIGH)
    GPIO.output(5, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(3, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)


def on_connect(client, userdata, flags, rc):
    print("connect with result code" + str(rc))
    client.subscribe("gpio_control")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    gpio = json.loads(str(msg.payload))

    if gpio['pin'] == 3:
        if gpio['value' == 0]:
            GPIO.output(3, GPIO.LOW)
        else:
            GPIO.output(3, GPIO.HIGH)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
gpio_setup()

try:
    client.connect("10.0.75.1", 61613, 60)
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()






