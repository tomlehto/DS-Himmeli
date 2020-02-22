import paho.mqtt.client as mqtt
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig, ax = plt.subplots(3, sharex='col', sharey='row')


def animate(i):
    graph_data = open('temperature.log','r').read()
    lines = graph_data.split('\n')
    xs = [[], [], []]
    ys = [[], [], []]
    for line in lines:
        if len(line) > 1:
            id, timestamp, data = line.split(' ')
            xs[int(id)-1].append(datetime.datetime.strptime(timestamp, "%H:%M:%S"))
            ys[int(id)-1].append(float(data))
    for i in range(3):
        ax[i].clear()
        ax[i].plot(xs[i], ys[i])


def log_data(client_id, data):
    t = datetime.datetime.now()
    timestamp = str(t.hour) + ":" + str(t.minute) + ":" + str(t.second)
    with open("temperature.log", "a") as f:
        f.write(client_id + " " + timestamp + " " + str(data) + "\n")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors/+/temperature")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #parse client id from topic
    client_id = msg.topic.replace("sensors/","").replace("/temperature","")
    #write data to log with timestamp
    log_data(client_id, float(msg.payload))
    
    print(msg.topic+" "+str(msg.payload))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

client.loop_start()

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
