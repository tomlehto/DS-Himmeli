# DS-Himmeli
Course project for 521290S Distributed Systems

## Demo
Following Python modules are required:
```
paho-mqtt
matplotlib
```

MQTT broker used is mosquitto, which needs to be installed.


Start demo, which will start mosquitto MQTT broker, 3 sensor nodes and data visualizer:
```bash
chmod +x demo_script.sh
./demo_script.sh
```

Set sensor state to be on or off:
```bash
#on
mosquitto_pub -t config/state -m 1
#off
mosquitto_pub -t config/state -m 0
```

Change sensor data reporting period (value in seconds, default is 1):
```bash
mosquitto_pub -t config/period-m <value>
```


