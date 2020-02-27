import paho.mqtt.client as mqtt
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import sys


if (2 != len(sys.argv)):
    print("Wrong number of arguments!")
    print("Usage: python dashboard.py [ip/address]")
    sys.exit(0)


style.use('fivethirtyeight')

fig, ax = plt.subplots(3, sharex='col', sharey='row')

#arrays for sensor timestamps and temperature data
times = [[], [], []]
temps = [[], [], []]

# animation function for live matplotlib plot
def animate(i):
    global times
    global temps
    for i in range(3):
        ax[i].clear()
        ax[i].plot(times[i], temps[i])

# Save data to log file
def log_data(client_id, data):
    global times
    global temps
    times[int(client_id)-1].append(datetime.datetime.now())
    temps[int(client_id)-1].append(float(data))
    # Remove first datapoint after 100 values have arrived
    if len(times[int(client_id)-1]) >= 100:
        times[int(client_id)-1].pop(0)
        temps[int(client_id)-1].pop(0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribe to all temperature topics with "+"-wildcard
    client.subscribe("sensors/+/temperature")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #parse client id from topic
    client_id = msg.topic.replace("sensors/","").replace("/temperature","")
    #write data to log with timestamp
    log_data(client_id, float(msg.payload))

    print(msg.topic+" "+str(msg.payload))


#Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#Connect to broker
client.connect(str(sys.argv[1]), 1883, 60)

#Start network loop
client.loop_start()

#Start animation and show plot
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
