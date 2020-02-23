import paho.mqtt.client as mqtt
import random
import time
import sys

state = 1
period = 1

if (3 != len(sys.argv)):
    print("Wrong number of arguments!")
    print("Usage: python client.py [ip/address] [client_id]")
    sys.exit(0)
elif (int(sys.argv[2]) < 1 or int(sys.argv[2]) > 3):
    print("Client id must equal 1, 2 or 3")
    sys.exit(0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("config/period") # period is the sensor data reporting period in seconds, any value over 1 is considered valid
    client.subscribe("config/state") # state is 0 or 1 (off/on)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global state
    global period
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "config/state":
        if int(msg.payload) == 0 or int(msg.payload) == 1:
            state = int(msg.payload)
    elif msg.topic == "config/period":
        if int(msg.payload) >= 1:
            period = int(msg.payload)

def read_sensor():
    return random.randint(-30,30)

#Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#Connect to broker
client.connect(str(sys.argv[1]), 1883, 60)

#Start network loop
client.loop_start()

while True:
    time.sleep(period)
    # TODO: change read_sensor call to stubbed Sensor class method
    if state == 1:
        temperature = read_sensor()
        client.publish("sensors/"+str(sys.argv[2])+"/temperature", temperature)

