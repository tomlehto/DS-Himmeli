#Set to 1 if BMP280 sensor is connected to device
REAL_SENSOR = 0

# time interval (s) to read sensor data
MEAS_PERIOD = 0.5

import paho.mqtt.client as mqtt
import random
import time
import sys

if REAL_SENSOR:
    import board
    import busio
    import adafruit_bmp280

# Control dictionary for temperature measurements
# 'result' is current filtered temperature
# 'alpha' is weighting factor. Higher alpha discounts older samples faster
# 'n' is the number of samples collected
# 'N' is the number of total samples on the reporting period.
# Temperature is measured every MEAS_PERIOD (s) and averaged value is published every 'period' (s)
# N = period / MEAS_PERIOD
measurement = {
    "result": 0.0,
    "alpha": 0.0,
    "n": 0,
    "N": 0
}

# function to reset meas data when state == 0
def reset_meas():
    measurement["result"] = 0.0
    measurement["n"] = 0

# returns alpha for moving average filter
# alpha = 2 / (N + 1)
def calc_alpha(N):
    return 2.0 / (float(N) + 1.0)

# exponential moving average
def moving_average(old_result, new_result, alpha, n):
    if n in [0, 1]:
        return new_result
    else:
        return round((alpha * new_result + (1.0 - alpha) * old_result), 2)

state = 1
period = 2

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
        if int(msg.payload) == 0:
            reset_meas()
            state = 0
        elif int(msg.payload) == 1:
            state = 1
    elif msg.topic == "config/period":
        if int(msg.payload) >= 1:
            period = int(msg.payload)
            measurement["N"] = int(float(period) / MEAS_PERIOD)
            measurement["alpha"] = calc_alpha(measurement["N"])

def read_sensor():
    if REAL_SENSOR:
        return sensor.temperature
    else:
        return float(random.randint(20,25))

# Initial parameters
measurement["N"] = int(float(period) / MEAS_PERIOD)
measurement["alpha"] = calc_alpha(measurement["N"])

#Initialize BMP280 sensor via I2C
if REAL_SENSOR:
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

#Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#Connect to broker
client.connect(str(sys.argv[1]), 1883, 60)

#Start network loop
client.loop_start()

while True:
    time.sleep(MEAS_PERIOD)
    # TODO: change read_sensor call to stubbed Sensor class method
    if state == 1:
        temperature = read_sensor()
        measurement["n"] += 1
        measurement["result"] = moving_average(measurement["result"],
                                               temperature,
                                               measurement["alpha"],
                                               measurement["n"])

        if measurement["n"] == measurement["N"]:
            client.publish("sensors/"+str(sys.argv[2])+"/temperature", measurement["result"])
            reset_meas()
