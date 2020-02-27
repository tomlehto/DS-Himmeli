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
mosquitto_pub -t config/period -m <value>
```

## RasPi deployment
To use with BMP280 sensor connected to a Raspberry Pi device, change the following flag to 1:
```python
#Set to 1 if BMP280 sensor is connected to device
REAL_SENSOR = 0
```


